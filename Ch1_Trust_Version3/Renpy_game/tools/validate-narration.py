# -*- coding: utf-8 -*-
"""一次性旁白／對白紅旗掃描（game-tester）。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

GAME = Path(__file__).resolve().parents[1] / "game"

# 與繁體不同碼位的常見簡化字（避免誤判兩體共用字如「的」「一」）
SIMP_ONLY = set(
    "这说对门关时会过还从们个来开现发经长书见让给总听问飞东车头进运马买卖云点线国图语"
    "实选择为么后与并当应该种样处体气无电视机场边难备准确认际历史龙产历儿条两"
)

MAINLAND = [
    "柜台",
    "柜臺",
    "里边",
    "地铁",
    "公交车",
    "小区",
    "物业",
    "小姐姐",
    "宝子",
    "绝绝子",
    "好家伙",
    "咋了",
    "啥玩意",
]

texts: list[tuple[str, int, str]] = []
for p in sorted(GAME.glob("*.rpy")):
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        for m in re.finditer(r'"([^"]{2,})"', line):
            s = m.group(1)
            if any(ord(c) > 127 for c in s):
                texts.append((p.name, i, s))

bad_simp: list[tuple] = []
bad_mid: list[tuple] = []
bad_tri: list[tuple] = []
bad_star: list[tuple] = []
bad_ell: list[tuple] = []
bad_ta: list[tuple] = []
mainland: list[tuple] = []

for fn, ln, s in texts:
    hits = sorted({c for c in s if c in SIMP_ONLY})
    if hits:
        bad_simp.append((fn, ln, "".join(hits), s[:100]))
    if "\u00b7" in s:
        bad_mid.append((fn, ln, s[:80]))
    if "\u25b8" in s:
        bad_tri.append((fn, ln, s[:80]))
    if "\u2726" in s:
        bad_star.append((fn, ln, s[:80]))
    if re.search(r"[\u4e00-\u9fff]", s) and re.search(r"(?<!\.)\.\.\.(?!\.)", s):
        bad_ell.append((fn, ln, s[:80]))
    if re.search(r"牠 | 牠", s):
        bad_ta.append((fn, ln, s[:80]))
    for pat in MAINLAND:
        if pat in s:
            mainland.append((fn, ln, pat, s[:80]))

print(f"掃到含中文引號字串 {len(texts)} 段")
print(f"簡體碼位命中：{len(bad_simp)}")
for x in bad_simp[:50]:
    print(f"  [SIMP] {x[0]}:{x[1]} [{x[2]}] {x[3]}")
print(f"U+00B7 中點：{len(bad_mid)}｜U+25B8：{len(bad_tri)}｜U+2726：{len(bad_star)}")
for label, rows in (("MID", bad_mid), ("TRI", bad_tri), ("STAR", bad_star)):
    for x in rows[:10]:
        print(f"  [{label}] {x[0]}:{x[1]} {x[2]}")
print(f"ASCII ... 混用：{len(bad_ell)}")
for x in bad_ell[:20]:
    print(f"  [ELL] {x[0]}:{x[1]} {x[2]}")
print(f"牠 異常空格：{len(bad_ta)}")
for x in bad_ta[:10]:
    print(f"  [TA] {x[0]}:{x[1]} {x[2]}")
print(f"大陸用語：{len(mainland)}")
for x in mainland[:20]:
    print(f"  [CN] {x[0]}:{x[1]} {x[2]} {x[3]}")

fail = bool(bad_simp or bad_mid or bad_tri or bad_star or bad_ta or mainland)
# ASCII ellipsis 多為風格問題 → WARN 不擋
if fail:
    print("\n[FAIL] 旁白／對白有簡體或缺字紅旗")
    raise SystemExit(1)
print("\n[OK] 旁白／對白無簡體碼位、無缺字紅旗、無大陸用語命中")
if bad_ell:
    print(f"[WARN] {len(bad_ell)} 處 ASCII ...（建議統一 ……）")
raise SystemExit(0)
