# -*- coding: utf-8 -*-
"""四結局完整靜態煙測（tester：路由／coda／解鎖對齊／aftercare）"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (ROOT / "game" / "script.rpy").read_text(encoding="utf-8")
ENDINGS = (ROOT / "game" / "endings.rpy").read_text(encoding="utf-8")
SCREENS = (ROOT / "game" / "screens.rpy").read_text(encoding="utf-8")
HIDDEN = ""
hc = ROOT / "game" / "hidden_content.rpy"
if hc.exists():
    HIDDEN = hc.read_text(encoding="utf-8")

fails: list[str] = []


def fail(msg: str) -> None:
    fails.append(msg)
    print(f"[FAIL] {msg}")


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def simulate(trust: int, gave: bool, forced: bool) -> str:
    if gave:
        return "C"
    if trust >= 10 and not forced:
        return "A"
    if trust >= 4:
        return "B"
    return "D"


# --- 路由 ---
cases = [
    (12, False, False, "A"),
    (10, False, False, "A"),
    (12, False, True, "B"),
    (9, False, False, "B"),
    (4, False, False, "B"),
    (3, False, False, "D"),
    (0, False, False, "D"),
    (12, True, False, "C"),
    (0, True, True, "C"),
]
for trust, gave, forced, expect in cases:
    got = simulate(trust, gave, forced)
    if got != expect:
        fail(f"路由 trust={trust} gave={gave} forced={forced} → {got}≠{expect}")
if not any(f.startswith("路由") for f in fails):
    ok("路由真值表（9 案）")

# --- 四結局落地鏈 ---
meta = {
    "A": ("ending_ch1_back_to_back", "back_to_back", "ending_beat_back_to_back"),
    "B": ("ending_ch1_chosen_learning", "chosen_learning", "ending_beat_chosen_learning"),
    "C": ("ending_ch1_handed_over", "handed_over", "ending_beat_handed_over"),
    "D": ("ending_ch1_thin_ice", "thin_ice", "ending_beat_thin_ice"),
}
for eid, (label, flag, beat) in meta.items():
    if f"label {label}:" not in SCRIPT:
        fail(f"缺 {label}")
        continue
    if f'flags["ch1_ending"] = "{flag}"' not in SCRIPT:
        fail(f"{eid} 未寫 ch1_ending={flag}")
    if f'process_ending_unlock("{eid}"' not in SCRIPT:
        fail(f"{eid} 未 process_ending_unlock")
    if "record_trust_trajectory()" not in SCRIPT.split(f"label {label}:", 1)[1][:800]:
        fail(f"{eid} 開頭未 record_trust_trajectory")
    if f'call ending_coda_finish("{eid}"' not in SCRIPT:
        fail(f"{eid} 未接 coda")
    if f"label {beat}:" not in ENDINGS:
        fail(f"缺節拍 {beat}")
ok("四結局 label／unlock／trajectory／coda／beat")

# --- 睡姿契約 ---
if "show dog back_sleep at dog_near" not in SCRIPT:
    fail("A 缺 back_sleep@near")
if "show dog check_sleep at dog_mid" not in SCRIPT:
    fail("B 缺 check_sleep@mid")
if "show dog door_edge at dog_far" not in SCRIPT:
    fail("D 缺 door_edge@far")
c_label = SCRIPT.split("label ending_ch1_handed_over:", 1)[1].split(
    "label ending_ch1_thin_ice:", 1
)[0]
if re.search(r"^\s*show dog\b", c_label, re.M):
    fail("C 敘事不應 show dog")
c_beat = ENDINGS.split("label ending_beat_handed_over:", 1)[1].split("label ", 1)[0]
if re.search(r"^\s*show dog\b", c_beat, re.M):
    fail("C 節拍不應 show dog")
ok("睡姿／C 空屋契約")

# --- 解鎖：process vs hidden_content 目錄 vs 提示文案 ---
if 'unlock_secret_content("dog_diary_" + eid.lower())' not in SCRIPT:
    fail("process 未解鎖 dog_diary_*")
if 'unlock_secret_content("character_aftercare_" + eid.lower())' not in SCRIPT:
    fail("process 未解鎖 character_aftercare_*")
if 'unlock_secret_content("friend_perspective_" + eid.lower())' not in SCRIPT:
    fail("process 未解鎖 friend_perspective_*")
if 'unlock_secret_photo("lap_sleep")' not in SCRIPT and "unlock_secret_photo(_pid)" not in SCRIPT:
    fail("A 未解鎖紀念照")
if 'unlock_secret_photo("back_to_back")' in SCRIPT:
    fail("A 不應再解鎖 back_to_back 紀念照")
if "forehead_nudge" not in SCRIPT or "water_bowl" not in SCRIPT:
    fail("A 應解鎖新紀念照 id（forehead_nudge／water_bowl 等）")

order = re.findall(r'"(dog_diary_[abcd]|character_aftercare_[abcd]|friend_perspective_[abcd])"', HIDDEN)
need = []
for eid in "abcd":
    need += [f"dog_diary_{eid}", f"character_aftercare_{eid}", f"friend_perspective_{eid}"]
missing_order = [x for x in need if x not in order]
if missing_order:
    fail(f"HIDDEN_CONTENT_ORDER 缺 {missing_order}")
else:
    ok("hidden_content 12 篇目錄齊")

# 提示文案關鍵詞（不對假 id，只查玩家可見宣稱是否合理）
for eid, words in {
    "A": ["狗的日記", "予安心境", "朋友視角", "紀念照片"],
    "B": ["狗的日記", "予安心境", "朋友視角"],
    "C": ["狗的日記", "予安心境", "朋友視角"],
    "D": ["狗的日記", "予安心境", "朋友視角"],
}.items():
    # 在 ending_unlock_lines 的對應分支找
    fn = ENDINGS.split("def ending_unlock_lines", 1)[1].split("\ndef ", 1)[0]
    # 粗切：找 eid == "X" 到下一個 elif/return
    chunk_m = re.search(
        rf'eid == "{eid}":(.*?)(?=elif eid|return lines)', fn, re.S
    )
    chunk = chunk_m.group(1) if chunk_m else ""
    for w in words:
        if w not in chunk:
            fail(f"結局{eid} 解鎖提示缺「{w}」")
ok("解鎖提示文案與三層內容對齊")

# --- gallery 結局靜幀 ---
for name in (
    "gallery ending_a_back",
    "gallery ending_b_learning",
    "gallery ending_c_handover",
    "gallery ending_d_thin_ice",
):
    if name not in SCRIPT and name not in SCREENS:
        fail(f"缺結局靜幀 image {name}")
if "ending_still_view" not in SCREENS:
    fail("缺 ending_still_view screen")
else:
    ok("結局一覽靜幀 viewer")

# --- aftercare ---
if "label ending_aftercare:" not in SCRIPT:
    fail("缺 ending_aftercare")
ac = SCRIPT.split("label ending_aftercare:", 1)[1][:2000]
for key in ("back_to_back", "chosen_learning", "handed_over"):
    if key not in ac:
        fail(f"aftercare 缺 {key} 分支風味")
ok("aftercare 存在且有結局風味")
if "label ending_aftercare_menu:" not in SCRIPT:
    fail("缺 ending_aftercare_menu")
if SCRIPT.split("label ending_aftercare_menu:", 1)[1][:800].count("jump ending_aftercare\n") > 0:
    fail("aftercare 選單仍跳回評語（應 jump ending_aftercare_menu）")

# --- 防呆 ---
if "list(persistent.unlocked_secret_content or [])" not in SCRIPT:
    fail("unlock_secret_content 未防 None")
if "time.time()" not in SCRIPT:
    fail("trajectory 未用 time.time()")
if "default persistent.unlocked_secret_content" not in SCRIPT:
    fail("缺 default unlocked_secret_content")
ok("persistent／timestamp 防呆")

# --- 禁止詞 ---
end_bodies = SCRIPT.split("label ending_ch1_back_to_back:", 1)[1]
for term in ("安樂", "衰老", "Game Over", "親密％", "親密%"):
    if term in end_bodies:
        fail(f"結局區出現禁止詞 {term}")
ok("無禁止詞")

if fails:
    print(f"\n共 {len(fails)} 項 FAIL")
    raise SystemExit(1)
print("\n[OK] 四結局完整煙測通過")
raise SystemExit(0)
