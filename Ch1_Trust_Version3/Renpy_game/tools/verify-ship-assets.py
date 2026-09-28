#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""確認發行資產在 game/ 內且非 build.classify 排除路徑。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"

SAMPLES = (
    "images/bg/bg-living-night.png",
    "images/dog/dog-anxious.png",
    "images/char/char-yuan-headphones.png",
    "images/gallery/ending-a-back.png",
    "images/theme/menu-bg.png",
    "audio/calm.ogg",
    "audio/sfx/puppy-whimper-a.wav",
    "window-icon.png",
    "OFL.txt",
    "SourceHanSansLite.ttf",
)

missing = [rel for rel in SAMPLES if not (GAME / rel).is_file()]
if missing:
    print("[FAIL] missing:", ", ".join(missing))
    raise SystemExit(1)

options = (GAME / "options.rpy").read_text(encoding="utf-8")
if "config.searchpath.append" in options:
    print("[FAIL] options.rpy still uses external searchpath")
    raise SystemExit(1)

print("[OK] ship sample assets present in game/ ({})".format(len(SAMPLES)))
raise SystemExit(0)
