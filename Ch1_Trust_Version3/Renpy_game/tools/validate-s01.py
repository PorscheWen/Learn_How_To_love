from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "game" / "script.rpy"
SCREENS = ROOT / "game" / "screens.rpy"


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


if not SCRIPT.exists():
    fail(f"找不到 {SCRIPT}")

text = SCRIPT.read_text(encoding="utf-8")
screens_text = SCREENS.read_text(encoding="utf-8") if SCREENS.exists() else ""
combined = text + "\n" + screens_text

required = {
    "S01 label": "label section_01_fluorescent_over_moon:",
    "S02 label": "label section_02_backdoor_glance:",
    "S03 label": "label section_03_gate_temp_border:",
    "S04 label": "label section_04_shared_quiet:",
    "S05 label": "label section_05_two_voices:",
    "S06 label": "label section_06_corridor_third_person:",
    "S07 label": "label section_07_sick_guard:",
    "S08 label": "label section_08_corner_walk:",
    "S09 label": "label section_09_almost_handoff:",
    "S10 label": "label section_10_share_the_key:",
    "default dog name": 'default dog_label = "小7"',
    "flavor flag": 'flags["peeked_backdoor"]',
    "peek choice": '"繞去看一眼":',
    "home choice": '"照原路回家":',
    "clerk hook": "小7 今天好像沒力氣跑了",
    "ending hook": "直到明天。",
    "yuan headphones": "show yuan headphones",
    "yuan commute": "show yuan commute",
    "clerk sprite": "show clerk stand",
    "S01 bgm": 'play_bgm("blank_night"',
    "S02 bgm melancholy": 'play_bgm("melancholy"',
    "S02 bgm tender": 'play_bgm("tender"',
    "S02 bgm warm": 'play_bgm("warm"',
    "slow title screen": "screen section_title(",
    "slow title transform": "transform title_slow_fade",
    "S01 title call": 'show_section_title("Section 01", "螢幕光比月亮亮")',
    "S02 title call": 'show_section_title("Section 02", "後門那一瞥")',
    "dog anxious sprite": "show dog anxious",
    "dog halfstep sprite": "show dog halfstep",
    "S02 path flag shelter": 'flags["called_shelter"] = True',
    "S02 path flag vet": 'flags["vet_first"] = True',
    "S02 path flag gate": 'flags["gate_night"] = True',
    "S02 hook line": "今晚不算數",
    "S03 title call": 'show_section_title("Section 03", "大門的臨時國界")',
    "S03 BGM": 'play_bgm("gate_border"',
    "S03 return flag": 'flags["s03_returned"] = True',
    "S03 ignore flag": 'flags["s03_ignored"] = True',
    "S03 G1 entered": 'flags["entered_home"] = True',
    "S03 G1 delayed": 'flags["delayed_entry"] = True',
    "S03 memory pose": "show dog stair_watch",
    "S03 hook pose": "show dog door_sleep",
    "S03 entrance night": "scene bg entrance_night",
    "S03 entrance day": "scene bg entrance_day",
    "S03 gate bg": "scene bg gate_night",
    "S04 title call": 'show_section_title("Section 04", "共享同一種安靜")',
    "S04 BGM": 'play_bgm("shared_quiet"',
    "S04 parallel flag": 'flags["s04_parallel"] = True',
    "S04 forced photo flag": 'flags["s04_forced_photo"] = True',
    "S04 bathroom flag": 'flags["bathroom_closed"] = True',
    "S04 parallel pose": "show dog parallel",
    "S04 memory pose": "show dog kitchen_door",
    "S04 hook line": "明天，會不會有兩種聲音",
    "S05 title call": 'show_section_title("Section 05", "你的聲音有兩種")',
    "S05 BGM": 'play_bgm("two_voices"',
    "S05 soft flag": 'flags["s05_soft_voice"] = True',
    "S05 sharp flag": 'flags["s05_sharp_voice"] = True',
    "S05 repair flag": 'flags["s05_repaired"] = True',
    "S05 fear pose": "show dog ear_flat",
    "S05 memory pose": "show dog sniff_wire",
    "S05 rename UI": 'renpy.input("想怎麼叫牠？"',
    "S06 title call": 'show_section_title("Section 06", "走廊上的第三者")',
    "S06 BGM silent start": 'renpy.music.stop(channel="music"',
    "S06 BGM after enter": 'play_bgm("tender"',
    "S06 entrance after door": "scene bg entrance_day",
    "S06 protect flag": 'flags["s06_protected"] = True',
    "S06 touch flag": 'flags["s06_allowed_touch"] = True',
    "S06 inside flag": 'flags["s06_sent_inside"] = True',
    "S06 guard pose": "show dog behind_legs",
    "S06 memory pose": "show dog forehead_nudge",
    "S06 hook line": "我們還在適應",
    "S07 title call": 'show_section_title("Section 07", "她倒下的那天")',
    "S07 BGM": 'play_bgm("sick_guard"',
    "S07 reassure flag": 'flags["s07_reassured"] = True',
    "S07 shut-out flag": 'flags["s07_shut_out"] = True',
    "S07 ajar flag": 'flags["s07_door_ajar"] = True',
    "S07 guard pose": "show dog guard_door",
    "S07 memory line": "門邊也有一種很淺的呼吸",
    "S08 title call": 'show_section_title("Section 08", "走到轉角就好")',
    "S08 BGM": 'play_bgm("corner_walk"',
    "S08 wait flag": 'flags["s08_waited"] = True',
    "S08 force flag": 'flags["s08_forced_walk"] = True',
    "S08 return flag": 'flags["s08_returned_early"] = True',
    "S08 tense pose": "show dog street_tense",
    "S08 wait pose": "show dog leash_wait",
    "S08 walk pose": "show yuan walk",
    "S08 behind pose": "dog_behind_walk",
    "S08 entrance bg": "scene bg entrance_day",
    "S08 alley bg": "scene bg alley_day",
    "S08 scooter parked": "show scooter parked",
    "S08 scooter pass": "show scooter pass",
    "S08 memory pose": "show dog shoe_sleep",
    "S08 hook line": "如果真的顧不來，我可以養",
    "Ch2 busy seed": 'flags["ch2_seed_busy_calendar"] = True',
    "Ch2 water seed": 'flags["ch2_seed_water_bowl"] = True',
    "Ch2 lease seed": 'flags["ch2_seed_lease_pet"] = True',
    "Ch2 dog origin seed": 'flags["ch2_seed_dog_no_collar"] = True',
    "Ch2 yuan family seed": 'flags["ch2_seed_yuan_family_unread"] = True',
    "Ch2 entry persist": 'persistent.ch2_from_ch1',
    "S09 title call": 'show_section_title("Section 09", "差點交給別人")',
    "S09 BGM": 'play_bgm("almost_gave"',
    "S09 stay flag": 'flags["s09_stayed"] = True',
    "S09 handover flag": 'flags["gave_away"] = True',
    "S09 refuse pose": "show dog cafe_refuse at dog_cafe_near_guard",
    "S09 entrance out": "這次開門，不是散步，是去見另一個人",
    "S10 title call": 'show_section_title("Section 10", "把鑰匙分給心跳")',
    "ending A": "label ending_ch1_back_to_back:",
    "ending B": "label ending_ch1_chosen_learning:",
    "ending C": "label ending_ch1_handed_over:",
    "ending D": "label ending_ch1_thin_ice:",
    "ending A pose": "show dog back_sleep",
    "ending B pose": "show dog check_sleep",
    "ending D pose": "show dog door_edge",
    "ending unlock A": 'process_ending_unlock("A"',
    "ending unlock B": 'process_ending_unlock("B"',
    "ending unlock C": 'process_ending_unlock("C"',
    "ending unlock D": 'process_ending_unlock("D"',
    "secret photo unlock loop": "unlock_secret_photo(_pid)",
    "secret photo lap id": '"lap_sleep"',
    "secret photo forehead id": '"forehead_nudge"',
    "secret photo water id": '"water_bowl"',
    "secret photo image": "gallery secret_lap_sleep",
    "secret forehead image": "gallery secret_forehead_nudge",
    "ending still A": "gallery ending_a_back",
    "ending gallery screen": "screen ending_gallery():",
    "ending still view": "screen ending_still_view",
    "secret photo view": "screen secret_photo_view",
    "hidden content reader": "screen hidden_content_reader",
    "dog diary unlock": 'unlock_secret_content("dog_diary_"',
    "friend perspective unlock": 'unlock_secret_content("friend_perspective_"',
    "start S07": "label start_section_07:",
    "start S08": "label start_section_08:",
    "start S09": "label start_section_09:",
    "start S10": "label start_section_10:",
    "reset clears rename": "$ proposed_name = \"\"",
}

