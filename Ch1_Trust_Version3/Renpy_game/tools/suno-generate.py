# -*- coding: utf-8 -*-
r"""Suno 音樂生成（AceData Cloud API）

Token 讀取順序同 seedance-generate.py：
  1. 環境變數 ACEDATA_API_TOKEN
  2. tools\.env 的 ACEDATA_API_TOKEN

用法（在 Renpy_game 目錄）：

  python tools\suno-generate.py --preset tense
  python tools\suno-generate.py --prompt "instrumental tense piano" --instrumental
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

API_URL = "https://api.acedata.cloud/suno/audios"
TASK_URL = "https://api.acedata.cloud/suno/tasks"
DEFAULT_MODEL = "chirp-v5-5"
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_AUDIO = os.path.abspath(os.path.join(TOOLS_DIR, "..", "..", "assets", "audio"))

PRESETS = {
    "tense": {
        "title": "Alley Pass Tense",
        "custom": True,
        "instrumental": True,
        "duration": 90,
        "style": (
            "instrumental only, no vocals; restrained Taiwan slice-of-life visual novel score; "
            "sudden tense swell without jump scare; sparse low piano, muted strings, dry anxious pulse; "
            "76 BPM minor but warm; seamless loopable bed for a scooter passing too close in a narrow alley; "
            "leave space for spoken dialogue"
        ),
        "negative_tags": "vocals, singing, lyrics, choir, horror, jump scare, EDM, dubstep, epic orchestra, comedy, ukulele",
        "install_as": "tense.ogg",
    }
}


def load_env_value(key):
    val = os.environ.get(key, "").strip()
    if val:
        return val
    env_path = os.path.join(TOOLS_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith(key + "="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def load_token():
    return load_env_value("ACEDATA_API_TOKEN")


def post_json(url, payload, token, timeout):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"[錯誤] HTTP {e.code}：{body}")
    except urllib.error.URLError as e:
        sys.exit(f"[錯誤] 連線失敗：{e.reason}")


def download(url, out_path):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=300) as resp, open(out_path, "wb") as f:
        while True:
            chunk = resp.read(65536)
            if not chunk:
                break
            f.write(chunk)


def tracks_from(result):
    if not isinstance(result, dict):
        return []
    data = result.get("data")
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        inner = data.get("data") or data.get("audios") or []
        if isinstance(inner, list):
            return inner
    resp = result.get("response")
    if isinstance(resp, dict):
        inner = resp.get("data") or []
        if isinstance(inner, list):
            return inner
    return []


def poll_task(task_id, token, timeout_s=180):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        result = post_json(TASK_URL, {"action": "retrieve", "id": task_id}, token, 60)
        tracks = tracks_from(result)
        states = [t.get("state") for t in tracks] if tracks else [result.get("status") or result.get("state")]
        print(f"[輪詢] {', '.join(str(s) for s in states)}")
        if tracks and all(s == "succeeded" for s in states) and all(t.get("audio_url") for t in tracks):
            return result, tracks
        if any(s == "error" for s in states) or result.get("success") is False:
            sys.exit(f"[錯誤] 任務失敗：{json.dumps(result, ensure_ascii=False)[:2000]}")
        time.sleep(8)
    sys.exit("[錯誤] 等待逾時（仍在排隊或生成中）")


def to_ogg(src, dest):
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        sys.exit("[錯誤] 找不到 ffmpeg")
    os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
    cmd = [ffmpeg, "-y", "-i", src, "-c:a", "libvorbis", "-q:a", "5", dest]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    p = argparse.ArgumentParser(description="Suno 音樂生成（AceData API）")
    p.add_argument("--preset", choices=sorted(PRESETS), help="內建曲目（tense＝S08 機車）")
    p.add_argument("--prompt", help="靈感模式 prompt（custom=false）")
    p.add_argument("--style", help="自訂模式 style")
    p.add_argument("--title", default="Untitled")
    p.add_argument("--instrumental", action="store_true")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--duration", type=int, default=90)
    p.add_argument("--install-as", help="轉 OGG 後寫入 assets/audio 的檔名，例如 tense.ogg")
    args = p.parse_args()

    token = load_token()
    if not token:
        sys.exit("[錯誤] 未設定 ACEDATA_API_TOKEN（tools\\.env）")
    from acedata_account import report_account
    report_account("開始")

    preset = PRESETS.get(args.preset or "", {})
    custom = bool(preset.get("custom") or args.style)
    instrumental = bool(preset.get("instrumental") or args.instrumental)
    style = args.style or preset.get("style")
    title = args.title if args.title != "Untitled" else preset.get("title") or args.title
    duration = preset.get("duration") or args.duration
    install_as = args.install_as or preset.get("install_as")
    prompt = args.prompt

    if not custom and not prompt:
        sys.exit("[錯誤] 請給 --preset tense，或 --prompt／--style")

    payload = {
        "action": "generate",
        "model": args.model,
        "custom": custom,
        "instrumental": instrumental,
        "async": True,
        "title": title,
        "duration": duration,
    }
    if custom:
        payload["style"] = style
        payload["lyric"] = "[instrumental]\n[no vocals]"
        if preset.get("negative_tags"):
            payload["negative_tags"] = preset["negative_tags"]
    else:
        payload["prompt"] = prompt
        payload["instrumental"] = True if instrumental else payload["instrumental"]

    print(f"[送出] model={args.model} custom={custom} instrumental={instrumental} title={title}")
    try:
        submitted = post_json(API_URL, payload, token, 60)
        task_id = submitted.get("task_id") or submitted.get("id")
        tracks = tracks_from(submitted)
        if tracks and all(t.get("audio_url") for t in tracks):
            result = submitted
        elif task_id:
            print(f"[等待] task_id={task_id}")
            result, tracks = poll_task(task_id, token)
        else:
            sys.exit(f"[錯誤] 沒有 task_id／音檔：{json.dumps(submitted, ensure_ascii=False)[:2000]}")

        out_dir = os.path.join(TOOLS_DIR, "output", "suno")
        os.makedirs(out_dir, exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        saved = []
        for i, track in enumerate(tracks, 1):
            url = track.get("audio_url")
            if not url:
                continue
            mp3_path = os.path.join(out_dir, f"{stamp}-{i}.mp3")
            print(f"[下載] {track.get('title') or title}  {track.get('duration')}s")
            download(url, mp3_path)
            saved.append(mp3_path)
            print(f"[完成] {mp3_path}")

        if not saved:
            sys.exit("[錯誤] 沒有可下載的 audio_url")

        if install_as:
            dest = os.path.join(ASSETS_AUDIO, install_as)
            to_ogg(saved[0], dest)
            print(f"[安裝] {dest}（來源 {os.path.basename(saved[0])}；另有 {len(saved)-1} 版在 output/suno）")
    finally:
        from acedata_account import report_account
        report_account("完成")


if __name__ == "__main__":
    main()
