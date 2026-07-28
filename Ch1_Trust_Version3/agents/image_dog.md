# Version3｜狗外型鎖定｜image_dog.md

> 對齊：`game_guild.md` · `image.md` · `outline_trilogy_ch1_10sections.md`  
> **定稿：** Option **B｜wiry**  
> **基準參考：** `assets/dog/dog-ref-canonical.png`（之後所有 pose 必須像同一隻）  
> **風格錨點（2026-07-25 用戶定稿）：** `assets/dog/refs/`（`ref-anxious-*`／`ref-side-profile`／`ref-behind-legs`／`ref-refuse-stranger`）  
> 預設名：**小7**（超商暱稱）；玩家可改 → `dogLabel(s)`；圖檔**勿寫死狗名**。  
> 落選候選 A／C／D 與暫存 `dog-option-*.png` **已刪除**，勿再引用。  
> **生圖順序：** 先用 Cursor `GenerateImage`（必附 `dog-ref-canonical.png` ＋至少一張 `refs/`）；FLUX 僅備援。

---

## 0. 一致性原則（必讀）

| 規則 | 說明 |
|------|------|
| **同一隻** | 毛色區塊、耳形、眼型、體型比例跨 pose **不得漂移** |
| **軟分軌** | 高低信任**只改 pose／距離／表情**，不換外型、不換品種感 |
| **分層** | 狗 PNG **獨立疊層**；勿畫進背景 |
| **禁純種** | 不得畫成柯基／貴賓／柴／哈士奇等可辨純種 |
| **禁寫字** | 無文字、logo、信任 HUD／數字 |

產新 pose 前：先對照 `dog-ref-canonical.png` 與 `assets/dog/refs/`，再貼下方 **IDENTITY LOCK**。

---

## 1. 定稿外型（Option B｜wiry｜2026-07-25 錨點）

### 1.1 身分卡

| 項目 | 鎖定 |
|------|------|
| 代號 | **B｜wiry** |
| 品種感 | 台灣常見 **scruffy / wiry mixed breed**（略像 Border／㹴混，但**非純種㹴**） |
| 年齡 | **約 2～3 個月** 幼犬（compact puppy，非壯年） |
| 體型 | **短腿、結實偏瘦**；街犬幼崽感；寫實幼犬比例（非 Q 版） |
| 頭臉 | 略角／精實吻；吻周與眉際 **wiry 鬍鬚感**；表情可讀「靈魂大眼」 |
| 耳 | **軟垂 V 耳**貼頭；耳緣與耳尖 **深褐～栗褐** |
| 眼 | **大而暖的深褐**；明顯 catchlight；可擔憂／警戒／求護衛 |
| 鼻 | 小而濕潤的 **黑鼻** |
| 毛質 | **短～中、硬毛／wiry、略亂**；筆觸粗厚（impasto 團塊），非絲滑細毛 |
| 毛色 | 主色 **honey gold / golden-tan**；背脊 **grizzled darker saddle**；耳尖深褐；吻周／胸口偏 **cream～淺蜜** |
| 尾 | 中短、自然下垂或微捲；隨情緒動 |

### 1.2 毛色區塊（不可改）

```text
主體：honey-gold / golden-tan
耳尖＋耳緣＋背脊 saddle：deeper chestnut / dark brown grizzle
胸口＋吻部周圍＋腳掌前緣：cream / light tan
鼻：black
眼：warm dark brown + catchlight
```

### 1.3 畫風錨點（對齊用戶定稿圖）

```text
Thick-impasto impressionistic oil painting of ONE puppy.
Heavy tactile brushstrokes; fur as chunky paint clumps, not fine strand realism.
Soft directional warm key light from above-left; dark studio isolation.
Subject centered on SOLID FLAT BLACK (#000000) background for cutout.
Not a photograph, not anime, not chibi, not smooth 3D render.
```

### 1.4 與落選方案的差別（勿混用）

| 代號 | 勿做成（落選，檔案已刪） |
|------|--------------------------|
| A fluffy | 過蓬、過圓、貴賓感 |
| C round | 過圓臉、過密毛、偏 Q／貼圖感 |
| D slender | 過修長優雅、站姿模特兒感 |

**B 的關鍵詞：** wiry、scruffy、impasto、honey-tan、dark-tipped floppy ears、grizzled saddle、soulful dark-brown eyes、black studio bg。

---

## 2. IDENTITY LOCK（每張狗圖必貼）

