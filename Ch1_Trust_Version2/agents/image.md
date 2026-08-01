# Version2 美術生圖規範｜FLUX 2 Pro via Nous Portal

> 對齊：`00_core_settings.md` · `03_character_bible.md` · `plot.md`  
> 端點／金鑰：[`../Nous_Portal.md`](../Nous_Portal.md)（與 `Ch1_Trust/Nous_Portal.md` 同源）  
> 模型鎖定：**FLUX 2 Pro**（`fal-ai/flux-2-pro`）  
> **背景命名／家族：** [`image_bg.md`](image_bg.md)（`bg-{place}-{light}`；同 place 共用基準只改日夜）  
> 用途：Agent／Portal 一鍵 job 組 prompt、產背景與角色圖；**不要**用 Cursor `GenerateImage` 當定稿。

---

## 1. 風格鎖定（每張必貼 · STYLE LOCK）

Version2 唯一風格：**印象派油畫**（厚筆觸、暖金室內光 × 冷靛夜空；不是照片、不是硬線動漫、不是 Q 版）。

**風格基準參考（使用者定稿 mood）：**

| 參考檔 | 對應場景 |
|--------|----------|
| `agents/style-refs/ref-bg-bedroom-night.png` | 夜客廳／窗望城市 |
| `agents/style-refs/ref-bg-entrance-night.png` | 陽台玄關夜景 |
| `agents/style-refs/ref-bg-pet-shop.png` | 寵物店午後金光 |

```text
Impressionistic oil painting. Thick visible brushstrokes, painterly impasto texture, soft blended edges, subtle canvas tooth. Warm amber and golden interior light contrasting cool deep indigo navy night exterior. Complementary blue-and-gold / teal-and-orange palette. Cozy nostalgic quiet everyday Taiwanese atmosphere. Soft atmospheric depth, storybook concept-art feel. Not a photograph, not DSLR realism, not anime cel shading, not hard black outlines, not chibi, not flat vector.
```

### 風格補充（建議接在 STYLE LOCK 之後）

```text
Indie visual novel background art. Indoor warmth leans burnt sienna + honey ochre lamp glow; night exteriors lean indigo wash with distant warm window lights. Keep edges soft and painterly; avoid cartoon exaggeration, glossy 3D, and photoreal detail.
```

### 禁止（`--no` 語意，寫進 prompt）

| 禁止 | 原因 |
|------|------|
| photorealistic photo, DSLR, cinematic 3D | 要油畫筆觸，不是照片 |
| hard black outlines, anime lineart, cel shading | 破壞厚塗暈邊 |
| chibi, Q-version, sticker | 體型誇張 |
| purebred corgi / poodle / shiba / husky | 必須是混種幼犬 |
| text, logo, watermark, UI chrome, readable shop signs | 遊戲資產不可帶字 |
| multiple puppies（除非劇情明確需要） | 角色一致性 |
| **bird nest, straw nest, twig nest, hay nest inside cardboard** | 紙箱＝棄養／臨時窩，**不是鳥巢**；最多乾毛巾／舊衣 |
| neon colors；背景用純白空洞 | 背景需環境色與筆觸；**狗／人物單獨圖**才用乾淨底去背 |
| `Week0`／`WeekN` 子資料夾當資產路徑 | **圖案目錄不分 week**（見 §3） |

---

## 2. 角色外型（Version2 鎖定）

### 布丁（幼犬）

| 項目 | 規格 |
|------|------|
| 品種感 | 台灣常見 **scruffy mixed breed**；毛略蓬、略捲 |
| 年齡 | **約 2 個月**（prompt：`exactly 2 months old`） |
| 體型 | 短腿、圓肚、整體很小、脆弱感；**寫實比例** |
| 毛色 | **golden-tan / honey ochre**；耳尖／背脊略深褐；胸口／吻部奶油色 |
| 五官 | 圓而暖的 **深褐**眼；半垂耳 |
| 表達 | **每張 pose 必須同時有「表情」＋「動作」差異**（耳／眼／嘴／尾／身體姿勢都要讀得出情緒） |
| 紙箱 pose | 幼犬在**空紙箱**或僅墊毛巾；**禁止**鳥巢／草窩／樹枝窩 |
| 分層 | **狗 PNG 獨立疊層**；勿畫進背景圖 |
| 筆觸 | 同一油畫 STYLE LOCK；邊緣柔和、無硬黑描邊 |

