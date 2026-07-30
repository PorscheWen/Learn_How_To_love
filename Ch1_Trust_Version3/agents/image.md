# Version3 美術生圖規範｜Cursor 優先

> 對齊：`game_guild.md` · `outline_trilogy_ch1_10sections.md` · `section_*.md`  
> 背景命名／家族：[`image_bg.md`](image_bg.md)（`bg-{place}-{light}`）  
> 狗外型鎖定：[`image_dog.md`](image_dog.md)（**Option B｜wiry** · `dog-ref-canonical.png`）  
> **預設生圖：Cursor `GenerateImage`**（狗圖務必附 `assets/dog/dog-ref-canonical.png` 作 reference）  
> **備援：** FLUX 2 Pro（`fal-ai/flux-2-pro`）via Nous Portal；僅在 Cursor 不可用、或使用者明確指定時才跑 `tools/flux_*.py`  
> 立繪產出後：`python tools/remove_ai_bg.py INPUT OUTPUT ...` 去背＋去綠邊

---

## 0. 與 game_guild 對齊（畫面原則）

| guild 規則 | 美術落地 |
|------------|----------|
| **不顯示 trust 大數字** | 靠**狗距離、耳尾、睡姿、是否背對**＋予安內心一句話 |
| **軟分軌**（S01～S08） | **同一 bg**；只換 `dogPose`／距離層，不產兩套背景劇情圖 |
| **硬分歧**（S09／S10） | 結局 A～D 用**睡姿／牽繩／門邊距離**區分，可少量專用 CG |
| **十段不增不減** | 資產表只對 S01～S10；禁止為「適應日記」加多餘場景 |
| **升信任體感** | 蹲等、側身、縮手、擋在中間、背對睡 → pose 必須讀得出 |
| **降信任體感** | 硬抓、腳趕、關、甩開、硬拖 → pose 退縮／貼牆／僵住 |

### 軟分軌距離層（疊狗時用，不改 bg）

| 進段 trust | 建議距離層 | 狗體感 |
|------------|------------|--------|
| 低（≤3） | 遠／貼牆／門邊 | 耳平、夾尾、僵 |
| 中（4～6） | 兩步遠地板 | 停、半步、觀望 |
| 高（≥7） | 伸手可及／貼腿／背對睡 | 耳鬆、下巴貼地、願背對 |

---

## 1. 風格鎖定（每張必貼 · STYLE LOCK）

Version3 沿用印象派油畫（與 V2 視覺語言相容，劇情／角色全新）。

### 1.0 背景一句鎖定（BG ONE-LINER｜未來背景必貼）

> 自 `entrance-day`／`alley-day`／`corridor-day`／`living-night` 四張定稿歸納；視覺錨點見 `assets/bg/refs/`。

```text
Thick-impasto impressionistic oil painting of quiet everyday Taiwanese residential spaces—warm amber lamp glow or sunlit ochre walls against cool indigo night sky or soft daylight; soft blended edges, tactile brush texture on wood floors, plaster walls, Monstera plants and navy sofa accents indoors, metal window bars and sidewalk potted plants outdoors; empty of people and dogs, no readable text—storybook visual-novel background, not a photograph, not anime.
```

**生圖用法：** 先貼 BG ONE-LINER，再接「本場 place／light／構圖一句」；Cursor `GenerateImage` 建議附 `assets/bg/refs/ref-living-night.png`（室內）或 `ref-alley-day.png`（外景）作 reference。

### 1.1 通用 STYLE LOCK（背景＋立繪＋狗）

```text
Impressionistic oil painting. Thick visible brushstrokes, painterly impasto texture, soft blended edges, subtle canvas tooth. Warm amber and golden interior light contrasting cool deep indigo navy night exterior. Complementary blue-and-gold / teal-and-orange palette. Cozy nostalgic quiet everyday Taiwanese atmosphere. Soft atmospheric depth, storybook concept-art feel. Not a photograph, not DSLR realism, not anime cel shading, not hard black outlines, not chibi, not flat vector.
```

### 風格補充

```text
Indie visual novel background art. Indoor warmth leans burnt sienna + honey ochre lamp glow; night exteriors lean indigo wash with distant warm window lights. Keep edges soft and painterly; avoid cartoon exaggeration, glossy 3D, and photoreal detail.
```

### 禁止（`--no` 語意）

