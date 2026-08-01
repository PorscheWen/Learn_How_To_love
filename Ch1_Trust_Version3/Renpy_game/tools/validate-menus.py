# -*- coding: utf-8 -*-
"""選單連線靜態驗收：主選單／子頁／返回／禁開新遊戲的 action。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREENS = (ROOT / "game" / "screens.rpy").read_text(encoding="utf-8")
SCRIPT = (ROOT / "game" / "script.rpy").read_text(encoding="utf-8")

fails: list[str] = []


def fail(msg: str) -> None:
    fails.append(msg)
    print(f"[FAIL] {msg}")


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def screen_body(name: str) -> str:
    m = re.search(rf"^screen {name}\(.*?\):(.*?)(?=^screen |\Z)", SCREENS, re.M | re.S)
    if not m:
        fail(f"缺少 screen {name}")
        return ""
    return m.group(1)


# --- 必要畫面存在 ---
required = [
    "main_menu",
    "section_select",
    "ending_gallery",
    "hidden_content_gallery",
    "preferences",
    "save",
    "load",
    "history",
    "game_menu",
]
for name in required:
    if f"screen {name}" not in SCREENS and f"screen {name}(" not in SCREENS:
        fail(f"缺 screen {name}")
ok("必要選單畫面齊全")

# --- 主選單出口 ---
mm = screen_body("main_menu")
expected_actions = {
    "開始": r'action Start\(\)',
    "讀取進度": r'ShowMenu\("load"\)',
    "章節選擇": r'ShowMenu\("section_select"\)',
    "結局一覽": r'ShowMenu\("ending_gallery"\)',
    "隱藏內容": r'ShowMenu\("hidden_content_gallery"\)',
    "設定": r'ShowMenu\("preferences"\)',
    "離開": r"Quit\(",
}
for label, pat in expected_actions.items():
    if label not in mm or not re.search(pat, mm):
        fail(f"主選單「{label}」連線異常")
if "Function(sync_unlocked_ending_rewards)" in mm:
    fail("主選單仍把 sync Function 放進 action 清單（會誤開新遊戲）")
ok("主選單七個出口連線正確")

# --- sync 必須回傳 None ---
if "def sync_unlocked_ending_rewards" not in SCRIPT:
    fail("缺 sync_unlocked_ending_rewards")
else:
    fn = SCRIPT.split("def sync_unlocked_ending_rewards", 1)[1].split("\n    def ", 1)[0]
    if "return True" in fn:
        fail("sync_unlocked_ending_rewards 仍 return True（主選單會重開）")
    if "return None" not in fn:
        fail("sync_unlocked_ending_rewards 應明確 return None")
    else:
        ok("sync 回傳 None（不干擾主選單）")

# --- 子頁返回 ---
eg = screen_body("ending_gallery")
hg = screen_body("hidden_content_gallery")
ss = screen_body("section_select")
## Return() 標準行為：主選單開啟時回主選單、遊戲中回遊戲，皆安全
for name, body in (
    ("ending_gallery", eg),
    ("hidden_content_gallery", hg),
):
    if (
        "action Return()" not in body
        and 'ShowMenu("main_menu")' not in body
        and "If(main_menu" not in body
    ):
        fail(f"{name} 返回未處理主選單情境")
    if re.search(r'action\s+MainMenu\(\)', body):
        fail(f"{name} 不應使用 MainMenu() 當返回")
ok("結局一覽／隱藏內容返回安全")

if (
    "action Return()" not in ss
    and 'ShowMenu("main_menu")' not in ss
    and "If(main_menu" not in ss
):
    fail("section_select 返回未連回主選單")
else:
    ok("章節選擇可返回主選單")

# --- 設定頁禁 MainMenu；應有離開遊戲 ---
pref = screen_body("preferences")
if re.search(r"action\s+MainMenu\(\)", pref):
    fail("preferences 內有 MainMenu()：遊戲中開設定會被丟回標題")
if "use game_menu" not in pref:
    fail("preferences 未套用 game_menu（缺統一返回）")
## 離開遊戲：設定頁自帶 Quit，或委派 game_menu(show_quit=True) 顯示
gm_body = screen_body("game_menu")
has_quit = "Quit(" in pref or ("show_quit=True" in pref and "Quit(" in gm_body)
if not has_quit:
    fail("preferences 缺離開遊戲 Quit")
elif 'text "輔助需求"' not in pref:
    fail("preferences 缺輔助需求")
elif "enable_assist_pack" not in pref:
    fail("preferences 缺開啟輔助組合")
else:
    ok("設定頁無 MainMenu，有離開遊戲／game_menu Return／輔助需求")

gm = screen_body("game_menu")
if "action Return()" not in gm:
    fail("game_menu 缺 Return()")
else:
    ok("存讀檔／設定／紀錄共用 game_menu Return")

# --- aftercare 選單 ---
if "label ending_aftercare:" not in SCRIPT:
    fail("缺 ending_aftercare")
else:
    ac = SCRIPT.split("label ending_aftercare:", 1)[1][:2500]
    for need in (
        'call screen ending_gallery',
        'call screen hidden_content_gallery',
        'jump ending_aftercare',
        'jump start_section_09',
        'jump start',
    ):
        if need not in ac:
            fail(f"aftercare 缺 {need}")
    ok("aftercare 結局／隱藏／重玩出口齊全")

# --- 章節 Start 標籤存在 ---
labels = re.findall(r'\("start_section_\d+",', ss)
for i in range(1, 11):
    lab = f"start_section_{i:02d}"
    if f'("{lab}"' not in ss:
        fail(f"章節選擇缺 {lab}")
    if f"label {lab}:" not in SCRIPT:
        fail(f"script 缺 label {lab}")
ok("章節選擇 S01～S10 Start 標籤對得上")

if fails:
    print(f"\n共 {len(fails)} 項 FAIL")
    raise SystemExit(1)
print("\n[OK] 選單連線靜態驗收全部通過")
raise SystemExit(0)