### 小晴（女主）

| 項目 | 規格 |
|------|------|
| 年齡 | **26** 歲都市上班族 |
| 外型 | 年輕長髮女性；自然深褐或黑長髮；暖調膚色；一般身形；**溫和寫實五官** |
| 服裝 | 簡素：米白／燕麥／灰褐／低飽和牛仔；無 Logo、無螢光色 |
| 臉 | **允許入鏡**（半身／3/4／柔和正面皆可）；表情疲憊、溫柔、笨拙關心；非名人臉、非網紅整形感 |
| 局部仍可用 | 手／臂特寫（掀箱、抱箱、擦乾）可與有臉立繪並存 |
| 膝靠 | 可靠腿；避免多餘鳥巢道具 |

---

## 3. 資產目錄（**不分 week**）

| 類型 | 路徑 |
|------|------|
| 背景 | `Ch1_Trust_Version2/assets/bg/bg-{slug}.png` |
| 狗 pose | `Ch1_Trust_Version2/assets/dog/dog-{pose}.png` |
| 人物 | `Ch1_Trust_Version2/assets/char/char-{slug}.png` |
| 場景／CG | `Ch1_Trust_Version2/assets/scene/scene-{slug}.png` |
| 風格參考 | `Ch1_Trust_Version2/agents/style-refs/ref-bg-*.png`（僅參考，非遊戲 runtime） |

**禁止**再使用 `dog/Week0/`、`dog/Week3/`、`char/Week0/` 等週次資料夾。  
日數只寫在劇本檔名／內文，不寫進圖檔目錄。

去背：

```powershell
python Ch1_Trust_Version2/tools/remove_sprite_bg.py {pose或完整路徑}
```

Ren'Py 同步（產生後複製一份）：

```text
Ch1_Trust_Version2/Renpy_game/game/assets/bg/
```

---

## 4. Nous Portal 觸發方式

詳見 [`../Nous_Portal.md`](../Nous_Portal.md) §4。

```powershell
hermes login
cd Learn_How_To_Love\tools\hermes
python hermes.py agent --job lhtl-flux-…
```

油畫背景三張（對齊 style-refs）：

```powershell
python hermes.py agent --job lhtl-flux-v2-oil-bgs
```

### Agent job prompt 開頭（複製）

```text
任務前請讀 Ch1_Trust_Version2/agents/image.md 與 Ch1_Trust_Version2/agents/03_character_bible.md。

用 image_generate，模型必須選 fal-ai/flux-2-pro（FLUX 2 Pro）。

風格必須包含並遵守：
Impressionistic oil painting. Thick visible brushstrokes, painterly impasto texture, soft blended edges, subtle canvas tooth. Warm amber and golden interior light contrasting cool deep indigo navy night exterior. Complementary blue-and-gold / teal-and-orange palette. Cozy nostalgic quiet everyday Taiwanese atmosphere. Soft atmospheric depth, storybook concept-art feel. Not a photograph, not DSLR realism, not anime cel shading, not hard black outlines, not chibi, not flat vector.

[下方貼對應模板]
[存檔路徑：assets/dog/ 或 assets/bg/ 或 assets/char/ —— 不分 Week]
只回報路徑與 prompt 摘要。不要改劇本 JS。不要開遊戲。
```

---

## 5. Prompt 模板（FLUX · 複製後替換）

### 5.1 狗單獨（去背用）

**比例建議：** 直式約 3:4。

```text
Impressionistic oil painting. Thick visible brushstrokes, painterly impasto texture, soft blended edges. Warm amber lighting, cozy mood. Soft atmospheric depth. Not a photograph, not anime cel, not chibi, not hard black outlines.

Single scruffy golden-tan mixed breed puppy, exactly 2 months old, short stubby legs, round soft belly, honey ochre fur with slightly darker brown ears and back, lighter cream chest and muzzle, semi-floppy ears, warm dark brown eyes.
{POSE_AND_EXPRESSION — must change both body action AND facial expression}
Centered full body, clean plain soft cream paper background for cutout.
No bird nest, no straw nest, no hay nest. No text, no logo, no purebred markers.
```

### 5.2 背景（無狗、無人物）

