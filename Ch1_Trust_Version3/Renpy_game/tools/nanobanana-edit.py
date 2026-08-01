# -*- coding: utf-8 -*-
r"""NanoBanana 圖片生成／編輯工具（AceData Cloud API）

用法範例（PowerShell，在 Renpy_game 目錄下）：

  # 編輯模式：以現有圖為底，用 prompt 改變光線／內容（保構圖）
  python tools\nanobanana-edit.py --image ..\assets\bg\bg-stairwell-night.png `
      --prompt "convert to daytime, keep composition" `
      --output ..\assets\bg\bg-stairwell-day.png

  # 純生成模式：不給 --image 即為 text-to-image
  python tools\nanobanana-edit.py --prompt "..." --output out.png --ratio 16:9

Token 讀取順序：
  1. 環境變數 ACEDATA_API_TOKEN
  2. tools\.env 內的 ACEDATA_API_TOKEN=...（此檔已被 .gitignore 排除，勿提交）
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.acedata.cloud/nano-banana/images"
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))


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


def report_balance():
    platform_token = load_env_value("ACEDATA_PLATFORM_TOKEN")
    if not platform_token:
        print("[餘額] 未設定 ACEDATA_PLATFORM_TOKEN，無法查詢剩餘積分")
        return
    req = urllib.request.Request(
        "https://platform.acedata.cloud/api/v1/applications/?user_id=me&limit=100",
        headers={"accept": "application/json",
                 "authorization": f"Bearer {platform_token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[餘額] 查詢失敗（不影響生成結果）：{e}")
        return
    items = data.get("items") or data.get("results") or []
    total = 0.0
    for app in items:
        amt = app.get("remaining_amount")
        if isinstance(amt, (int, float)):
            total += amt
    print(f"[餘額] 剩餘積分：{total:.2f} Credits（約 ${total * 0.095215:.2f} USD）")


def image_to_data_url(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def find_image_urls(data):
    """從回應 JSON 撈出圖片 URL 清單（相容多種欄位形狀）。"""
    if isinstance(data.get("image_urls"), list):
        return data["image_urls"]
    if isinstance(data.get("image_url"), str):
        return [data["image_url"]]
    d = data.get("data")
    if isinstance(d, list):
        urls = []
        for item in d:
            if isinstance(item, dict):
                u = item.get("image_url") or item.get("url")
                if u:
                    urls.append(u)
            elif isinstance(item, str):
                urls.append(item)
        if urls:
            return urls
    if isinstance(d, dict):
        return find_image_urls(d)
    return []


def main():
    ap = argparse.ArgumentParser(description="NanoBanana 圖片生成／編輯")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--image", action="append", default=[],
                    help="參考圖路徑（可重複給多張）；有給即為 edit 模式")
    ap.add_argument("--output", required=True, help="輸出 PNG 路徑")
    ap.add_argument("--model", default="nano-banana",
                    help="nano-banana / nano-banana-2 / nano-banana-pro")
    ap.add_argument("--ratio", default="", help="aspect_ratio，如 16:9（edit 預設沿用原圖）")
    ap.add_argument("--resolution", default="", help="1K / 2K / 4K")
    args = ap.parse_args()

    token = load_env_value("ACEDATA_API_TOKEN")
    if not token:
        print("錯誤：找不到 ACEDATA_API_TOKEN（環境變數或 tools\\.env）")
        sys.exit(1)

    payload = {
        "action": "edit" if args.image else "generate",
        "prompt": args.prompt,
        "model": args.model,
    }
    if args.image:
        payload["image_urls"] = [image_to_data_url(p) for p in args.image]
    if args.ratio:
        payload["aspect_ratio"] = args.ratio
    if args.resolution:
        payload["resolution"] = args.resolution

    print(f"[生成] action={payload['action']} model={args.model} 參考圖 {len(args.image)} 張 …")
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"accept": "application/json",
                 "content-type": "application/json",
                 "authorization": f"Bearer {token}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        print(f"HTTP {e.code}: {body}")
        sys.exit(1)

    urls = find_image_urls(data)
    if not urls:
        print("回應中找不到圖片 URL：")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])
        sys.exit(1)

    out = os.path.abspath(args.output)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    urllib.request.urlretrieve(urls[0], out)
    print(f"[完成] 已存檔：{out}")
    if len(urls) > 1:
        print(f"[提示] 回應共 {len(urls)} 張，其餘 URL：")
        for u in urls[1:]:
            print("  " + u)
    report_balance()


if __name__ == "__main__":
    main()
