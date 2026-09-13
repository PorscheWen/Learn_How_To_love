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
| **室內／室外** | 梯廳、巷口、街、咖啡廳、後門＝**樂福鞋＋外出襯衫／針織**；客廳、開冰箱、脫鞋後玄關＝**襪、不穿鞋**。S06 開場在梯廳，禁毛衣＋襪、禁拖鞋 |
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
| 服裝主調 | **米白／燕麥／奶油**上衣；**深褐／橄欖／炭灰**寬褲；**室外平底樂福、室內襪（不穿鞋）**；禁梯廳／巷口拖鞋 |
| 道具 | 黑／深灰 **頭戴式耳機**（掛脖或戴上）；便當塑膠袋；**牛皮紙購物袋**；棕色皮牽繩 |
| 禁 | Logo、螢光色、華麗飾品、偶像臉、過尖下巴歐美網紅感 |

### 1.2 IDENTITY 文案（必貼）

```text
SAME WOMAN IDENTITY LOCK (Yuan / 予安 — MUST match assets/char/refs/ref-yuan-*.png):
One continuous character across all poses. 26-year-old Taiwanese office worker woman. Long natural dark brown-black hair, slightly messy or soft waves past shoulders. Warm East-Asian skin, soft realistic features, gentle tired eyes (subtle under-eye fatigue OK), not celebrity face, not anime idol face. Slender everyday build. Wardrobe always muted: cream/oatmeal/beige tops, dark brown/taupe/charcoal trousers. Outdoor (stairwell, alley, street, cafe, backdoor): simple brown loafers. Indoor after shoes off (living, kitchen, post-entry entrance): socks, no shoes, no slippers on public floors. No logos, no neon colors, no jewelry flash. Thick-impasto impressionistic oil painting. Believable adult proportions. No text, no trust HUD.
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
| `char-yuan-commute.png` | 疲憊垂眼、略駝 | 奶油開襟針織＋灰 T＋深褐寬褲；**耳機掛脖**；右手提便當塑膠袋；外出皮鞋 | **僅** 外出：S01 夜歸／超商／巷口／玄關進門、S02 後門前、S10 送走後巷口；**禁**開冰箱、倒水、白天門邊、客廳坐、S10 空屋／擺碗 |
| `char-yuan-home-stand.png` | 進屋後空手站 | **室內裝**：燕麥寬鬆毛衣＋炭灰家居褲＋淺色襪；**不穿鞋** | S01 開冰箱；S06 **進屋玄關後**；S07 倒水；S10 脫鞋後客廳／廚房／擺碗。**禁**梯廳／走廊 |
| `char-yuan-paper-bag.png` | 提紙袋回家 | 通勤服＋皮鞋；右手提**牛皮紙購物袋** | **僅** S10 街／玄關進門（尚未脫鞋） |
| `char-yuan-sofa.png` | 室內沙發坐 | **室內裝**＋襪；坐姿**無椅**（疊左沙發）；滑手機 | S01 客廳吃便當；S09／S10 夜客廳（`char_left_sit`） |
| `char-yuan-home-sit.png` | 室內坐椅 | **室內裝**＋襪；坐在小木凳上滑手機；面向左 | **S04** 書櫃前木椅（`yuan home_sit`／`char_chair`） |
| `char-yuan-squat-side.png` | 側身蹲等 | 米白襯衫＋橄欖褲；側蹲不伸手；**無牽繩** | **S02** Dist＋；`char_backdoor_squat` zoom **0.31**（卸貨門對景） |
| `char-yuan-carry-pup.png` | 側抱幼犬 | 米白襯衫＋橄欖褲＋**棕色樂福鞋**；側抱小7 | S02 帶走／硬抱失敗一瞬（後門 `char_backdoor_carry` **0.31**、巷口 `char_street_carry` **0.23**、急診 `char_clinic` **0.27**、客廳 `char_living` **0.32**）；**S06 梯廳**抱回屋內（`CHAR_POSE_SCALE` **1.056**） |
| `char-yuan-headphones.png` | 專注／疏離 | 淺灰藍長袖襯衫袖捲起＋深褐褲；**耳機戴上**；外出皮鞋；**站姿** | S01／S09 **辦公室** |
| `char-yuan-headphones-off.png` | Tone 切換／下班 | 同服裝；**耳機掛脖**；站姿 | **S02** 辦公室關螢幕（`char_office`） |
| `char-yuan-headphones-sit.png` | 視訊開會 | 同襯衫；耳機戴上；**室內襪**；坐木凳 | **S05** 客廳左坐（`yuan headphones_sit`／`char_chair_left`） |
| `char-yuan-headphones-off-sit.png` | 關麥／散會 | 同襯衫；耳機掛脖；**室內襪**；坐木凳 | **S05** 客廳左坐（`yuan headphones_off_sit`／`char_chair_left`） |
| `char-yuan-sick-bed.png` | 發燒虛弱 | **沿床躺、看向狗**：頭在右枕（床頭），身體與床平行；面向左、視線看向門邊地板。米白棉質睡衣；腰以下蓋燕麥薄被；**無皮帶、無鞋、不畫狗** | **S07** 開場即顯示（`char_bedroom` **0.18**／xalign **0.78**／ypos **0.76**）。倒水仍 `home-stand`。舊正對鏡頭稿 `_work/char-yuan-sick-bed-facing-camera.png` |
| `char-yuan-block.png` | 冷靜擋在中間 | 米白襯衫袖捲＋橄欖褲＋**棕色樂福鞋**；**面向左**；一臂前伸開掌擋／護（對左側鄰居） | **僅** S06 選「往前半步擋住」；梯廳外出裝；勿再當空手站姿暫代 |
| `char-yuan-door-hold.png` | 扶門、還沒擋 | 米白襯衫袖捲＋橄欖褲＋**棕色樂福鞋**；**面向左**；一手抬到胸前像扶著門沿，低頭看狗；**不畫狗** | **S06 梯廳**開場～選前／選 C 回到門邊；外出裝＋鞋。勿用室內襪／拖鞋 |
| `char-yuan-leash.png` | 蹲等／耐心 | 米白襯衫＋橄欖褲＋**棕色平底鞋／樂福**；側蹲；手握**棕色皮牽繩**下垂；**面向左** | S08 玄關穿帶／返家／樹下停等；S09 玄關。與 `walk` 同衣櫃＋鞋。尺：玄關 **0.33**、巷口樹下仍 alley **0.32**（`CHAR_POSE_SCALE` 1.0，勿再縮）。舊中跟稿在 `assets/char/_work/` |
| `char-yuan-walk.png` | 巷口散步 | 米白襯衫＋橄欖褲；**站姿走路**握牽繩；**面向左**；無狗同框 | **S08 巷口**（非蹲）；`char_right_walk` **0.32** |
| `char-yuan-leash-pass.png` | 交繩／收回 | 站姿；**僅予安雙手**握牽繩握把（**禁**對方伸入畫面的手） | **S09** 硬分歧（期間勿疊同事全身） |
| `char-yuan-farewell.png` | 告別／攤手 | **室內裝**＋襪；單膝下跪；手掌攤開**無牽繩**；圖檔**面向左**（遊戲內 `xzoom` 翻成面右對狗） | S09 客廳 |
| `char-yuan-cafe.png` | 交接衝突 | 米白襯衫＋橄欖褲；**站姿**握牽繩；**面向左**（對同事／狗） | S09 咖啡廳 |
| `char-clerk.png` | 禮貌微笑 | 年輕男店員；深藍短袖＋深色圍裙＋深褲 | S01／S02；`char_convenience` zoom 0.29（勿套客廳 `char_left`） |
| `char-neighbor.png` | 熱心伸手 | 中年女鄰居；綠卡迪＋米上衣；**面向右**伸手（對右側予安／狗） | S06 伸手要摸 |
| `char-neighbor-idle.png` | 剛看見養狗 | 同上服裝；雙手自然垂著；**面向右**看狗 | S06 開場／問完後 |
| `char-neighbor-lower.png` | 先讓牠聞 | 同上服裝；彎腰、手放到膝小腿高度 | S06「聞一下就好」／讓摸 |
| `char-neighbor-withdraw.png` | 把手收回 | 同上服裝；右手收到胸前 | S06 選 A 擋人之後 |
| `char-coworker.png` | 真誠提議 | 年輕女同事；淡紫開襟＋米內搭＋炭灰褲；一手前伸 | S09 茶水間 |
| `char-coworker-cafe.png` | 蹲等聞狗 | 同上服裝；**蹲姿側身**；手留膝上／低伸；**面向右**（對女主／狗） | S09 咖啡廳 |

**站位慣例：** 予安多在 `char_right`／`char_chair`（S04 面左看狗）；**S05** 予安在 `char_chair_left`（面右），狗用 `dog_near`／`mid`／`far`（不翻轉、面左）。其餘需人狗互視時，狗用 `dog_*_to_yuan` 或 `dog_chair_*`（水平翻轉面右）。合成圖（`carry_pup`／`leash_pass`／`nose_tip`）同框時先 `hide` 另一層，避免雙重手／雙重狗。S02 對景尺（門／機車／路）見 `image_bg.md` §5／§9。

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

### 同事・咖啡廳（coworker-cafe）

```text
Same coworker identity. Crouched / kneeling sideways at cafe entrance, body angled toward Yuan and the puppy on her right, one hand resting calmly on knee, other hand open low near the ground without grabbing. Empathetic patient expression. Full body. SOLID FLAT BLACK background. NOT the same face as Yuan.
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
| 2026-07-25 | 建立本檔；備份 `assets/_backup_unused/_backup_20260725_193450/`；以現有 7 張為錨重寫 IDENTITY／STYLE；全量重產 |
| 2026-07-28 | 新增 `char-yuan-farewell`／`char-yuan-cafe`／`char-coworker-cafe`；S09 朝向寫入 pose 表 |
| 2026-08-13 | 新增 `char-yuan-home-stand`／`char-yuan-paper-bag`；`leash-pass` 重產去除對方伸入的手 |
| 2026-09-06 | 室內裝統一：`home-sit`／`home-stand`／`sofa`／`farewell` 不穿鞋；S05 另產 `headphones-sit`；辦公室站姿耳機圖保留 |
| 2026-09-10 | S06 梯廳予安改外出裝＋樂福鞋（`door-hold`／`block` 與 cafe／carry 同衣櫃）；室內襪只留玄關 `home-stand`；`carry_pup` CHAR_POSE_SCALE 1.056 對齊鄰居身高 |
| 2026-09-13 | S07 病床改沿床躺、面向左看狗；`char_bedroom` 0.18／xalign 0.78／ypos 0.76 |
| 2026-09-13 | S07 辦公室尾鉤不顯示予安；改 overlay 手機門邊照 |
| 2026-09-13 | S08 人尺確認：`leash`／`walk` CHAR_POSE_SCALE 1.0；玄關 0.33、巷口 0.32；勿為蹲姿再縮 |

---

*更新：2026-09-13｜S07 病床沿床躺看狗；`char_bedroom` 0.18／ypos 0.76*