| 禁止 | 原因 |
|------|------|
| photorealistic photo, DSLR, cinematic 3D | 要油畫筆觸 |
| hard black outlines, anime lineart, cel shading | 破壞厚塗暈邊 |
| chibi, Q-version, sticker | 體型誇張 |
| purebred corgi / poodle / shiba / husky | 必須是混種幼犬 |
| text, logo, watermark, UI chrome, readable signs | 遊戲資產不可帶字 |
| **trust meter, number HUD, floating score** | 對齊 guild：畫面不顯示信任數字 |
| multiple puppies（除非劇情需要） | 角色一致 |
| bird nest, straw nest, hay nest in cardboard | 紙箱僅空箱／毛巾／舊衣 |
| neon；背景純白空洞 | 背景需環境色；狗／人物單獨圖才用乾淨底去背 |
| `Week0`／`WeekN` 子資料夾 | **圖案目錄不分 week** |

---

## 2. 角色外型（Version3 鎖定）

### 狗（預設名小7 · 混種幼犬）

> **外型定稿：Option B｜wiry** — 完整鎖定見 [`image_dog.md`](image_dog.md)。  
> 基準圖：`assets/dog/dog-ref-canonical.png`。  
> 預設 **小7**（超商暱稱）；玩家可改 → `dogLabel(s)`。取名前敘事多用「牠」；**圖檔勿寫死狗名**。

| 項目 | 規格（B 摘要） |
|------|----------------|
| 品種感 | 台灣常見 **scruffy / wiry mixed breed**（略亂硬毛，非純種） |
| 年齡 | **約 2～3 個月**（prompt：`about 2-3 months old`） |
| 體型 | **短腿、結實偏瘦**；脆弱街犬幼崽感 |
| 毛質 | **短～中、wiry／scruffy＋厚 impasto 團塊**（禁蓬毛貴賓感、禁過圓 Q 臉） |
| 毛色 | **honey golden-tan**；耳尖深褐；背脊 **grizzled saddle**；胸口／吻周／腳掌 **cream** |
| 五官 | 略角精實臉；**大而暖深褐眼＋catchlight**；**軟垂 V 耳** |
| 表達 | **每張 pose 必須同時有表情＋動作**（耳／眼／嘴／尾／身體） |
| 分層 | **狗 PNG 獨立疊層**；勿畫進背景 |
| 底板 | 生圖用 **純黑 #000** → `remove_ai_bg.py` 去背 |
| 紙箱 | S02 為壓扁紙箱邊／臨時窩；禁鳥巢 |
| 錨點 | `assets/dog/refs/`（2026-07-25 用戶定稿） |

產狗圖必貼 `image_dog.md` 的 **IDENTITY LOCK**；審查清單見該檔 §5。

### 予安（女主）

> **完整鎖定：** [`image_char.md`](image_char.md) · 錨點 `assets/char/refs/ref-yuan-*.png`

| 項目 | 規格 |
|------|------|
| 年齡 | **26** 歲都市上班族 |
| 外型 | 長深褐～近黑髮（略亂／微波）；暖調膚色；疲憊溫柔寫實五官；一般偏瘦 |
| 服裝 | 米白／燕麥／奶油上衣；深褐／橄欖／炭灰寬褲；平底樂福；無 Logo、無螢光 |
| 臉 | **允許入鏡**；非名人臉、非偶像二次元臉 |
| 關鍵道具 | **耳機**（掛脖／戴上）；便當塑膠袋；棕色皮牽繩 |
| 畫風 | 厚 **impasto**；生圖純黑底 → `remove_ai_bg.py` |

### NPC（精簡 · 勿沿用 V2 寵物店阿姨主線）

| 角色 | 檔名 | 出現 |
|------|------|------|
| 超商店員 | `char-clerk.png` | S01／S02 |
| 走廊第三者（鄰居／管理員） | `char-neighbor.png` | S06 |
| 同事（接手提議） | `char-coworker.png` | S09 茶水間 |
| 同事（咖啡廳蹲等） | `char-coworker-cafe.png` | S09 咖啡廳 |

詳見 [`image_char.md`](image_char.md) NPC 鎖定。

---

## 3. 資產目錄（**不分 week**）