**比例建議：** 橫向 16:9。

```text
Impressionistic oil painting. Thick visible brushstrokes, painterly impasto texture, soft blended edges, subtle canvas tooth. Warm amber and golden interior light contrasting cool deep indigo navy night exterior. Complementary blue-and-gold palette. Cozy nostalgic quiet everyday Taiwanese atmosphere. Soft atmospheric depth. Not a photograph, not anime cel, not hard black outlines.

Empty environment background for a Taiwanese visual novel, no people, no dogs, no animals, no text, no logo, no readable signs.
{SCENE_DESCRIPTION}
If cardboard box appears: empty damp shipping box only, maybe a plain towel — NEVER a bird nest or straw nest.
Wide 16:9.
```

### 5.3 小晴（可含臉 · 去背用）

```text
Impressionistic oil painting. Thick visible brushstrokes, soft blended edges, warm amber lighting. Believable proportions, soft facial features. Not a photograph, not anime idol face, not chibi.

26-year-old Taiwanese office worker woman Xiaoqing, long natural dark hair, warm skin, simple oatmeal or gray-brown clothes, tired gentle expression allowed, face visible OK.
{ACTION / CROP}
Clean soft cream cutout background. No bird nest. No text, no logo.
```

### 5.3b 寵物店 NPC（可含臉 · 去背用）

**阿姨** → `char-shop-aunt.png`（Day3 迎賓／貨架推薦）

```text
Impressionistic oil painting character illustration…（同 STYLE LOCK）
Taiwanese middle-aged pet shop auntie ~50, short permed dark hair, warm enthusiastic smile, mustard-yellow apron over oatmeal blouse, full-body welcoming gesture. Cream cutout background. No dog, no text.
```

**結帳妹妹** → `char-shop-cashier.png`（Day2 取名／Day3 結帳）

```text
Impressionistic oil painting character illustration…（同 STYLE LOCK）
Young Taiwanese pet shop checkout clerk ~22, shoulder-length dark hair with side clip, gentle polite smile, sage-green apron over white tee + jeans. Full-body standing, NO counter/furniture. Cream cutout background. No dog, no text.
```

生圖腳本：`tools/flux_petshop_npcs.py`（需 FAL_KEY 或 Nous Tool Gateway）。

### 5.4 全景 CG（人＋狗＋環境 · 少用）

```text
Impressionistic oil painting…（同 STYLE LOCK）
{CG_BEAT}
Same woman and same golden-tan 2-month puppy, cohesive oil painting, Taiwanese apartment or rainy street, no photorealism, no text, cardboard without bird nest.
```

### 5.5 油畫背景（定稿 prompt · 詳見 image_bg.md）

#### A) `bg-living-night.png`（living 基準）

```text
Impressionistic oil painting. Thick visible brushstrokes, painterly impasto. Empty Taiwanese apartment living room at night. Navy sofa + warm lamp left, sliding balcony doors to city night center, wooden bookshelf + Monstera right, cream rug. No people/dogs/text. Wide 16:9.
```

#### B) `bg-living-day.png`（自 living-night img2img）

```text
Same apartment as bg-living-night. Change ONLY to daytime bright natural light. Keep furniture. Optional empty cardboard + towel. No people/dogs/text. Wide 16:9.
```

#### C) `bg-entrance-night.png`

```text
Impressionistic oil painting. Balcony entrance twilight, warm door light, shoes, plants, city dusk. No people/dogs/text. Wide 16:9.
```

#### D) `bg-petshop-day.png`（明亮店內｜無入口）

```text
Impressionistic oil painting. Bright pet boutique INTERIOR: counter + shelves, sunny window. NO entrance/doorway/exterior. No text/logo. Wide 16:9.
```

#### E) `bg-street-night.png`

```text
Impressionistic oil painting. Rainy Taiwanese alley night, wet reflections, empty cardboard box prop. No people/dogs. Wide 16:9.
```

---

## 6. Day1 優先資產清單

對齊 `week0/day1_rainy_cardboard.md`。目錄**不分 week**。

### 6.1 背景（bg）

> 完整規則見 [`image_bg.md`](image_bg.md)。格式：`bg-{place}-{light}.png`

