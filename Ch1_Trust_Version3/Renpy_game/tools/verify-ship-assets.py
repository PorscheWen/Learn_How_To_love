#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""確認所有腳本引用的資產都在 game/ 內（發行包不可依賴 Version3/assets）。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"

RPY = "\n".join(p.read_text(encoding="utf-8") for p in sorted(GAME.glob("*.rpy")))
SCRIPT = (GAME / "script.rpy").read_text(encoding="utf-8")
SCREENS = (GAME / "screens.rpy").read_text(encoding="utf-8")


def loadable(rel: str) -> bool:
    if "%" in rel:
        return True
    return (GAME / rel).is_file() or (GAME / "images" / rel).is_file()


def collect_ref_paths() -> set[str]:
    paths: set[str] = set()
    for pat in (
        r'optional_background\(\s*\n?\s*"([^"]+)"',
        r'optional_displayable\(\s*\n?\s*"([^"]+)"',
        r'dog_sprite\("([^"]+)"',
        r'char_sprite\("([^"]+)"',
        r'"((?:audio|gallery|theme|bg|dog|char|prop)/[^"]+\.(?:png|jpg|webp|ogg|wav|mp3|flac))"',
    ):
        paths.update(re.findall(pat, RPY))
        paths.update(re.findall(pat, SCREENS))
    for m in re.finditer(r'"((?:dog|char)/[^"]+\.png)"\s*:', SCRIPT):
        paths.add(m.group(1))
    anim_poses = re.findall(
        r'"((?:door-sleep|back-sleep|check-sleep|door-edge|sniff-wire|drink-bowl|farewell|guard-door))"\s*:\s*[\d.]+',
        SCRIPT,
    )
    for pose in anim_poses:
        for i in range(1, 6):
            paths.add(f"dog/{pose}/dog-{pose}-{i:02d}.png")
    for i in range(1, 6):
        paths.add(f"dog/wag/dog-wag-{i:02d}.png")
    if m := re.search(r'define config\.main_menu_music = "([^"]+)"', RPY):
        paths.add(m.group(1))
    if m := re.search(r'define config\.window_icon = "([^"]+)"', RPY):
        paths.add(m.group(1))
    paths.add("SourceHanSansLite.ttf")
    paths.add("OFL.txt")
    alias_block = SCRIPT.split("aliases = {", 1)[1].split("}", 1)[0]
    for m in re.finditer(r'\("([^"]+\.ogg)"', alias_block):
        paths.add(m.group(1))
    paths.add("audio/tense.ogg")
    paths.add("audio/tense-2.ogg")
    return paths


def main() -> int:
    options = (GAME / "options.rpy").read_text(encoding="utf-8")
    if "config.searchpath.append" in options:
        print("[FAIL] options.rpy still uses external searchpath")
        return 1

    missing = sorted(rel for rel in collect_ref_paths() if not loadable(rel))
    if missing:
        print(f"[FAIL] {len(missing)} referenced asset(s) missing under game/:")
        for rel in missing[:40]:
            print(f"  - {rel}")
        if len(missing) > 40:
            print(f"  … and {len(missing) - 40} more")
        return 1

    print(f"[OK] all {len(collect_ref_paths())} referenced ship paths present in game/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
