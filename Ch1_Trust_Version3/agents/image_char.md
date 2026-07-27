# Version3｜人物外型鎖定｜image_char.md

> 對齊：`game_guild.md` · `image.md` · `image_dog.md`（畫風一致）  
> **女主：** 予安（Yuan）— 連續同一人跨 pose  
> **錨點（2026-07-25）：** `assets/char/refs/`（由當日正式檔備份）  
> **生圖順序：** Cursor `GenerateImage`（必附對應 `refs/ref-*`）；產完 `python tools/remove_ai_bg.py`  
> 圖檔**勿寫死狗名**；女主姓名固定予安。

---

## 0. 一致性原則

| 規則 | 說明 |
|------|------|
| **同一人** | 予安跨 pose：臉型、髮長／髮色、體型、服裝色系不得漂成另一個角色 |
| **畫風對齊狗／背景** | 厚 **impasto** 油畫筆觸；非寫真、非二次元大眼、非 Q 版 |
| **分層** | 人物 PNG **獨立疊層**；勿畫進 bg |
| **禁寫字** | 無文字、logo、信任 HUD |
| **禁名人臉** | 非可辨公眾人物 |

---

## 1. 予安 IDENTITY LOCK

### 1.1 身分卡

| 項目 | 鎖定 |
|------|------|
| 姓名 | **予安**（敘事固定；勿改回小晴） |
| 年齡 | **26** 歲台灣都市上班族 |
| 體型 | 偏瘦、一般身高比例；疲憊感在姿勢與眼神，不是病態瘦 |
| 髮 | **長、自然深褐～近黑**；略亂／微波浪；披肩 |
| 膚 | 暖調東亞膚色；可有淡淡黑眼圈 |
| 臉 | 溫和寫實五官；疲憊／溫柔／笨拙關心；**允許入鏡** |
| 服裝主調 | **米白／燕麥／奶油**上衣；**深褐／橄欖／炭灰**寬褲；平底樂福／室內拖鞋感 |
| 道具 | 黑／深灰 **頭戴式耳機**（掛脖或戴上）；便當塑膠袋；棕色皮牽繩 |
| 禁 | Logo、螢光色、華麗飾品、偶像臉、過尖下巴歐美網紅感 |

### 1.2 IDENTITY 文案（必貼）

```text
SAME WOMAN IDENTITY LOCK (Yuan / 予安 — MUST match assets/char/refs/ref-yuan-*.png):
One continuous character across all poses. 26-year-old Taiwanese office worker woman. Long natural dark brown-black hair, slightly messy or soft waves past shoulders. Warm East-Asian skin, soft realistic features, gentle tired eyes (subtle under-eye fatigue OK), not celebrity face, not anime idol face. Slender everyday build. Wardrobe always muted: cream/oatmeal/beige tops, dark brown/taupe/charcoal trousers, simple flat loafers or indoor slippers. No logos, no neon colors, no jewelry flash. Thick-impasto impressionistic oil painting. Believable adult proportions. No text, no trust HUD.
```

### 1.3 STYLE（與狗圖同錨）

```text
Thick-impasto impressionistic oil painting. Heavy visible brushstrokes, painterly impasto texture, soft blended edges, tactile canvas tooth. Soft warm key light. Soft atmospheric depth, storybook concept-art feel. Not a photograph, not DSLR realism, not anime cel shading, not hard black outlines, not chibi, not flat vector, not smooth 3D.
```

### 去背底板

```text
Centered full body (or clear readable crop). SOLID FLAT BLACK (#000000) background for cutout. No floor plane, no scenery unless a minimal prop is required (headphones, plastic bento bag, leather leash).
```

---

## 2. Pose／檔名契約