| 檔名 | 場景 | 摘要 | 基準 |
|------|------|------|------|
| `bg-street-night.png` | `d1_street_rain` | 雨夜巷口；空濕紙箱可有 | street 基準 |
| `bg-living-day.png` | Day2 清晨～午 | 同公寓日間／較亮 | 自 **`bg-living-night`** |
| `bg-living-night.png` | Day1 夜客廳／就寢；Day2 傍晚／日終 | **living 基準** | living 基準（勿隨意覆寫） |
| `bg-entrance-night.png` | 陽台玄關 | 開門暖金光 × 暮色城市 | entrance 基準 |
| `bg-petshop-day.png` | 寵物店 | 明亮店內；貨架＋櫃檯；**無入口** | petshop 基準 |

### 6.2 狗 pose（表情＋動作都要變）

| 檔名 | 表情 | 動作 |
|------|------|------|
| `dog-anxious.png` | 擔憂、濕潤上望 | 低趴、耳貼、夾尾、輕顫 |
| `dog-box.png` | 無助、懇求 | **空紙箱**內探頭＋前爪搭箱緣；箱內僅可有毛巾，**禁鳥巢** |
| `dog-wet.png` | 怕但安全感 | 奶油毛巾捲裹，只露眼鼻 |
| `dog-hungry.png` | 猶豫貪食（眼神瞟向食物） | **四腳完整可見**；身後縮、鼻伸向側邊空碗（碗勿遮腳） |
| `dog-shy.png` | 害羞／不好意思 | **頭貼地**；**右前爪放在鼻子上**；左前爪在旁撐地；四肢正確 |
| `dog-scare.png` | 慌亂、受驚 | **整隻趴在地板**，雙耳貼平，眼神慌亂上望／亂瞟，夾尾 |
| `dog-sleepy.png` | 筋疲力盡 | 蜷睡、眼皮沉重、呼吸放慢 |

### 6.3 人物（可含臉）

| 檔名 | 內容 |
|------|------|
| `char-hand-reach.png` | 伸手掀濕紙箱（可半隱臉或低頭側臉） |
| `char-carry-box.png` | 抱／罩箱趕路，**臉可見**，疲憊關心 |
| `char-sit-floor.png` | 客廳地板坐下陪空紙箱／毛巾窩，**臉可見**；箱內**無鳥巢** |
| `char-shop-aunt.png` | 寵物店阿姨；迎賓／推薦（Day3） |
| `char-shop-cashier.png` | 結帳妹妹；問名字／結帳（Day2・Day3） |

---

## 7. 與劇本對照

```text
| ID | 場景 | bg | dogPose | char |
|----|------|-----|---------|------|
| d1_street_rain | 雨夜巷口 | bg-street-night | box / anxious | hand-reach |
```

- 背景：**永不含狗**（空紙箱道具可）  
- 狗／人物：乾淨底 → 去背 RGBA  
- 紙箱：**永不畫鳥巢／草窩**
- 背景／店面：**永不畫可讀文字／招牌**

---

## 8. 審查清單（定稿前）

- [ ] STYLE LOCK 為「印象派油畫」（非照片、非動漫硬線）
- [ ] 模型 `fal-ai/flux-2-pro`
- [ ] 路徑在 `assets/dog/`、`assets/char/`、`assets/bg/`，**無 Week 子資料夾**
- [ ] 狗：每張表情＋動作都不同
- [ ] 紙箱：無鳥巢／草／枝條窩
- [ ] 背景：無人無狗、無文字 logo
- [ ] 人物：臉可出現；溫柔疲憊寫實感
- [ ] 狗／人物已去背；背景不去背
- [ ] 未自動開遊戲

---

## 9. 與正式產線差異

| | Version2（本檔） | 舊 Ch1 產線 |
|--|------------------|---------------|
| 風格 | **印象派油畫**（厚筆觸、暖金×冷靛） | 既有 Demo 水彩對齊圖 |
| 目錄 | **不分 week** | 常有 `Week0/`／`Week3/` |
| 女主臉 | **允許** | 多半不露臉 |
| 紙箱 | 禁鳥巢 | 未特別鎖定 |
| 狗年齡 | 2 months | 常 3 months |
| 風格參考 | `agents/style-refs/ref-bg-*.png` | — |

---

*更新：2026-07-12｜油畫 STYLE LOCK、image_bg 時段、Day1～2 場景表*