生圖時把整段貼在 STYLE 之後、POSE 之前：

```text
SAME PUPPY IDENTITY LOCK (Option B wiry — MUST match dog-ref-canonical.png and assets/dog/refs/):
One continuous character across all poses. About 2-3 months old Taiwanese scruffy wiry mixed-breed puppy (not purebred terrier, not corgi, not poodle, not shiba, not husky). Compact short-legged puppy body, slightly thin street-puppy build. Wiry short-to-medium messy coat rendered as thick impasto paint clumps. Honey golden-tan fur; darker chestnut-brown floppy ear tips and a grizzled darker saddle along the back; cream-light tan muzzle area and chest. Soft V-shaped floppy ears close to the head. Large round warm dark-brown eyes with catchlights (soulful "puppy-dog eyes" when looking up). Small wet black nose. Slightly angular scruffy street-puppy face with wiry brow and muzzle whiskers (NOT round plush face, NOT fluffy show-dog coat, NOT slender elegant silhouette). Thick-impasto impressionistic oil painting. Believable puppy proportions. No text, no logo, no name tag, no trust HUD.
```

### STYLE（與 image.md 一致 · 對齊用戶錨點）

```text
Thick-impasto impressionistic oil painting. Heavy visible brushstrokes, painterly impasto texture, soft blended edges, tactile canvas tooth. Warm amber key light from above-left. Soft atmospheric depth, storybook concept-art feel. Not a photograph, not DSLR realism, not anime cel shading, not hard black outlines, not chibi, not flat vector, not smooth 3D.
```

### 去背底板

```text
Centered full body (or clearly readable crop). SOLID FLAT BLACK (#000000) background for cutout. No floor plane, no scenery, no props unless the pose requires a minimal prop (shoe / wire / partial human lower leg / harness).
```

落地後執行：`python tools/remove_ai_bg.py INPUT OUTPUT`

---

## 3. Pose 產出契約

| 規則 | 說明 |
|------|------|
| 表情＋動作 | **每張**必須同時改：耳／眼／嘴／尾／身體姿勢 |
| 信任可讀 | 低信任＝遠／貼牆／僵／耳平；高信任＝近／貼腿／背對睡 |
| 檔名 | `dog-{pose}.png`（例：`dog-anxious.png`）；**無 Week 子資料夾** |
| 路徑 | `Ch1_Trust_Version3/assets/dog/` |
| 禁 | 同 pose 別名濫竽充數；禁把狗嵌進 bg |

### Pose 表（對齊 image.md §6.2）

| 檔名 | 表情 | 動作 | 主用 | 錨點 |
|------|------|------|------|------|
| `dog-ref-canonical.png` | 中性側臉 | 全身側立母版 | 外型基準 | `refs/ref-side-profile` |
| `dog-anxious.png` | 擔憂上望 | 低趴、下巴貼前爪 | S02／低信任 | `refs/ref-anxious-*` |
| `dog-halfstep.png` | 警戒好奇 | 「既不碰你、也不放你走」的半步 | S02 記憶 | 生成 |
| `dog-stair-watch.png` | 警戒 | 靠牆、面向門口方向 | S03 | 生成 |
| `dog-door-sleep.png` | 睏但守門 | 睡在房門外 | S03 鉤子 | 生成 |
| `dog-parallel.png` | 放鬆一點 | 兩步遠地板、下巴貼地 | S04 | 生成 |
| `dog-kitchen-door.png` | 跟隨觀望 | 停在廚房門檻外 | S04 記憶 | 生成 |
| `dog-ear-flat.png` | 被尖聲嚇到 | 耳平、退 | S05 Tone− | 生成 |
| `dog-sniff-wire.png` | 好奇 | 嗅耳機線 | S05 鉤子 | 生成 |
| `dog-behind-legs.png` | 求護衛 | 縮身躲藏 peek | S06 | `refs/ref-behind-legs` |
| `dog-forehead-nudge.png` | 輕謝 | 額頭頂小腿 | S06 記憶 | 生成 |
| `dog-guard-door.png` | 不安守門 | 趴房門口 | S07 | 生成 |
| `dog-street-tense.png` | 繃緊 | 貼牆／僵住 | S08 低 | 生成 |
| `dog-leash-wait.png` | 累但信任 | 胸背帶、停步等待 | S08 高；S09 玄關 | 生成 |
| `dog-shoe-sleep.png` | 安心 | 靠燕麥灰平底鞋邊睡 | S08 記憶 | 生成 |
| `dog-farewell.png` | 告別上望 | 坐姿抬頭（無牽繩／無胸背帶） | S09 客廳 | 生成 |
| `dog-cafe-refuse.png` | 拒絕警告 | 胸背帶＋牽繩、貼腳對伸手僵 | S09 咖啡廳 | 生成 |
| `dog-cafe-tense.png` | 兩人中間僵 | 僵住、面向認得的人 | S09 咖啡廳低信任 | 生成 |
| `dog-refuse-stranger.png` | 拒絕 | 胸背帶＋牽繩、低蹲對伸手僵 | S09 fallback | `refs/ref-refuse-stranger` |
| `dog-back-sleep.png` | 信任落地 | **背對**睡在伸手可及處 | 結局 A | 生成 |
| `dog-check-sleep.png` | 選定仍學 | 睡近但睜眼確認 | 結局 B | 生成 |
| `dog-door-edge.png` | 薄冰 | 睡門邊、不看人 | 結局 D | 生成 |

