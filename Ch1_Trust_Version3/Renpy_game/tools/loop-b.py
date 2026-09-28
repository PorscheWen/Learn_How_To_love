# -*- coding: utf-8 -*-
"""Loop B：單段 Designer 封包（無計時器、不改檔、不過 PASS/FAIL）。

抽出 section_*.md × script.rpy 該段現場，供 Agent 寫最多 5 條 D0–D2。
體感判斷不在本腳本；本腳本只列事實與 HINT。
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

TOOLS = Path(__file__).resolve().parent
RENPY = TOOLS.parent
CH1 = RENPY.parent
REPO = CH1.parent
AGENTS = CH1 / "agents"
SCRIPT = RENPY / "game" / "script.rpy"

WINDOW_HIDE_RE = re.compile(r"^\s*window hide\b", re.M)
SHOW_DOG_RE = re.compile(r"^\s*show dog (\w+)", re.M)
YUAN_SHOW_RE = re.compile(r"^\s*show yuan (\w+)", re.M)
SCENE_BG_RE = re.compile(r"^\s*scene bg (\w+)", re.M)
SHOW_SCREEN_RE = re.compile(r"^\s*show screen (\w+)", re.M)
BGM_RE = re.compile(r'play_bgm\("([^"]+)"')
SFX_RE = re.compile(r'dog_sfx\("([^"]+)"')
MENU_RE = re.compile(r"^\s*menu:", re.M)
PAUSE_RE = re.compile(r"^\s*pause\b", re.M)
TRUST_RE = re.compile(r"\btrust\s*([+\-]=|=)")
FLAG_RE = re.compile(r'flags\["([^"]+)"\]\s*=')
TICK_RE = re.compile(r"`([a-z][a-z0-9_]*)`")

# transform／場景／BGM／回憶 id，不當 pose 差集
NOT_POSE = {
    "bedroom_night",
    "office_night",
    "entrance_day",
    "alley_day",
    "char_bedroom",
    "dog_bedroom_far",
    "dog_bedroom_mid",
    "dog_bedroom_near",
    "dog_bedroom_shift",
    "dog_bedroom_nose_cu",
    "dog_sick_far",
    "dog_sick_sofa",
    "dog_cafe_near_guard",
    "sick_guard",
    "door_sleep",
    "nose_touch",
    "true",
    "false",
    "label",
    "trust",
    "flags",
    "pause",
    "menu",
    "scene",
    "show",
    "hide",
    "with",
    "far",
    "mid",
    "near",
    "shift",
    "bark",
    "soft",
    "whimper",
    "murmur",
    "tender",
    "tense",
    "xalign",
    "yalign",
    "xpos",
    "ypos",
    "zoom",
    "dissolve",
    "overlay",
    "screen",
    "transform",
    "window",
    "hide",
    "auto",
    "overlay",
    "walk",
    "far_walk",
    "behind",
}


def fail(msg: str) -> int:
    print(f"[B] FAIL {msg}", flush=True)
    return 2


def unique(seq: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def git_script_hunk_lines() -> list[int]:
    try:
        out = subprocess.check_output(
            [
                "git",
                "-C",
                str(REPO),
                "diff",
                "-U0",
                "--",
                "Ch1_Trust_Version3/Renpy_game/game/script.rpy",
            ],
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    lines: list[int] = []
    for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", out, re.M):
        start = int(m.group(1))
        count = int(m.group(2) or "1")
        lines.extend(range(start, start + max(count, 1)))
    return lines


def parse_labels(text: str) -> list[tuple[int, str, str, str]]:
    found: list[tuple[int, str, str, str]] = []
    for i, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^label (section_(\d{2})_([a-z0-9_]+)):", line)
        if m:
            found.append((i, m.group(1), m.group(2), m.group(3)))
    return found


def slice_section(text: str, nn: str) -> tuple[str, str, int, int, str] | None:
    labels = parse_labels(text)
    hits = [row for row in labels if row[2] == nn]
    if not hits:
        return None
    start_line, full, _, slug = hits[0]
    lines = text.splitlines()
    end_line = len(lines) + 1
    for row in labels:
        if row[0] > start_line:
            end_line = row[0]
            break
    body = "\n".join(lines[start_line - 1 : end_line - 1])
    return full, slug, start_line, end_line - 1, body


def find_section_md(nn: str, slug: str) -> Path | None:
    matches = sorted(AGENTS.glob(f"section_{nn}_*.md"))
    if not matches:
        return None
    for path in matches:
        if slug and slug in path.stem:
            return path
    prefer = [path for path in matches if "stairwell" not in path.stem]
    return (prefer or matches)[0]


def infer_nn(text: str) -> str | None:
    labels = parse_labels(text)
    if not labels:
        return None
    hunks = git_script_hunk_lines()
    if not hunks:
        return None
    counts: dict[str, int] = {}
    for lineno in hunks:
        current = None
        for start, _full, nn, _slug in labels:
            if start <= lineno:
                current = nn
            else:
                break
        if current:
            counts[current] = counts.get(current, 0) + 1
    if not counts:
        return None
    return max(counts, key=counts.get)


def md_pose_tokens(md: str) -> list[str]:
    tokens = []
    for match in TICK_RE.finditer(md):
        token = match.group(1)
        if token in NOT_POSE or token.startswith("bg") or token.startswith("dog_"):
            continue
        if token.startswith("char_"):
            continue
        tokens.append(token)
    return unique(tokens)


def banned_tokens(md: str) -> list[str]:
    found: list[str] = []
    for chunk in re.finditer(r"禁[^。\n]{0,120}", md):
        found.extend(TICK_RE.findall(chunk.group(0)))
    return unique([t for t in found if t not in NOT_POSE])


def silent_beat_hints(nn: str, body: str) -> list[str]:
    hints: list[str] = []
    hides = len(WINDOW_HIDE_RE.findall(body))
    if nn in {"02", "05", "06", "07", "08", "09"} and hides == 0:
        hints.append("本段稿有無字拍契約，但 script 沒有 window hide")
    if nn == "08":
        if "s08_explore" not in body:
            hints.append("S08 探路應 show s08_explore＠far_walk")
        if "s08_startle" not in body:
            hints.append("S08 機車後應 show s08_startle")
        if "s08_resist" not in body:
            hints.append("S08 機車後應 show s08_resist")
        if "leash_yank" not in body:
            hints.append("S08 被帶半步應 show yuan leash_yank")
        if "走到樹下側身蹲著" in body:
            hints.append("S08 選 A 不應再走到樹下才蹲")
        wait = body.split("把視線移開，繼續蹲著等牠自己決定下一步", 1)[-1]
        wait = wait.split("既然都出門了，拉著牠把一圈走完", 1)[0]
        if "s08_tense" not in wait:
            hints.append("S08 選 A 應先 s08_tense＠behind 再 leash_wait")
        after = body.split("轉角那邊先傳來引擎聲", 1)[-1]
        spoken = after.split("window auto", 1)[-1].split("menu:", 1)[0]
        if "前腳抬起來" in spoken or "再退半步" in spoken:
            hints.append("S08 無字拍後旁白應對齊 resist（前腳收回），勿抬腳／再退")
        dodge = body.split("轉角那邊先傳來引擎聲", 1)[-1]
        silent = dodge.split("window auto", 1)[0]
        if "window hide" in dodge and "s08_startle" not in silent:
            hints.append("S08 s08_startle 應在 window auto 前")
        if "window hide" in dodge and "s08_resist" not in silent:
            hints.append("S08 s08_resist 應在 window auto 前")
    if nn == "09" and ("s08_phone_photo" in body or "show dog shoe_sleep" in body):
        hints.append("鞋邊睡圖只在 S08 尾；S09 不要 overlay")
    return hints


def menu_echo_hints(body: str) -> list[str]:
    hints: list[str] = []
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^\s*menu:", line):
            window = "\n".join(lines[i : i + 80])
            if "show dog" not in window:
                hints.append(f"約第 {i + 1} 行起的 menu 後 80 行內沒有 show dog（可能缺選擇回聲）")
    return hints


def main() -> int:
    parser = argparse.ArgumentParser(description="Loop B：單段 Designer 封包")
    parser.add_argument("section", nargs="?", help="S07 / 7 / 07")
    args = parser.parse_args()

    if not SCRIPT.exists():
        return fail(f"找不到 {SCRIPT}")
    text = SCRIPT.read_text(encoding="utf-8")

    raw = (args.section or "").strip().upper().replace("SECTION", "").replace("S", "")
    nn = raw.zfill(2) if raw.isdigit() else None
    if nn is None:
        nn = infer_nn(text)
    if nn is None:
        print("Usage: python tools/loop-b.py S07", flush=True)
        print("[B] 請指定一段 S01～S10（不要一次掃十段）", flush=True)
        return 2
    if nn < "01" or nn > "10":
        return fail(f"段落 {nn} 超出 S01～S10")

    sliced = slice_section(text, nn)
    if not sliced:
        return fail(f"script.rpy 沒有 section_{nn}_* label")
    full, slug, start, end, body = sliced
    md_path = find_section_md(nn, slug)

    dogs = unique(SHOW_DOG_RE.findall(body))
    yuans = unique(YUAN_SHOW_RE.findall(body))
    bgs = unique(SCENE_BG_RE.findall(body))
    screens = unique(SHOW_SCREEN_RE.findall(body))
    bgms = unique(BGM_RE.findall(body))
    sfx = unique(SFX_RE.findall(body))
    menus = len(MENU_RE.findall(body))
    pauses = len(PAUSE_RE.findall(body))
    hides = len(WINDOW_HIDE_RE.findall(body))
    trusts = len(TRUST_RE.findall(body))
    flags = unique(FLAG_RE.findall(body))

    print("[B] Loop B 封包（只出事實；Agent 再寫 D0–D2，預設不改檔）", flush=True)
    print(f"[B] 段：S{nn}  label {full}  script.rpy:{start}-{end}", flush=True)
    print(f"[B] 稿：{md_path if md_path else '（找不到 section_*.md）'}", flush=True)
    print(f"[B] 統計：menu {menus}｜pause {pauses}｜window hide {hides}｜trust 寫入 {trusts}｜字數 {len(body)}", flush=True)
    print(f"[B] scene bg：{', '.join(bgs) or '—'}", flush=True)
    print(f"[B] show dog：{', '.join(dogs) or '—'}", flush=True)
    print(f"[B] show yuan：{', '.join(yuans) or '—'}", flush=True)
    print(f"[B] show screen：{', '.join(screens) or '—'}", flush=True)
    print(f"[B] BGM：{', '.join(bgms) or '—'}", flush=True)
    print(f"[B] SFX：{', '.join(sfx) or '—'}", flush=True)
    print(f"[B] flags 寫入：{', '.join(flags) or '—'}", flush=True)

    if md_path and md_path.exists():
        md = md_path.read_text(encoding="utf-8")
        table_poses = md_pose_tokens(md)
        banned = banned_tokens(md)
        missing = [
            p for p in table_poses
            if p not in dogs and p not in banned and p not in yuans
            and p not in flags and p not in bgms and p not in sfx
        ]
        extra = [p for p in dogs if p not in table_poses]
        print(f"[B] 稿 pose token：{', '.join(table_poses) or '—'}", flush=True)
        if banned:
            print(f"[B] 稿禁 pose（供對照，不是自動 FAIL）：{', '.join(banned)}", flush=True)
        if missing:
            print(f"[B] HINT 稿有、本段沒 show：{', '.join(missing)}", flush=True)
        if extra:
            print(f"[B] HINT 本段有 show、稿表未列：{', '.join(extra)}", flush=True)
        if "不新產 pose" in md or "不新產" in md:
            print("[B] HINT 本段稿鎖：優先重用 pose，不要產新 PNG", flush=True)

    for hint in silent_beat_hints(nn, body):
        print(f"[B] HINT {hint}", flush=True)
    for hint in menu_echo_hints(body):
        print(f"[B] HINT {hint}", flush=True)

    print("[B] 下一步：讀 designer.md §3.4／§6／§7，最多 5 條 D0–D2；未說「照這個改」不要改檔。", flush=True)
    print("[B] 封包完成（不是驗收綠燈）", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