| 類型 | 路徑 |
|------|------|
| 背景 | `Ch1_Trust_Version3/assets/bg/bg-{place}-{light}.png` |
| 狗 pose | `Ch1_Trust_Version3/assets/dog/dog-{pose}.png` |
| 人物 | `Ch1_Trust_Version3/assets/char/char-{slug}.png` |
| 場景／結局 CG | `Ch1_Trust_Version3/assets/scene/scene-{slug}.png` |
| 風格參考 | `Ch1_Trust_Version3/agents/style-refs/ref-bg-*.png`（可沿用 V2 refs） |

**禁止** `dog/Week0/` 等週次資料夾。Section 只寫在劇本，不寫進圖檔目錄。

去背（若工具已就位）：

```powershell
python tools/remove_ai_bg.py INPUT OUTPUT
```

---

## 4. Nous Portal 觸發方式

```powershell
hermes login
cd Learn_How_To_Love\tools\hermes
python hermes.py agent --job lhtl-flux-…
```

### Agent job prompt 開頭（複製）

```text
任務前請讀 Ch1_Trust_Version3/agents/image.md、image_dog.md、image_char.md 與 game_guild.md。

用 image_generate，模型必須選 fal-ai/flux-2-pro（FLUX 2 Pro）。  
> 注意：本節僅供 **FLUX 備援**；日常定稿請先用 Cursor `GenerateImage`。

風格必須包含並遵守 STYLE LOCK（厚 impasto 印象派油畫）。
狗必須遵守 image_dog.md IDENTITY LOCK（Option B wiry），並對齊 dog-ref-canonical.png。
人物必須遵守 image_char.md（予安／NPC），並對齊 assets/char/refs/。
畫面禁止信任數字／HUD。軟分軌＝同背景換狗 pose。

[下方貼對應模板]
[存檔：Ch1_Trust_Version3/assets/dog|bg|char —— 不分 Week]
只回報路徑與 prompt 摘要。不要改劇本。不要開遊戲。
```

---

## 5. Prompt 模板（Cursor 優先 · FLUX 備援 · 複製後替換）

### 5.1 狗單獨（去背用）

**比例建議：** 直式約 3:4。  
**必讀：** [`image_dog.md`](image_dog.md)（Option B｜完整 IDENTITY LOCK）。

```text
Thick-impasto impressionistic oil painting. Heavy visible brushstrokes, painterly impasto texture, soft blended edges. Warm amber key light from above-left. Soft atmospheric depth. Not a photograph, not anime cel, not chibi, not hard black outlines.

SAME PUPPY IDENTITY LOCK (Option B wiry — MUST match dog-ref-canonical.png and assets/dog/refs/):
One continuous character. About 2-3 months old Taiwanese scruffy wiry mixed-breed puppy (not purebred). Compact short-legged body, slightly thin street-puppy build. Wiry short-to-medium messy coat as thick impasto paint clumps. Honey golden-tan fur; darker chestnut floppy ear tips and grizzled darker saddle on back; cream-light tan muzzle and chest. Soft V-shaped floppy ears. Large round warm dark-brown eyes with catchlights. Small wet black nose. Slightly angular scruffy street-puppy face (NOT round plush face, NOT fluffy show-dog coat).
{POSE_AND_EXPRESSION — must change both body action AND facial expression; convey trust distance: retreat / half-step / parallel rest / back-to-back sleep}
Centered full body. SOLID FLAT BLACK (#000000) background for cutout.
No bird nest, no straw nest. No text, no logo, no purebred markers, no trust meter UI.
```

### 5.2 背景（無狗、無人物）

**比例建議：** 橫向 16:9。詳見 [`image_bg.md`](image_bg.md)。

```text
Impressionistic oil painting. Thick visible brushstrokes, painterly impasto texture, soft blended edges, subtle canvas tooth. Warm amber and golden interior light contrasting cool deep indigo navy night exterior. Complementary blue-and-gold palette. Cozy nostalgic quiet everyday Taiwanese atmosphere. Soft atmospheric depth. Not a photograph, not anime cel, not hard black outlines.

Empty environment background for a Taiwanese visual novel, no people, no dogs, no animals, no text, no logo, no readable signs, no UI meters.
{SCENE_DESCRIPTION}
If cardboard appears: empty damp shipping box or flattened carton + plain towel only — NEVER a bird nest.
Wide 16:9.
```

### 5.3 予安／人物（可含臉 · 去背用）

**必讀：** [`image_char.md`](image_char.md)。比例建議直式 3:4。

