# -*- coding: utf-8 -*-
"""Loop A：改完才驗（無計時器）。

預設跑契約核心四支；再依 --files／git 變更加資產／旁白／選單版面。
閱讀時長要顯式 --reading。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

TOOLS = Path(__file__).resolve().parent
RENPY = TOOLS.parent
CH1 = RENPY.parent
REPO = CH1.parent

CORE = [
    "validate-s01.py",
    "validate-s10.py",
    "validate-all-endings.py",
    "validate-menus.py",
]

EXTRA = {
    "assets": "validate-assets.py",
    "narration": "validate-narration.py",
    "layout": "validate-menu-layout.py",
    "reading": "validate-reading-time.py",
}


def git_names() -> list[str]:
    if not (REPO / ".git").exists() and not (REPO / ".git").is_file():
        return []
    cmds = [
        ["git", "-C", str(REPO), "diff", "--name-only"],
        ["git", "-C", str(REPO), "diff", "--cached", "--name-only"],
        ["git", "-C", str(REPO), "ls-files", "--others", "--exclude-standard"],
    ]
    names: list[str] = []
    for cmd in cmds:
        try:
            out = subprocess.check_output(cmd, text=True, encoding="utf-8", errors="replace")
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
        names.extend(line.strip().replace("\\", "/") for line in out.splitlines() if line.strip())
    return names


def extras_from_paths(paths: list[str]) -> list[str]:
    extra: list[str] = []
    for raw in paths:
        p = raw.replace("\\", "/").lower()
        name = Path(p).name.lower()
        in_ch1 = (
            "ch1_trust_version3/" in p
            or "renpy_game/" in p
            or p.startswith("game/")
            or "/assets/" in p
            or name.endswith((".rpy", ".png", ".webp", ".ogg", ".mp3", ".wav"))
        )
        if not in_ch1:
            continue
        if p.endswith("screens.rpy") or "menu" in Path(p).name.lower():
            extra.append("layout")
        if p.endswith((".rpy", ".md")) and "screen" not in Path(p).name.lower():
            extra.append("narration")
        if "/assets/" in p or p.endswith((".png", ".webp", ".jpg", ".ogg", ".mp3", ".wav")):
            extra.append("assets")
        if "image.md" in p or "image_" in Path(p).name:
            extra.append("assets")
    # 純 screens 不要硬加旁白掃描
    if extra.count("narration") and all(
        p.replace("\\", "/").lower().endswith("screens.rpy") for p in paths if p.strip()
    ) and len(paths) == 1:
        extra = [e for e in extra if e != "narration"]
    return extra


def pick_scripts(args: argparse.Namespace) -> list[str]:
    scripts = list(CORE)
    keys: list[str] = []
    if args.core_only:
        return scripts
    if args.all:
        keys.extend(["assets", "narration", "layout"])
    if args.reading:
        keys.append("reading")
    if args.assets:
        keys.append("assets")
    if args.narration:
        keys.append("narration")
    if args.layout:
        keys.append("layout")
    paths = list(args.files or [])
    if not paths and not any([args.all, args.assets, args.narration, args.layout, args.reading]):
        paths = git_names()
    keys.extend(extras_from_paths(paths))
    seen = set(scripts)
    for key in keys:
        name = EXTRA[key]
        if name not in seen:
            scripts.append(name)
            seen.add(name)
    return scripts


def run_one(name: str) -> int:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"
    print(f"\n[A] ▶ {name}", flush=True)
    proc = subprocess.run(
        [sys.executable, "-u", str(TOOLS / name)],
        cwd=str(RENPY),
        env=env,
    )
    code = proc.returncode
    print(f"[A] {'PASS' if code == 0 else 'FAIL'} {name} (exit {code})", flush=True)
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description="Loop A：改完才驗")
    parser.add_argument("--core-only", action="store_true", help="只跑契約四支")
    parser.add_argument("--all", action="store_true", help="核心＋資產／旁白／選單版面")
    parser.add_argument("--assets", action="store_true")
    parser.add_argument("--narration", action="store_true")
    parser.add_argument("--layout", action="store_true")
    parser.add_argument("--reading", action="store_true", help="另加閱讀時長（較慢）")
    parser.add_argument("--files", nargs="*", help="本次改動路徑，用來加選工具")
    args = parser.parse_args()

    scripts = pick_scripts(args)
    print("[A] Loop A 驗證（改完才驗，無計時器）", flush=True)
    print("[A] 目錄:", RENPY, flush=True)
    print("[A] 套件:", ", ".join(scripts), flush=True)

    failed: list[str] = []
    for name in scripts:
        if run_one(name) != 0:
            failed.append(name)

    print("\n[A] —— 摘要 ——", flush=True)
    if failed:
        print("[A] FAIL:", ", ".join(failed), flush=True)
        return 1
    print("[A] 全綠", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
