# Tester 報告｜選單連線與版面

> 日期：2026-07-29（設定空白修正：2026-07-30）  
> 範圍：主選單、章節選擇、結局一覽、隱藏內容、存／讀檔、設定、對話紀錄、靜幀／紀念照  
> 方法：`validate-menus.py`＋`validate-menu-layout.py`＋Ren'Py lint（實機抽測建議另做）

---

## 總評

**靜態：選單出口與版面契約通過；無框溢出／返回擠壓。**  
已知修復：設定頁曾因 `viewport`＋`yfill` 嵌在 `game_menu` 的 `side` 中央而**高度歸零、整頁空白** → 已改回 `vbox`。

---

## 自動化結果

| 腳本 | 結果 |
|------|------|
| `python tools/validate-menus.py` | **OK**（出口／返回／設定無 MainMenu／章節 Start） |
| `python tools/validate-menu-layout.py` | **OK**（1280×720 框高、side／yfill、設定禁 nested viewport） |
| `renpy.exe . lint` | **OK** |

---

## 版面契約（鎖定）

| 畫面 | 契約 |
|------|------|
| 主選單 | `ymaximum 660`；「設定｜離開」`hbox` 並排 |
| 結局／隱藏 | `side "t c b"`＋viewport `yfill`；勿 `ymaximum 420`；返回安全回主選單 |
| 章節選擇 | 卡片高度使 2×5 網格落在 frame 內 |
| `game_menu` | 標題／內容／返回分區；存讀檔／設定／紀錄共用 |
| **設定** | 內容用 `vbox`；**禁止** side 中央 `viewport`＋`yfill`；`Quit`＝離開遊戲 |
| 靜幀／紀念照 | 深色底；標題 `yalign≈0.05`、關閉 `≈0.96` |

---

## 實機煙測（建議）

1. 主選單 → 結局一覽／隱藏內容／章節選擇／設定／讀檔 → 各自「返回」  
2. 設定：文字速度／音量／顯示模式可見；「離開遊戲」與「返回」分開  
3. 解鎖後點結局靜幀、紀念照 → 關閉  
4. 遊戲中 Esc／右鍵開設定 → 返回遊戲（勿被丟回標題）

---

## 重跑

```powershell
cd Ch1_Trust_Version3\Renpy_game
python tools\validate-menus.py
python tools\validate-menu-layout.py
```

對照手冊：`tester.md` §6.3.1；引擎說明：`Renpy_game/README.md`「選單 UI 契約」。