```text
Thick-impasto impressionistic oil painting. Heavy visible brushstrokes, painterly impasto texture, soft blended edges. Soft warm key light. Soft atmospheric depth. Not a photograph, not anime idol face, not chibi, not hard black outlines.

SAME WOMAN IDENTITY LOCK (Yuan / 予安 — MUST match assets/char/refs/ref-yuan-*.png):
26-year-old Taiwanese office worker woman. Long natural dark brown-black hair slightly messy past shoulders. Warm East-Asian skin, soft realistic tired gentle features, not celebrity face. Slender everyday build. Muted wardrobe: cream/oatmeal/beige tops, dark brown/taupe/charcoal trousers, flat loafers.
{POSE_AND_EXPRESSION / props: headphones on|around neck, bento bag, blocking palm, squat with leash}
Centered full body. SOLID FLAT BLACK (#000000) background for cutout.
No text, no logo, no trust HUD, no scenery.
```

NPC 用 `image_char.md` §3 對應段落；同事臉必須 ≠ 予安。

### 5.4 全景 CG（人＋狗＋環境 · 少用）

僅建議用於：**S02 對視記憶點**、**S09 差點送走**、**S10 四結局睡姿**。其餘用 bg＋疊層。

```text
Impressionistic oil painting…（同 STYLE LOCK）
{CG_BEAT}
Same woman Yuan and same golden-tan mixed puppy, cohesive oil painting, Taiwanese apartment / alley / cafe entrance, no photorealism, no text, no trust numbers.
```

---

## 6. Ch1 十段優先資產（對齊 guild §0）

> 節奏：S01 短、S02 鉤子、S03～S04 各一記憶點、中段軟分軌少產新 bg、S09～S10 結局圖。

### 6.1 背景優先序

| 優先 | 檔名 | 主要 Section |
|------|------|----------------|
| P0 | `bg-living-night.png` | S01／S04／S07／S10 |
| P0 | `bg-living-day.png` | S04／S05 |
| P0 | `bg-backdoor-night.png` | **S02 相遇**（卸貨後門／機車棚） |
| P0 | `bg-stairwell-night.png` | **S03** |
| P1 | `bg-convenience-night.png` | S01／S02 |
| P1 | `bg-corridor-day.png` | S06 |
| P1 | `bg-alley-day.png` | S08 巷口轉角 |
| P1 | `bg-cafe-day.png` | S09 咖啡廳門口 |
| P2 | `bg-office-night.png` | S01 可省略／用黑場＋對白 |
| P2 | `bg-kitchen-day.png` | S04 門口記憶點（或 living 裁切） |

完整家族規則見 `image_bg.md`。

### 6.2 狗 pose（表情＋動作；信任可感）

| 檔名 | 表情 | 動作 | 主用 |
|------|------|------|------|
| `dog-anxious.png` | 擔憂上望 | 低趴、耳貼、夾尾 | S02／低信任 |
| `dog-halfstep.png` | 警戒好奇 | 「既不碰你、也不放你走」的半步 | S02 記憶 |
| `dog-stair-watch.png` | 警戒 | 靠牆、面向電梯方向 | S03 換窩 |
| `dog-door-sleep.png` | 睏但守門 | 睡在房門外墊上 | S03 鉤子 |
| `dog-parallel.png` | 放鬆一點 | 兩步遠地板、下巴貼地 | S04 |
| `dog-kitchen-door.png` | 跟隨觀望 | 停在廚房門檻外 | S04 記憶 |
| `dog-ear-flat.png` | 被尖聲嚇到 | 耳平、退 | S05 Tone− |
| `dog-sniff-wire.png` | 好奇 | 嗅耳機線 | S05 鉤子 |
| `dog-behind-legs.png` | 求護衛 | 躲小腿後（S06 用 `dog_behind_pair`，疊在予安下方） | S06 Guard＋ |
| `dog-forehead-nudge.png` | 輕謝 | 額頭頂小腿 | S06 記憶 |
| `dog-guard-door.png` | 不安守門 | 趴房門口 | S07 |
| `dog-street-tense.png` | 繃緊 | 貼牆／僵住（低信任 S08） | S08 |
| `dog-leash-wait.png` | 累但信任 | 停步等待後願再走 | S08 高；S09 玄關 |
| `dog-shoe-sleep.png` | 安心 | 喝完水靠鞋邊睡 | S08 記憶 |
| `dog-farewell.png` | 告別上望 | 坐姿抬頭看予安（無牽繩） | S09 客廳 |
| `dog-cafe-refuse.png` | 拒絕警告 | 胸背帶＋牽繩、貼腳對同事僵／低鳴 | S09 咖啡廳 |
| `dog-cafe-tense.png` | 兩人中間僵 | 僵住、面向予安（找妳） | S09 咖啡廳低信任 |
| `dog-refuse-stranger.png` | 拒絕 | 貼予安腳邊、對伸手僵／低鳴 | S09 fallback／舊 |
| `dog-back-sleep.png` | 信任落地 | **背對**睡在伸手可及處 | 結局 A |
| `dog-check-sleep.png` | 選定仍學 | 睡近但睜眼確認／轉身查看 | 結局 B |
| `dog-door-edge.png` | 薄冰 | 牽繩掛好、狗睡門邊、不看人 | 結局 D |

