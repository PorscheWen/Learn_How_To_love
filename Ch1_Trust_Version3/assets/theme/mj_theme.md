# Version3｜主題視覺 Prompt｜`mj_theme.md`

> 用途：Ren'Py **主選單／標題畫面**主視覺（Theme）。  
> 放置路徑：`Ch1_Trust_Version3/assets/theme/title-main.png`  
> 引擎掛載點：`screens.rpy` 的 `main_menu` 已用 `optional_background("theme/title-main.png", "#17120F")`——**檔案放進來就生效，缺檔自動退回深棕純色**。  
> 風格對齊：`agents/image.md` STYLE LOCK；狗對齊 `agents/image_dog.md`（Option B wiry）。

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
Impressionistic oil painting, thick visible brushstrokes, painterly impasto texture, soft blended edges, subtle canvas tooth. Warm amber and golden interior light contrasting cool deep indigo night exterior. Cozy nostalgic quiet everyday Taiwanese atmosphere, storybook concept-art feel.

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

## 3. 現況（2026-07-19）

- **`title-main.png` 已由 Cursor `GenerateImage` 產出落地**（方案 A 構圖：予安背影左下、小7右下、中央暖光留白），2048×1152。
- **`menu-bg.png` 已由 Cursor 產出落地**（方案 C 意象：暗牆＋右側牆鉤掛鑰匙與牽繩、單側暖光，中央近抽象暗紋理），2048×1152；墊在存讀檔／設定／紀錄／章節選擇底下。
- MJ prompt 保留作重產備援；換圖時直接覆蓋同名檔即可，不用改程式。
- 資料夾只放正式檔，不留 `*-src` 中介圖。

## 3.1 落地流程

```powershell
cd Ch1_Trust_Version3
# 1) MJ 產圖後把原檔存 assets/theme/title-main-src.png
# 2) 裁 16:9 → 2048x1152 存 assets/theme/title-main.png（可用 PIL，同 bg 流程）
# 3) 不需改程式；main_menu 會自動載入
```

驗收：主選單標題米白框文字清楚可讀；圖不搶字、不出現可讀文字。

## 4. 可再延伸（同風格）

| 檔名 | 用途 | 掛載點 |
|------|------|--------|
| `theme/title-main.png` | 主選單 | 已接（`screens.rpy` main_menu） |
| `theme/menu-bg.png` | 存讀檔／設定／紀錄／章節選擇底圖 | 已接（`game_menu`、`section_select`） |
| `theme/ending-card-{a,b,c,d}.png` | 四結局收尾卡 | 未接；結局 `centered` 前可加 |

---

*建立：2026-07-19｜主選單 Theme MJ prompt＋Ren'Py 掛載說明*
