# Tester 報告｜全線圖片＋旁白驗收

> 日期：2026-08-02  
> 角色：game-tester（台灣玩家視角）  
> 範圍：S01～S10＋四結局＋選單／畫廊；**圖片引用**與**旁白／對白／選項**  
> 方法：靜態自動化（未開實機）

---

## 總評

**通過。** 圖片引用與實體檔全數存在；旁白／對白無簡體碼位、無 SourceHanSansLite 缺字紅旗、無大陸用語命中。

本次另修 1 項 **P1**（結局解鎖列表項目符號缺字）。

---

## 1. 圖片／資產

| 檢查 | 結果 |
|------|------|
| scene/show 引用 61 個 image 有定義 | OK |
| at 引用 48 個 transform 有定義 | OK |
| `play_bgm` 18／`dog_sfx` 6 | OK |
| 引用實體檔 134/134 存在 | OK |
| gallery 紀念照 7＋結局靜幀 4 | OK |
| 狗動畫幀 wag／door-sleep／back-sleep／check-sleep／door-edge／sniff-wire／guard-door／drink-bowl／farewell（各 5） | OK |
| `bg-stairwell-day`／`bg-stairwell-night` 存在且同構圖契約（左門／右電梯） | OK |
| S03 `dog_far_stair` → `xalign 0.22`（靠左側門） | OK |
| S06 `scene bg stairwell_day` | OK |

`scene bg` 使用分布（節錄）：`stairwell_night`×5（S03）、`stairwell_day`×1（S06）、其餘 living／entrance／gate／alley／cafe 皆有對應檔。

---

## 2. 旁白／對白／選項

掃描：`game/*.rpy` 含中文引號字串 **1104** 段（`tools/validate-narration.py`）

| 紅旗 | 命中 |
|------|------|
| 簡體碼位（常見簡繁異形字） | **0** |
| U+00B7 中點／U+25B8／U+2726（字型缺字） | **0**（修後） |
| `牠 ` 異常空格 | **0** |
| 大陸用語抽樣（柜台／地铁／小区…） | **0** |
| ASCII `...` 混用 | **0** |

### 本次修正（P1）

| 位置 | 現象 | 處理 |
|------|------|------|
| `endings.rpy` 結局解鎖列表前綴 | `·`（U+00B7）SourceHanSansLite **缺字** → 可能顯示方框 | 改為 `・`（U+30FB） |

---

## 3. 章節／選單／時長（回歸）

| 腳本 | 結果 |
|------|------|
| `validate-s01.py` | OK |
| `validate-s10.py` | OK |
| `validate-all-endings.py` | OK |
| `validate-reading-time.py`（S01～S07≥5；S08／S09≥8；S10 各結局≥5） | OK |
| `validate-menus.py` | OK |
| `validate-menu-layout.py` | OK（需 `PYTHONIOENCODING=utf-8` 於 cp950 主控台） |

---

## 4. 已知非阻斷（P2）

- `gallery/secret-back-to-back.png` 與 `gallery/ending-a-back.png` **MD5 相同**（紀念照與結局 A 靜幀重複）→ 交 visual-art 另產一張更佳。
- 實機肉眼：字幕與狗疊層、S03 門邊站位微調，仍建議抽測一輪（靜態無法替代）。

---

## 5. 重跑指令

```powershell
cd Ch1_Trust_Version3\Renpy_game
$env:PYTHONIOENCODING='utf-8'
python tools\validate-assets.py
python tools\validate-narration.py
python tools\test-gallery-load.py
python tools\validate-s01.py
python tools\validate-s10.py
python tools\validate-all-endings.py
python tools\validate-reading-time.py
python tools\validate-menus.py
python tools\validate-menu-layout.py
```

---

*game-tester｜2026-08-02｜圖片＋旁白靜態驗收通過*
