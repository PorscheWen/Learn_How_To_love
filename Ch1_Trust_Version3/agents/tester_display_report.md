# Version3 Playtest 報告｜內容與圖片顯示｜2026-09-02

- 測試者：game-tester（靜態＋引擎 smoke）
- 建置：`Ch1_Trust_Version3/Renpy_game`（commit `0e85dfe`＋工作樹 `script.rpy` 口語化未提交）
- 解析度：Ren'Py log 顯示 virtual 1280×720、physical 1920×974、DPI 150%
- 路線：全套 validate ＋資產完整性 ＋重疊靜態 ＋Ren'Py lint ＋引擎啟動 smoke

## 總評

- **Smoke：通過** — 無 P0／P1 腳本或資產失敗
- **圖片／音訊引用：138/138 檔存在**，322 個 PNG 均可 PIL 正常開啟
- **引擎啟動：正常** — script 編譯、介面、gl2 renderer 初始化無錯（`log.txt` 2026-09-02）
- **結局觸發（邏輯）**：A☑ B☑ C☑ D☑
- **本輪未做**：1280／1920 實機逐段目視、四結局手打、存讀檔回溯

最影響後續試玩的 1 件事：**口語化旁白 diff 尚未 commit**，若要對外試玩建議先提交再測。

---

## 1. 自動化結果

| 腳本 | 結果 |
|------|------|
| `validate-narration.py` | OK（1169 段；簡體 0、大陸用語 0） |
| `validate-reading-time.py` | OK（S01～S07 ≥5 分；S08～S09 ≥8 分；S10 四路 ≥5 分） |
| `validate-s01.py` | OK |
| `validate-s10.py` | OK |
| `validate-all-endings.py` | OK |
| `validate-menus.py` | OK |
| `validate-menu-layout.py` | OK |
| `validate-assets.py` | OK（66 image、54 transform、138 實體檔 0 缺檔） |
| `test-gallery-load.py` | OK（11 張畫廊＋7 紀念照＋13 隱藏文） |
| `check_overlap.py` | OK（字幕框遮蓋 0%；見 §2） |
| Ren'Py `lint` | OK（764 對話塊、81 images、31 screens） |

### 閱讀時間（最短路徑）

| 段 | 約略分鐘 | 門檻 |
|----|----------|------|
| S01 | 6.72 | ≥5 |
| S02 | 8.54 | ≥5 |
| S03 | 7.35 | ≥5 |
| S04 | 6.67 | ≥5 |
| S05 | 6.46 | ≥5 |
| S06 | 6.49 | ≥5 |
| S07 | 6.56 | ≥5 |
| S08 | 11.38 | ≥8 |
| S09 | 10.50 | ≥8 |
| S10-A～D | 5.64～5.99 | ≥5 |

---

## 2. 圖片／立繪（靜態重疊）

| 場景 | 重疊 | 字幕遮蓋 | 判定 |
|------|------|----------|------|
| S02 相遇／靠近 | 0px | 0% | OK |
| S05 耳機＋狗 | 0px | 0% | OK |
| S06 擋人＋躲腿後 | 22～27px（18%） | 0% | OK（設計內「身後」疊層） |
| S06 頂額單圖 | solo | 0% | OK |
| S08 出發／高信任 | 0px | 0% | OK |
| S09 拒絕接繩 | 22px（18%） | 0% | OK（輕微，不切臉） |
| S09 交接／玄關 | 0px | 0% | OK |
| 結局睡姿 pose | — | 0% | OK |

**立繪 pose 抽樣（前次 mismatch 修正後）：**

- S09 交接：`leash_pass` ✓
- S10 留下：`paper_bag`／`home_stand` ✓
- S06 擋人：`block` ✓
- S08 散步：`leash`＋`char_right_walk` ✓

---

## 3. 內容抽樣

| 項目 | 結果 |
|------|------|
| 四結局條件與 `game_guild` | 通過 |
| S10 不再改 trust | 通過 |
| 取名 `screen input` 契約 | 通過（靜態） |
| 無 Game Over／養死／親密％ | 通過 |
| 旁白口語化（本輪 diff） | 靜態通過；實機未逐句聽讀 |

---

## 4. 已知非阻斷（P2）

| 級 | 項目 | 說明 |
|----|------|------|
| P2 | 畫廊圖重複 | `secret-back-to-back.png` 與 `ending-a-back.png` MD5 相同（沿用舊報告） |
| P2 | S09 拒絕 pose | 人狗橫向重疊 18%，未遮字幕；可視需要交 visual-art 微調 transform |

---

## 5. 重跑指令

```powershell
cd Ch1_Trust_Version3\Renpy_game
$env:PYTHONIOENCODING="utf-8"
python tools\validate-assets.py
python tools\test-gallery-load.py
python tools\validate-narration.py
python tools\validate-reading-time.py
python tools\validate-s01.py
python tools\validate-s10.py
python tools\validate-all-endings.py
python tools\validate-menus.py
python tools\validate-menu-layout.py
cd ..
python tools\check_overlap.py
tools\renpy-sdk\renpy.exe . lint
```

實機：`Renpy_game\開啟遊戲.bat` — 建議至少目視 S02 後門、S06 走廊、S08 巷口、S09 交接、S10 四結局背景＋pose。