for label, needle in required.items():
    if needle not in combined:
        fail(f"缺少 {label}: {needle}")

s01 = text.split(
    "label section_01_fluorescent_over_moon:", 1
)[1].split("label section_02_backdoor_glance:", 1)[0]

for variable in ("trust", "dist", "tone", "guard"):
    if re.search(rf"\$\s*{variable}\s*[+\-*/]?=", s01):
        fail(f"S01 不得修改 {variable}")

if s01.count('flags["peeked_backdoor"] = True') != 1:
    fail("繞看分支必須且只能寫入一次 True")

if s01.count('flags["peeked_backdoor"] = False') != 1:
    fail("原路分支必須且只能寫入一次 False")

s02 = text.split(
    "label section_02_backdoor_glance:", 1
)[1].split("label section_03_gate_temp_border:", 1)[0]

# S02 淨變動範圍 0～+2／−1：正向 trust += 1 至多三處（蹲等、良心回頭、路徑加成）
plus = len(re.findall(r"\$\s*trust\s*\+=\s*1", s02))
minus = len(re.findall(r"\$\s*trust\s*-=\s*1", s02))
if plus == 0 or minus == 0:
    fail("S02 必須同時存在升／降 trust 的分支")
if re.search(r"\$\s*trust\s*[+\-]=\s*[2-9]", s02):
    fail("S02 單次 trust 變動不得超過 1（鋸齒式累積）")

