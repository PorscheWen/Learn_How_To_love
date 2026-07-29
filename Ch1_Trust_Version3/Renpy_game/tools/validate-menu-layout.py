# -*- coding: utf-8 -*-
"""選單版面靜態驗收（1280×720）：框尺寸、網格是否超出、side 是否 yfill、禁固定 ymaximum 擠返回。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / "game" / "screens.rpy").read_text(encoding="utf-8")

W, H = 1280, 720
fails: list[str] = []


def fail(msg: str) -> None:
    fails.append(msg)
    print(f"[FAIL] {msg}")


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def screen_body(name: str) -> str:
    m = re.search(rf"^screen {name}\(.*?\):(.*?)(?=^screen |\Z)", TEXT, re.M | re.S)
    return m.group(1) if m else ""


def frame_metrics(body: str) -> list[tuple[int | None, int | None]]:
    """粗抓 xsize／ysize。"""
    out = []
    for m in re.finditer(
        r"frame:\s*((?:(?!\n\s*(?:screen |frame:|viewport:|vbox:|hbox:|side |grid |textbutton )).|\n)*?)(?=\n\s*(?:viewport:|vbox:|hbox:|side |grid |textbutton |text |\Z))",
        body,
        re.S,
    ):
        chunk = m.group(0)
        xs = re.search(r"xsize\s+(\d+)", chunk)
        ys = re.search(r"ysize\s+(\d+)", chunk)
        if xs or ys:
            out.append((int(xs.group(1)) if xs else None, int(ys.group(1)) if ys else None))
    return out


# --- 主選單：須有離開、設定並排 ---
mm = screen_body("main_menu")
if 'textbutton "離開"' not in mm or "Quit(" not in mm:
    fail("主選單缺少離開")
if "hbox:" not in mm or 'textbutton "設定"' not in mm:
    fail("主選單設定／離開應並排 hbox")
if "ymaximum 660" not in mm:
    fail("主選單缺 ymaximum 防護")
ok("主選單：離開可見、高度防護")

# --- 結局／隱藏：side yfill + viewport yfill，禁死 ymaximum 420 ---
for name in ("ending_gallery", "hidden_content_gallery"):
    body = screen_body(name)
    if "yfill True" not in body:
        fail(f"{name} 缺 yfill（返回易被擠）")
    if re.search(r"ymaximum\s+420", body):
        fail(f"{name} 仍用 ymaximum 420（會與返回重疊）")
    metrics = frame_metrics(body)
    for xs, ys in metrics:
        if xs and xs > W:
            fail(f"{name} frame xsize {xs} > {W}")
        if ys and ys > H - 40:
            fail(f"{name} frame ysize {ys} 幾乎滿高，易裁切")
    ok(f"{name}：side／viewport 可伸縮，框在螢幕內")

# --- 章節：網格高度估算 ---
ss = screen_body("section_select")
ysize_m = re.search(r"ysize\s+(\d+)", ss)
card_m = re.search(r"ysize\s+(\d+)", ss[ss.find("grid") :]) if "grid" in ss else None
spacing_m = re.search(r"grid 2 5:.*?spacing\s+(\d+)", ss, re.S)
if not ysize_m or not card_m:
    fail("章節選擇缺 frame／卡片 ysize")
else:
    frame_h = int(ysize_m.group(1))
    card_h = int(card_m.group(1))
    gap = int(spacing_m.group(1)) if spacing_m else 8
    grid_h = 5 * card_h + 4 * gap
    # 預留標題+返回+padding ≈ 140
    if grid_h + 140 > frame_h:
        fail(f"章節網格高 {grid_h}+140 > frame {frame_h}（會壓返回）")
    else:
        ok(f"章節選擇：網格 {grid_h}px + 邊距 ≤ frame {frame_h}")

# --- 存檔格 ---
fs = screen_body("file_slots")
slot_w = int(re.search(r"xsize\s+(\d+)", fs).group(1))
slot_h = int(re.search(r"ysize\s+(\d+)", fs).group(1))
gap = int(re.search(r"spacing\s+(\d+)", fs).group(1))
grid_w = 3 * slot_w + 2 * gap
grid_h = 2 * slot_h + gap
# game_menu 內容區約 900×450
if grid_w > 900:
    fail(f"存檔格寬 {grid_w} > 內容區 900")
if grid_h > 480:
    fail(f"存檔格高 {grid_h} > 內容區 480")
ok(f"存讀檔格：{grid_w}×{grid_h} 落在 game_menu 內容區")

# --- 設定：禁止 nested viewport+yfill（高度變 0 整頁空白）；無 MainMenu ---
pref = screen_body("preferences")
if re.search(r"viewport:\s*\n(?:[ \t].*\n)*?[ \t]+yfill True", pref):
    fail("設定頁勿用 viewport+yfill（嵌 game_menu side 會高度歸零）")
if re.search(r"yalign\s+0\.\d+", pref):
    fail("設定頁內容仍用 yalign 推位（易疊到標題／返回）")
if "MainMenu(" in pref:
    fail("設定頁仍有 MainMenu()")
if "Quit(" not in pref:
    fail("設定頁缺離開遊戲")
if 'text "文字速度"' not in pref or 'text "音樂音量"' not in pref:
    fail("設定頁缺主要控制項")
ok("設定頁：內容可見、無推位重疊、可離開")

# --- 靜幀／照片：標題頂、關閉底 ---
for name in ("ending_still_view", "secret_photo_view"):
    body = screen_body(name)
    if "yalign 0.05" not in body and "yalign 0.06" not in body:
        fail(f"{name} 標題未置頂")
    if "yalign 0.96" not in body and "yalign 0.94" not in body:
        fail(f"{name} 關閉鈕未置底")
    if 'action Hide("' not in body:
        fail(f"{name} 缺關閉")
ok("靜幀／紀念照：標題與關閉分離")

# --- game_menu 結構 ---
gm = screen_body("game_menu")
if 'side "t c b"' not in gm:
    fail("game_menu 缺 t/c/b 分區")
if "yfill True" not in gm:
    fail("game_menu 缺 yfill")
if "action Return()" not in gm:
    fail("game_menu 缺 Return")
ok("game_menu：標題／內容／返回分區")

# --- tag menu 互斥（同時只顯示一個主選單頁）---
tagged = re.findall(r"^screen (\w+).*?:\n\s+tag menu", TEXT, re.M)
need_tag = [
    "main_menu",
    "ending_gallery",
    "hidden_content_gallery",
    "section_select",
    "save",
    "load",
    "preferences",
    "history",
    "game_menu",
]
for n in need_tag:
    body = screen_body(n)
    # save/load use game_menu which has tag; they also have tag menu
    if "tag menu" not in body and n not in ("game_menu",):
        # save/load have tag menu on themselves
        if n in ("save", "load", "preferences", "history") and "tag menu" not in body:
            fail(f"{n} 缺 tag menu（可能與其他選單疊層）")
ok(f"選單 tag menu 覆蓋檢查（{len(tagged)} 個 tagged screen）")

if fails:
    print(f"\n共 {len(fails)} 項 FAIL")
    raise SystemExit(1)
print("\n[OK] 選單版面靜態驗收通過（無框溢出／返回擠壓／設定重疊）")
raise SystemExit(0)