### 6.3 人物

| 檔名 | 內容 |
|------|------|
| `char-yuan-commute.png` | 予安夜歸／超商；可戴耳機 |
| `char-yuan-squat-side.png` | 側身蹲下等待（S02 A） |
| `char-yuan-carry-pup.png` | 側抱幼犬上樓 |
| `char-yuan-headphones.png` | 戴耳機開會（S05 尖）；S09 茶水間 |
| `char-yuan-block.png` | 走廊擋在狗與陌生人中間（S06）；**面向左**擋左側鄰居 |
| `char-yuan-leash.png` | 牽繩、蹲等（S08 玄關／樹下停等）；S09 **玄關**（×0.8） |
| `char-yuan-walk.png` | 站姿走路握牽繩｜**S08 巷口**（非蹲） |
| `char-yuan-farewell.png` | 單膝下跪攤手告別（無牽繩）｜S09 客廳 |
| `char-yuan-cafe.png` | 站姿握牽繩、衝突表情｜S09 咖啡廳 |
| `char-clerk.png` | 超商店員 |
| `char-neighbor.png` | 走廊第三者 |
| `char-coworker.png` | S09 茶水間同事（站姿提議） |
| `char-coworker-cafe.png` | S09 咖啡廳同事（蹲姿側身、面向女主／狗） |

### 6.4 結局靜幀（gallery／結局一覽解鎖）

| 檔名 | 結局 | 畫面 |
|------|------|------|
| `gallery/ending-a-back.png` | A 背靠 | 停電夜沙發前同睡／背靠 |
| `gallery/ending-b-learning.png` | B 選定 | 近睡仍抬頭確認 |
| `gallery/ending-c-handover.png` | C 送走 | 空屋；空掛勾／鑰匙獨掛 |
| `gallery/ending-d-thin-ice.png` | D 薄冰 | 門邊睡、人狗隔一段距離 |

達成對應結局後，主選單「結局一覽」可點開靜幀。

### 6.5 隱藏紀念照（gallery／僅結局 A）

| 檔名 | 解鎖 | 畫面 |
|------|------|------|
| `gallery/secret-lap-sleep.png` | 結局 A | 中型幼犬躺在予安大腿特寫 |
| `gallery/secret-forehead-nudge.png` | 結局 A | 額頭輕碰 |
| `gallery/secret-behind-legs.png` | 結局 A | 擋在身後（走廊） |
| `gallery/secret-shoe-sleep.png` | 結局 A | 鞋邊小睡 |
| `gallery/secret-nose-touch.png` | 結局 A | 指尖碰鼻 |
| `gallery/secret-water-bowl.png` | 結局 A | 第一次喝新水碗 |

- **已移除**背對背／胸口同睡紀念照（結局 A 靜幀 `ending-a-back` 仍保留）。
- 文案軟提示；**禁止**親密度條或 100% 字樣。
- `persistent.unlocked_secret_photos`；`process_ending_unlock("A")` 解鎖 `SECRET_PHOTO_ORDER` 六張。
- 隱藏文章見 `Renpy_game/game/hidden_content.rpy`。

---

## 7. Section × 資產對照（劇本用）