if "flags[\"peeked_backdoor\"]" not in s02:
    fail("S02 開場必須依 peeked_backdoor 呈現軟分軌")
if s02.count('flags["s02_conscience_return"] = True') != 1:
    fail("S02 趕走後良心回頭必須且只能寫入一次 s02_conscience_return=True")
if s02.count('flags["s02_conscience_return"] = False') != 2:
    fail("S02 蹲等／硬抓必須各自清除 s02_conscience_return")
if 'not flags.get("s02_conscience_return", False)' not in s02:
    fail("S02 BGM 收束必須區分良心回頭，避免 tender 被切回 melancholy")
if 'elif flags.get("s02_conscience_return", False):' not in s02:
    fail("S02 良心回頭必須有獨立的距離／喝水反應鏡頭")

s03 = text.split(
    "label section_03_gate_temp_border:", 1
)[1].split("label section_04_shared_quiet:", 1)[0]

if not re.search(r"\$\s*trust\s*\+=\s*2", s03):
    fail("S03 歸來選項必須提供 trust +2")
if not re.search(r"\$\s*trust\s*-=\s*[12]", s03):
    fail("S03 必須包含不歸來／腳趕的 trust 風險")
if "jump section_04_shared_quiet" not in s03:
    fail("S03 G1 不得卡關，所有路徑都必須進 S04")

s04 = text.split(
    "label section_04_shared_quiet:", 1
)[1].split("label section_05_two_voices:", 1)[0]

if not re.search(r"\$\s*trust\s*\+=\s*2", s04):
    fail("S04 平行安靜選項必須提供 trust +2")
if len(re.findall(r"\$\s*trust\s*-=\s*2", s04)) != 2:
    fail("S04 硬抱與關浴室都必須各有 trust -2")
if "jump section_05_two_voices" not in s04:
    fail("S04 所有軟分軌都必須進 S05")

s05 = text.split(
    "label section_05_two_voices:", 1
)[1].split("label section_06_corridor_third_person:", 1)[0]

if not re.search(r"\$\s*trust\s*\+=\s*2", s05):
    fail("S05 放慢語氣選項必須提供 trust +2")
if not re.search(r"\$\s*trust\s*-=\s*2", s05):
    fail("S05 尖聲喝止必須有 trust -2")
if "$ tone += 1" not in s05 or "$ tone -= 1" not in s05:
    fail("S05 必須同時存在 Tone 升／降")
if "jump section_06_corridor_third_person" not in s05:
    fail("S05 所有軟分軌都必須進 S06")

s06 = text.split(
    "label section_06_corridor_third_person:", 1
)[1].split("label section_07_sick_guard:", 1)[0]

if not re.search(r"\$\s*trust\s*\+=\s*2", s06):
    fail("S06 護衛選項必須提供 trust +2")
if not re.search(r"\$\s*trust\s*-=\s*2", s06):
    fail("S06 勉強讓摸必須有 trust -2")
if "$ guard += 1" not in s06 or "$ guard -= 1" not in s06:
    fail("S06 必須同時存在 Guard 升／降")
if "jump section_07_sick_guard" not in s06:
    fail("S06 所有軟分軌都必須進 S07")

s07 = text.split(
    "label section_07_sick_guard:", 1
)[1].split("label section_08_corner_walk:", 1)[0]

if not re.search(r"\$\s*trust\s*\+=\s*2", s07):
    fail("S07「我還在」必須提供 trust +2")
if not re.search(r"\$\s*trust\s*-=\s*2", s07):
    fail("S07 關到客廳必須有 trust -2")