| 檔名 | 表情／動作 | 服裝／道具 | 主用 |
|------|------------|------------|------|
| `char-yuan-commute.png` | 疲憊垂眼、略駝 | 奶油開襟針織＋灰 T＋深褐寬褲；**耳機掛脖**；右手提便當塑膠袋 | S01／夜歸／超商 |
| `char-yuan-headphones.png` | 專注／疏離 | 淺灰藍長袖襯衫袖捲起＋深褐褲；**耳機戴上**；雙手插口袋 | S05 Tone 尖 |
| `char-yuan-block.png` | 冷靜擋在中間 | 米白襯衫袖捲；**面向左**；一臂前伸開掌擋／護（對左側鄰居） | S06 |
| `char-yuan-leash.png` | 蹲等／耐心 | 米白襯衫＋橄欖褲；側蹲；手握**棕色皮牽繩**下垂 | S08 |
| `char-clerk.png` | 禮貌微笑 | 年輕男店員；深藍短袖＋深色圍裙＋深褲 | S01／S02 |
| `char-neighbor.png` | 熱心伸手 | 中年女鄰居；綠卡迪＋米上衣；**面向右**伸手（對右側予安／狗） | S06 |
| `char-coworker.png` | 真誠提議 | 年輕女同事；淡紫開襟＋米內搭＋炭灰褲；一手前伸 | S09 |

**未落地但 image.md 曾列：** `char-yuan-squat-side`／`char-yuan-carry-pup` — 需要時另產，仍須貼予安 IDENTITY。

---

## 3. NPC 鎖定（簡）

### 店員（clerk）

```text
Young Taiwanese convenience-store clerk, early 20s man, short neat black hair, polite gentle smile, dark blue short-sleeve collared shirt, long dark brown-gray bib apron, dark trousers, black work shoes. Hands clasped politely in front. Full body. Same thick-impasto oil style. SOLID FLAT BLACK background.
```

### 鄰居（neighbor）

```text
Middle-aged Taiwanese neighbor woman, warm kind smile, medium-length dark hair, sage-green knit cardigan over cream top, olive trousers. One arm extended forward palm open (reaching toward puppy / offering). Waist-up or three-quarter OK. Same thick-impasto oil style. SOLID FLAT BLACK background.
```

### 同事（coworker）

```text
Young Taiwanese office coworker woman, friendly sincere smile, dark shoulder-length bob with soft waves, lavender knit cardigan over cream tee, charcoal trousers, flat shoes. One arm gently extended open-palm (offering to take the dog). Full body. Same thick-impasto oil style. SOLID FLAT BLACK background. NOT the same face as Yuan.
```

---

## 4. 完整 Prompt 模板

```text
{STYLE}

{IDENTITY LOCK — Yuan or NPC block}

{POSE_AND_EXPRESSION / wardrobe / props}

Centered readable full body (or clear crop). SOLID FLAT BLACK (#000000) background for cutout.
No text, no logo, no trust meter UI, no scenery.
```

### Cursor 注意

- 予安：`reference_image_paths` 至少含 `refs/ref-yuan-commute.png`＋本 pose 舊檔  
- NPC：附對應 `refs/ref-clerk|neighbor|coworker.png`  
- `aspect_ratio`：全身 `"3:4"`；鄰居半身可用 `"3:4"`  
- 產完 → `python tools/remove_ai_bg.py INPUT OUTPUT` → 覆蓋 `assets/char/char-*.png`

---

## 5. 審查清單

- [ ] 予安跨 pose 仍是同一人（髮／臉／服裝色系）
- [ ] 厚 impasto，未漂成寫真或二次元
- [ ] 黑底已去背，四角透明
- [ ] 無文字／logo／信任數字
- [ ] 同事臉 ≠ 予安臉
- [ ] 未自動開遊戲

---

## 6. 變更紀錄

| 日期 | 內容 |
|------|------|
| 2026-07-25 | 建立本檔；備份 `assets/char/_backup_20260725_193450/`；以現有 7 張為錨重寫 IDENTITY／STYLE；全量重產 |

---

*建立：2026-07-25｜人物外型鎖定＋黑底去背流程（對齊狗圖重產）*