---

## 4. 完整 Prompt 模板（複製）

```text
{STYLE}

{IDENTITY LOCK — Option B wiry}

{POSE_AND_EXPRESSION — change BOTH body action AND facial expression;
 convey trust distance: retreat / half-step / parallel rest / back-to-back sleep}

Centered, readable full body or clear crop. SOLID FLAT BLACK (#000000) background for cutout.
No bird nest, no straw nest, no cardboard nest styling on the dog itself.
No text, no logo, no purebred markers, no trust meter UI.
```

### Cursor GenerateImage 注意

- `reference_image_paths` 必含：`assets/dog/dog-ref-canonical.png`，建議再加 `assets/dog/refs/ref-anxious-b.png`
- `aspect_ratio`：直式 pose 用 `"3:4"`；橫躺可用 `"4:3"`
- 產完 → `python tools/remove_ai_bg.py …` → 覆蓋 `assets/dog/dog-{pose}.png`

---

## 5. 一致性審查清單（定稿前打勾）

- [ ] 對得上 `dog-ref-canonical.png` 與 `assets/dog/refs/`（同一隻 B）
- [ ] 蜂蜜褐主體＋深耳尖＋背脊 grizzle＋奶油吻周仍在
- [ ] 毛質仍是 **wiry／scruffy＋厚 impasto**，未漂成蓬毛或光滑短毛
- [ ] 仍是短腿幼犬，未變壯年犬／Q 版
- [ ] 耳為軟垂，非尖直立雙耳純種感
- [ ] 大深褐眼＋catchlight 仍在
- [ ] 表情與身體動作都有改（不是只換背景）
- [ ] 無文字／logo／信任數字
- [ ] 狗為獨立透明 PNG，未嵌進 bg
- [ ] 未自動開遊戲

### 不一致時怎麼辦

1. 重貼 **IDENTITY LOCK**＋明確寫 `must match dog-ref-canonical.png and refs/`  
2. 加 `--no`：`fluffy coat, round plush face, purebred, chibi, photorealistic, cream background`  
3. 仍漂＝用基準圖做 img2img／edit，只改 pose

---

## 6. 與其他檔的關係

| 檔案 | 職責 |
|------|------|
| **本檔 `image_dog.md`** | 小7 **外型鎖定＋pose 一致性** |
| `image.md` | 總美術規範、人物／背景／STYLE |
| `image_bg.md` | 背景 place／light；**背景無人無狗** |
| `game_guild.md` | 信任體感用距離／睡姿表達，不顯示數字 |

`image.md` 的狗章節以本檔為準；衝突時以 **本檔 Option B** 為準。

---

## 7. 變更紀錄

| 日期 | 內容 |
|------|------|
| 2026-07-19 | Option B wiry 定稿；正式狗資產 |
| 2026-07-25 | 用戶提供 5 張錨點圖 → 備份至 `assets/dog/_backup_20260725_183542/`；重寫 IDENTITY／STYLE；落地 canonical／anxious／behind-legs／refuse-stranger；其餘 pose 依新鎖全量重產 |
| 2026-07-28 | 新增 `dog-farewell`／`dog-cafe-refuse`／`dog-cafe-tense`；S09 朝向見 `section_09_almost_handoff.md` |

---

*更新：2026-07-28｜S09 告別／咖啡廳狗姿；Option B 錨點鎖定見 2026-07-25*