```text
| Sec | 主 bg | 關鍵 dogPose | 信任畫面重點 |
|-----|-------|--------------|--------------|
| 01 | convenience-night → living-night | —（可無狗） | 空白；不轉後門 |
| 02 | backdoor-night | halfstep / retreat / anxious | 對視；蹲等可感 |
| 03 | stairwell-night | stair-watch → door-sleep | 換窩；歸來 |
| 04 | living-day/night | parallel / kitchen-door | 平行安靜 |
| 05 | living-day | ear-flat / sniff-wire | Tone 尖↔低 |
| 06 | corridor-day | behind-legs / forehead-nudge | Guard 擋人 |
| 07 | living-night | guard-door | 依賴對調 |
| 08 | alley-day → living | street-tense / leash-wait / shoe-sleep | Dist 停等 |
| 09 | living-day → entrance-day → cafe-day | farewell → leash-wait → cafe-refuse／cafe-tense | 告別→扣帶→G2 留下／送走 |
| 10 | living-night | back-sleep / check-sleep / door-edge | 結局睡姿 |
```

- 背景：**永不含狗**（空紙箱／牽繩掛勾可當道具）  
- 狗／人物：乾淨底 → 去背 RGBA  
- **禁止**畫面上的信任條／數字

---

## 8. 審查清單（定稿前）

- [ ] STYLE LOCK／背景 BG ONE-LINER（見 `image.md` §1.0、`image_bg.md` §0.5）
- [ ] 預設用 Cursor `GenerateImage`；FLUX 2 Pro 僅備援
- [ ] 路徑在 `Ch1_Trust_Version3/assets/`，**無 Week 子資料夾**
- [ ] 女主為**予安**（非小晴）；狗預設**小7**，外型為 **Option B wiry**（見 `image_dog.md`），圖檔不寫死玩家改名
- [ ] 狗：對齊 `dog-ref-canonical.png`；每張表情＋動作不同；軟分軌距離讀得出
- [ ] 無信任數字／HUD
- [ ] 背景：無人無狗、無文字 logo；時段 light 正確（見 image_bg）
- [ ] 結局 A～D 睡姿／距離可區分
- [ ] 未自動開遊戲

---

### 2026-07-25 正式資產狀態

- 背景 **13 張**已依 BG ONE-LINER 全量重產（含 `gate-night`）；原圖備份於 `assets/bg/_backup_20260725_125336/`。
- 風格錨點：`assets/bg/refs/` 四張已同步本次正式構圖。
- **狗圖（同日晚）：** 以用戶 5 張錨點重鎖 Option B；原圖備份於 `assets/dog/_backup_20260725_183542/`；`canonical`／`anxious`／`behind-legs`／`refuse-stranger` 直接落地錨點去背版；其餘 15 pose 依新 IDENTITY LOCK 全量重產（黑底＋`remove_ai_bg.py`）。詳見 `image_dog.md`。
- **人物（同日）：** 7 張 `assets/char/` 全量重產；備份 `assets/char/_backup_20260725_193450/`；新建 [`image_char.md`](image_char.md)（予安 IDENTITY＋NPC）；錨點 `assets/char/refs/`。

### 2026-07-28｜S09 專用立繪與劇情朝向

- 新增：`char-yuan-farewell`、`char-yuan-cafe`、`char-coworker-cafe`、`dog-farewell`、`dog-cafe-refuse`、`dog-cafe-tense`（Cursor 生圖＋`remove_ai_bg.py`）。
- 客廳開頭用**告別圖**（無牽繩）；玄關牽繩立繪 **×0.8**；咖啡廳**不沿用** S08 蹲牽繩／舊同事站姿。
- 朝向以劇情為準：拒絕時狗面向同事；僵住／留下時面向予安。詳見 [`section_09_almost_handoff.md`](section_09_almost_handoff.md)。

---

## 9. 與 Version2 切割

| | Version3（本檔） | Version2 |
|--|-----------------|----------|
| 故事 | 十段 S01～S10；超商後門相遇 | 雨夜紙箱七日 |
| 女主 | **予安** | 小晴 |
| 狗名 | 預設**小7**（可改） | 布丁等 |
| 信任畫面 | 距離／耳尾／睡姿（guild） | 未鎖定四結局睡姿 |
| 主場景 | backdoor／gate／entrance／corridor／cafe | street-rain／petshop／clinic |
| 分軌 | 同 bg 換 pose | Day 劇本導向 |
| 目錄 | `Ch1_Trust_Version3/assets/` | `Ch1_Trust_Version2/assets/` |

---

*更新：2026-07-28｜S09 告別／咖啡廳專用立繪與劇情朝向；此前 2026-07-25 全量重產見上*