if "$ tone += 1" not in s07 or "$ tone -= 1" not in s07:
    fail("S07 必須同時存在 Tone 升／降")
if "jump section_08_corner_walk" not in s07:
    fail("S07 所有軟分軌都必須進 S08")

s08 = text.split(
    "label section_08_corner_walk:", 1
)[1].split("label section_09_almost_handoff:", 1)[0]

if not re.search(r"\$\s*trust\s*\+=\s*2", s08):
    fail("S08 停等選項必須提供 trust +2")
if not re.search(r"\$\s*trust\s*-=\s*2", s08):
    fail("S08 硬拖選項必須有 trust -2")
if not re.search(r"\$\s*trust\s*\+=\s*1", s08):
    fail("S08 提早回家必須提供 trust +1")
if "$ dist += 1" not in s08 or "$ dist -= 1" not in s08:
    fail("S08 必須同時存在 Dist 升／降")
if "jump section_09_almost_handoff" not in s08:
    fail("S08 所有軟分軌都必須進 S09")
if "牠走了兩步又停" not in s08 or "等繩子垂回鬆弧" not in s08:
    fail("S08 中信任軟分軌必須有可見的停等與鬆弧回聲")
if "一張門邊的照片" not in s08 or "靠著鞋睡著的照片" not in s08:
    fail("S08 週一鉤子必須區分硬拖門邊照與非硬拖鞋邊睡照")

s09 = text.split(
    "label section_09_almost_handoff:", 1
)[1].split("label section_10_share_the_key:", 1)[0]

if "$ trust += 2" not in s09 or "$ trust -= 2" not in s09:
    fail("S09 留下／送走必須分別提供 trust +2／-2")
if "$ guard += 2" not in s09 or "$ guard -= 2" not in s09:
    fail("S09 留下／送走必須分別提供 Guard +2／-2")
if 'flags["gave_away"] = False' not in s09 or 'flags["gave_away"] = True' not in s09:
    fail("S09 必須完整寫入留下／送走旗標")
if "jump section_10_share_the_key" not in s09:
    fail("S09 所有硬分歧都必須進 S10")

s10 = text.split("label section_10_share_the_key:", 1)[1]
if re.search(r"\$\s*(trust|dist|tone|guard)\s*[+\-*/]?=", s10):
    fail("S10 不得再修改 trust／Dist／Tone／Guard")
for ending in (
    "ending_ch1_back_to_back",
    "ending_ch1_chosen_learning",
    "ending_ch1_handed_over",
    "ending_ch1_thin_ice",
):
    if f"jump {ending}" not in s10:
        fail(f"S10 缺少結局分流：{ending}")
if 'not flags.get("s08_forced_walk", False)' not in s10:
    fail("結局 A 必須排除 S08 硬拖路徑")
if s10.find('if flags.get("gave_away", False):') > s10.find("elif trust >= 10"):
    fail("結局 C 的 gave_away 判定必須優先於 trust 區間")

screens = (ROOT / "game" / "screens.rpy").read_text(encoding="utf-8")
_section_select = screens.split("screen section_select():", 1)[1].split("screen game_menu", 1)[0]
if "Start(entry_label)" not in _section_select:
    fail("章節選擇按鈕必須以 Start(entry_label) 啟動對應章節")
if "grid 2 5" not in _section_select:
    fail("章節選擇（S01～S10）必須用 2x5 網格一次呈現十段，不得依賴捲動")
for _n in range(1, 11):
    if f'start_section_{_n:02d}' not in _section_select:
        fail(f"章節選擇缺少 start_section_{_n:02d}")

banned = (
    "視頻", "信息", "質量", "渠道", "大陆", "打印", "硬盤", "軟件",
    "屏幕", "網絡", "智能", "激活", "默認", "數據", "文檔", "點贊",
    "靠譜", "給力", "牛逼", "曬貓", "空調",
)
for term in banned:
    if term in text:
        fail(f"偵測到非台灣用語／中國用語：{term}")

# 簡體字洩漏偵測：僅列與繁體不同碼位的簡化字，避免誤判兩體共用字。
simplified_only = (
    "们见华应时间来东车龙说话语读边过这无与专业丽万长发乐爱术样单变"
    "门问题风会众优关观学觉图员国团圆办点脑电视频质导节习际书画随开"
    "闻费脚馆闭钟处虽实样练线绍纸录"
)
leaked = sorted({c for c in text if c in simplified_only})
if leaked:
    fail(f"偵測到簡體字：{''.join(leaked)}")

print("[OK] S01～S10 結構、四結局、標題、BGM 與 trust 契約正確")
sys.exit(0)
