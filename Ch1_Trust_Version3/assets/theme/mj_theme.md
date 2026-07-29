# Version3｜主題視覺 Prompt｜`mj_theme.md`

> 用途：Ren'Py **主選單／標題畫面**主視覺（Theme）。  
> 放置路徑：`Ch1_Trust_Version3/assets/theme/title-main.png`  
> 引擎掛載點：`screens.rpy` 的 `main_menu` 已用 `optional_background("theme/title-main.png", "#17120F")`——**檔案放進來就生效，缺檔自動退回深棕純色**。  
> 風格對齊：`agents/image.md` STYLE LOCK；**背景一句**見 `agents/image_bg.md` §0.5 BG ONE-LINER；狗對齊 `agents/image_dog.md`（Option B wiry）。

---

## 1. 規格

| 項目 | 鎖定 |
|------|------|
| 尺寸 | 16:9（MJ 用 `--ar 16:9`）；落地後裁 2048×1152 |
| 構圖 | **文字區留白**：畫面中央偏下會蓋標題卡（米白 frame），主體避開中央 40% |
| 內容 | 予安×小7 的「距離感」意象；不出現可讀文字、logo、UI |
| 明度 | 中低明度、暖色；標題米白框要壓得住 |
| 禁止 | 信任數字／HUD、寫實照片感、anime 大眼、Q 版 |

## 2. MJ Prompt（直接貼）

### 方案 A｜背影同框（推薦）

```text
Thick-impasto impressionistic oil painting of quiet everyday Taiwanese residential spaces—warm amber lamp glow against cool indigo night sky; soft blended edges, tactile brush texture. Cozy nostalgic atmosphere, storybook concept-art feel.

A young Taiwanese woman in her mid-20s seen from BEHIND, sitting on the wooden floor of a cozy apartment living room at night, leaning against a navy sofa. Two steps away, a small scruffy wiry mixed-breed puppy (2 months old, honey golden-tan fur, darker brown ear tips and back ridge, cream chest and muzzle, soft semi-floppy ears) lies on its belly facing her, not yet touching. Warm lamp glow on the left, balcony window with distant city lights behind them. The empty space BETWEEN them is the emotional subject.

Composition: subjects placed in the lower-left and lower-right thirds, large soft negative space in the center for title text. No text, no logo, no watermark, no UI. Not a photograph, not anime, not chibi.
--sref https://cdn.midjourney.com/6006baad-1d97-4300-95a9-d885992b678a/0_0.png --sw 200 --stylize 180 --v 8.1 --ar 16:9
```

### 方案 B｜只有小7（安全牌，人臉不會漂）

```text
Impressionistic oil painting, thick visible brushstrokes, painterly impasto texture, soft blended edges. Warm amber lamp light, cool indigo night through a balcony window.

A small scruffy wiry Taiwanese mixed-breed puppy (2 months old, honey golden-tan, darker ear tips and back ridge, cream chest and muzzle, soft semi-floppy ears, round warm dark-brown eyes) asleep beside one plain oatmeal-gray flat shoe near an apartment doorway, a leash hanging on a wall hook above. Quiet, tender, slightly melancholic mood.

Composition: puppy in lower-right third, large soft negative space upper-left for title text. No text, no logo, no watermark. Not a photograph, not anime, not chibi.
--oref https://cdn.midjourney.com/6006baad-1d97-4300-95a9-d885992b678a/0_0.png --ow 150 --sref https://cdn.midjourney.com/6006baad-1d97-4300-95a9-d885992b678a/0_0.png --sw 200 --stylize 180 --v 8.1 --ar 16:9
```

### 方案 C｜物件靜物（極簡）

```text
Impressionistic oil painting, thick impasto brushstrokes, soft blended edges. Warm amber key light against deep indigo shadow.

Still life on a Taiwanese apartment wall: a key and a dog leash hanging side by side on two wall hooks, a faint warm lamp glow from the left, textured plaster wall. Quiet domestic intimacy, storybook concept-art feel.

Composition: hooks in the left third, large negative space right for title text. No text, no logo, no watermark. Not a photograph.
--sref https://cdn.midjourney.com/6006baad-1d97-4300-95a9-d885992b678a/0_0.png --sw 200 --stylize 180 --v 8.1 --ar 16:9
```

## 3. 現況（2026-07-25）

- **備份：** `assets/theme/_backup_20260725_132123/`（重產前 `title-main.png`／`menu-bg.png`）
- **公式：** BG ONE-LINER ＋ `mj_theme` 方案構圖 ＋ reference（`ref-living-night`、`dog-ref-canonical`、舊檔構圖）
- **`title-main.png` 已重產落地**（方案 A：予安背影左下、小7右下、中央留白），2048×1152
- **`menu-bg.png` 已重產落地**（方案 C：牆鉤掛鑰匙＋牽繩、單側暖光、大面積暗紋理留白），2048×1152  
  - 掛載：`screens.rpy` 章節選擇／結局一覽／隱藏內容／`game_menu`（存讀檔‧設定‧紀錄）→ `add "lhtl_menu_bg"`  
  - 並由 `script.rpy` 覆寫 `gui.game_menu_background`  
  - **UI 嵌入**：半透明殼（`LHTL_MENU_SHELL`）靠左；選項／存檔卡用 `LHTL_MENU_ITEM` 嵌在牆面；**右側約 25% 留給牆鉤**
  - **版面契約（2026-07-29）**：子選單用 `side "t c b"` 分標題／內容／返回；結局／隱藏列表 viewport 用 `yfill`（勿死鎖 `ymaximum 420`）；**設定頁勿在 side 中央放 `viewport`＋`yfill`**（會整頁空白）。靜態驗收：`Renpy_game/tools/validate-menus.py`、`validate-menu-layout.py`
- MJ prompt 保留作備援；換圖覆蓋同名檔即可，不用改程式
- 資料夾只放正式檔與 `mj_theme.md`；備份在 `_backup_*`

## 3.1 落地流程

```powershell
cd Ch1_Trust_Version3
# 1) Cursor GenerateImage 或 MJ 產圖
# 2) 裁 16:9 → 2048x1152 覆蓋 assets/theme/title-main.png 或 menu-bg.png
# 3) 不需改程式；screens.rpy 會自動載入
```

驗收：主選單標題米白框文字清楚可讀；圖不搶字、不出現可讀文字。

## 4. 可再延伸（同風格）

| 檔名 | 用途 | 掛載點 |
|------|------|--------|
| `theme/title-main.png` | 主選單 | 已接（`screens.rpy` main_menu） |
| `theme/menu-bg.png` | 存讀檔／設定／紀錄／章節選擇／結局一覽底圖 | 已接 |
| `theme/ending-card-{a,b,c,d}.png` | 四結局收尾卡 | 未接；結局 `centered` 前可加 |
| `gallery/secret-lap-sleep.png` | 結局 A 隱藏紀念照（中型幼犬躺大腿特寫） | 已接；結局一覽 → `secret_photo_view` |

---

*建立：2026-07-19｜主選單 Theme MJ prompt＋Ren'Py 掛載說明*  
*更新：2026-07-25｜title-main／menu-bg 依 BG ONE-LINER 重產；原圖備份於 `_backup_20260725_132123`*  
*更新：2026-07-25｜隱藏紀念照 `gallery/secret-lap-sleep.png`（僅結局 A）*  
*更新：2026-07-29｜選單版面契約（side／yfill、設定禁 nested viewport）；見 `agents/tester_menus_report.md`*
