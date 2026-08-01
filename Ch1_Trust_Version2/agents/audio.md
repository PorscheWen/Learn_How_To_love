# Version2 音樂／音效對照｜audio

> 對齊：`plot.md` · `image_bg.md` · 各日 `week0/dayN_*.md`  
> 資產路徑：`Ch1_Trust_Version2/assets/audio/`（Ren'Py `game/assets/audio` 為 junction）  
> 授權明細：[`../assets/audio/CREDITS.md`](../assets/audio/CREDITS.md) · 幼犬聲：[`../assets/audio/sfx/CREDITS.md`](../assets/audio/sfx/CREDITS.md)  
> 原則：**僅 BGM（OGG loop）＋稀疏幼犬 one-shot**；不加雨聲／環境 loop／合成 whimper。

---

## 1. 已 bunded BGM（實體檔）

| 檔案 | Profile 名 | 情緒 | 建議用途 |
|------|------------|------|----------|
| `warm.ogg` | `warm` | 暖、安定、室內日常 | 客廳日間、餵食後、日終陪伴、希望收束 |
| `calm.ogg` | `calm` | 安靜、沉、略緊 | 深夜、雨夜室內、衝突後冷靜、緊張但不 jump scare |
| `tender.ogg` | `tender` | 柔軟鋼琴、靠近 | 信任拉近、道歉後、取名／羈絆時刻 |
| `melancholy.ogg` | `melancholy` | 低沉開場、雨天孤獨 | **僅**雨夜巷口／開場發現紙箱 |

### Profile 別名（劇本日終表 → 實體檔）

劇本檢查表用敘事名；落地時改成左欄 Profile，對應右欄 OGG：

| 劇本標籤（日終表） | Profile | OGG | 備註 |
|--------------------|---------|-----|------|
| `rain_soft` | `melancholy` | `melancholy.ogg` | Day1 開場雨巷 |
| `awkward_day` | `calm` | `calm.ogg` | Day2 混亂清晨 |
| `shop_bustle` | `warm` | `warm.ogg` | Day3 寵物店（無 bustle SFX，只用暖日常） |
| `night_thin` | `calm` | `calm.ogg` | Day4 半夜哭聲（可降速 0.93） |
| `soft_growth` | `tender` | `tender.ogg` | Day5 主動靠近 |
| `tension_soft` | `calm` | `calm.ogg` | Day6 咬線衝突（禁 jump scare） |
| `clinic_soft` | `calm` | `calm.ogg` | Day7 診所／路程 |
| `warm_quiet` | `warm` | `warm.ogg` | 多數日終收束 |
| `ending_warm` | `warm`／`tender` | `warm.ogg`／`tender.ogg` | Day7 正式收養／溫暖結局 |
| `ending_quiet` | `tender` | `tender.ogg` | Day7 安靜羈絆結局 |

**擴充別名（可選，仍映射既有 OGG）：**

| Profile | OGG | 用途 |
|---------|-----|------|
| `hopeful` | `warm.ogg`（略升音量） | Day7 責任清單通過後 |
| `sunny` | `warm.ogg` | 陽台／日間外出 |
| `sunset` | `tender.ogg` | 傍晚趕回家 |
| `night` | `calm.ogg` @0.93 | 深夜就寢 |
| `tense` | `calm.ogg` @0.88 | 衝突當下（短） |
| `storm` | `calm.ogg` @0.85 | 未來雷雨日（Version2 Week0 暫無） |

---

## 2. 背景（place／light）→ 預設 BGM

對齊 `image_bg.md` 的 `bg-{place}-{light}`。場景未特別標 `music` 時用此表；**劇情情緒優先於背景**（例：客廳日間若正在吵架 → `calm`／`tense`，勿硬塞 `warm`）。

| bg | 時段感覺 | 預設 Profile | OGG |
|----|----------|--------------|-----|
| `bg-street-night` | 雨夜巷口、趕路 | `melancholy` → 進家後 `warm`／`calm` | `melancholy.ogg` → `warm.ogg`／`calm.ogg` |
| `bg-living-night` | 夜客廳、第一夜、日終 | `warm`（陪伴）／`calm`（焦慮夜） | `warm.ogg`／`calm.ogg` |
| `bg-living-day` | 清晨～午後客廳 | `warm`；混亂清晨用 `calm` | `warm.ogg`／`calm.ogg` |
| `bg-petshop-day` | 店內補給 | `warm` | `warm.ogg` |
| `bg-entrance-night` | 玄關／陽台夜 | `tender`／`warm` | `tender.ogg`／`warm.ogg` |

### 情緒覆寫規則

| 劇情情緒 | Profile | 例 |
|----------|---------|-----|
| 開場孤獨／雨天發現 | `melancholy` | `d1_street_rain` |
| 手忙腳亂但安全室內 | `warm` | Day1 擦乾後、餵食 |
| 混亂／崩潰邊緣 | `calm` | Day2 發現便便 |
| 靠近／信任成長 | `tender` | Day5 聞手摸背 |
| 衝突／咬壞東西 | `calm`（`tense`） | Day6 當下 |
| 道歉後／和解 | `tender` → `warm` | Day6 後半 |
| 診所緊張 | `calm` | Day7 路程／候診 |
| 正式取名／收養收束 | `tender`／`warm` | Day7 ending |

---

## 3. Week0 逐日 BGM 班表

每天：**開場曲 →（中段可換）→ 日終曲**。同一天內換曲用 fade crossfade（約 1.5～2.5s），勿硬切。

### Day1｜雨天的紙箱（相遇）

弧線：`melancholy` → `warm`

| 場景 ID | bg | Profile | 說明 |
|---------|-----|---------|------|
| `d1_street_rain` | `bg-street-night` | `melancholy` | 雨夜紙箱開場 |
| `d1_choice_carry` | `bg-street-night` | `melancholy` | 仍在巷口 |
| `d1_carry_home` | `bg-living-night` | `warm` | 進家後轉暖 |
| `d1_kg_first_aid`～`d1_choice_approach` | `bg-living-night` | `warm` | 照顧／餵食 |
| `d1_choice_sleep`～`d1_night_box` | `bg-living-night` | `warm`（`warm_quiet`） | 第一夜 |

### Day2｜混亂的客廳（混亂）

弧線：`calm` → `warm`

| 場景 ID | bg | Profile | 說明 |
|---------|-----|---------|------|
| `d2_morning_mess`～`d2_choice_react` | `bg-living-day` | `calm` | 清晨意外 |
| `d2_kg_potty`～`d2_choice_pad` | `bg-living-day` | `calm` → `warm` | 清潔後可漸暖 |
| `d2_tg_soft_voice` | `bg-living-day` | `tender` | 溫柔聲信任遊戲 |
| `d2_naming` | day／night | `tender` | 取名時刻 |
| `d2_day_end` | `bg-living-night` | `warm` | 日終 |

### Day3｜第一次出門買東西（磨合）

弧線：`warm`（店）→ `warm`／`tender`（換碗）

| 場景 ID | bg（建議） | Profile | 說明 |
|---------|------------|---------|------|
| `d3_empty_can` | `bg-living-day` | `warm` | 罐頭見底 |
| `d3_to_shop` | `bg-street-day` | `warm` | 日間巷口路程 |
| `d3_petshop_enter`～`d3_choice_toys` | `bg-petshop-day` | `warm` | 店內（`shop_bustle`→warm）＋阿姨 |
| `d3_checkout` | `bg-petshop-day` | `warm` | 結帳妹妹 |
| `d3_return_home`～`d3_choice_bowl` | `bg-living-day` | `warm`／`tender` | 新舊碗並排 |
| `d3_day_end` | `bg-living-night` | `warm` | 日終 |

### Day4｜半夜的哭聲（磨合低潮）

弧線：`calm`（夜）→ `tender`（陪睡）→ `warm`（天亮）

| 場景 ID | Profile | 說明 |
|---------|---------|------|
| `d4_bedtime`～`d4_whine_up` | `calm`（`night`） | 關門後哭聲 |
| `d4_choice_response`～`d4_tg_visible_sleep` | `calm` → `tender` | 安撫／可見距離 |
| `d4_dawn`～`d4_choice_morning` | `warm` | 天亮 |
| `d4_day_end` | `warm` | 日終 |

### Day5｜牠肯靠近一點（成長）

弧線：`tender` → `warm`

| 場景 ID | Profile | 說明 |
|---------|---------|------|
| `d5_afternoon_light`～`d5_approaches` | `tender` | 午後靠近 |
| `d5_choice_react`～`d5_tg_sniff_pet` | `tender` | 身體語言／聞手 |
| `d5_choice_touch`～`d5_choice_ritual` | `tender`／`warm` | 儀式感 |
| `d5_day_end` | `warm` | 日終 |

### Day6｜小意外與道歉（成長）

弧線：`calm`（衝突）→ `tender`（道歉）→ `warm`

| 場景 ID | Profile | 說明 |
|---------|---------|------|
| `d6_chewed_cord`～`d6_choice_words` | `calm`（`tense`） | 咬線當下 |
| `d6_kg_chew`～`d6_tg_trade` | `calm` → `tender` | 學習／交換玩具 |
| `d6_choice_after`～`d6_choice_night` | `tender`／`warm` | 和解後 |
| `d6_day_end` | `warm` | 日終 |

### Day7｜紙箱以外的名字（羈絆）

弧線：`warm` → `calm`（診所）→ `tender`／`warm`（結局）

| 場景 ID | Profile | 說明 |
|---------|---------|------|
| `d7_box_to_balcony`～`d7_kg_checklist` | `warm`／`hopeful` | 責任清單 |
| `d7_to_clinic`～`d7_tg_clinic` | `calm`（`clinic_soft`） | 路程／安撫 |
| `d7_choice_adopt` | `tender` | 是否正式留下 |
| `d7_home_again`～`d7_choice_name` | `tender` | 回家／名字 |
| `d7_ending` | `ending_warm`→`warm` 或 `ending_quiet`→`tender` | 依信任／選項 |

---

## 4. 幼犬 SFX（稀疏 one-shot）

路徑：`assets/audio/sfx/`（及 `sfx/dog/`）。**有狗在場的關鍵 beat 才播一次**；日常過場可只留 BGM。

| 情緒／beat | 建議 cue 池 | 檔案例 |
|------------|-------------|--------|
| 雨夜紙箱害怕 | whimper／murmur | `puppy-whimper-*.wav`、`puppy-murmur-*.wav` |
| 輕聲不安 | soft／sigh | `puppy-soft-*.wav`、`puppy-sigh-*.wav` |
| 開心／玩耍 | yip／excited／bark | `puppy-yip*`、`puppy-excited-*`、`puppy-bark-*` |
| 警戒／低哼 | growl／grumble | `dog-growl.ogg`、`sfx/dog/dog-*.flac` |
| 入睡 | （程序化或極輕 sigh） | 勿連續 loop |

**禁止（Version2 基線）：** weather 雨聲疊層、連續 ambient dog loop、合成 whimper。

---

## 5. Ren'Py 落地約定

```renpy
## audio.rpy
$ play_bgm("melancholy")   # 換 BGM（同 profile 不重播）
$ dog_sfx("whimper")       # 幼犬 one-shot
```

| 函式 | 用途 |
|------|------|
| `play_bgm(profile)` | `melancholy`／`warm`／`calm`／`tender`（含劇本別名） |
| `dog_sfx(cue)` | `whimper`／`murmur`／`soft`／`sigh`／`yip`／`excited`／`bark`／`growl` |
| `stop_bgm()` | 停止 BGM |

- 檔案：`Renpy_game/game/audio.rpy`；資產經 junction → `assets/audio/`
- 主選單 BGM：目前靜音（`config.main_menu_music = None`）

### Day1～3 已落地 cue（稀疏）

| Day | BGM 弧線 | 狗聲關鍵 beat |
|-----|----------|---------------|
| 1 | melancholy → warm | 紙箱 murmur／whimper；抓出／擦乾／餵食／就寢 |
| 2 | calm → tender → warm | 清晨 mess；罵／深呼吸；清潔；溫柔聲；取名 yip |
| 3 | warm → shop_bustle → tender → warm | 空罐；回家 murmur；換碗；日終 sigh |

---

## 6. 撰寫／審查清單

- [ ] 新場景有標 `music`（或可從 bg＋情緒推得）
- [ ] 開場雨巷用 `melancholy`，進家後有 crossfade 離開
- [ ] 同一天內勿每 30 秒換曲；建議 **2～3 次** 情緒節點才換
- [ ] 衝突用 `calm`／`tense`，不用恐怖／鼓點 jump scare
- [ ] 日終多落在 `warm` 或 `tender`
- [ ] 新 OGG 必須更新 `assets/audio/CREDITS.md`
- [ ] 狗在場關鍵 beat 才加 SFX；無狗不播幼犬聲

---

## 7. 新增曲目流程

1. 下載／匯出 **OGG**（建議 48kHz、可 seamless loop）。
2. 存成 `assets/audio/{profile}.ogg`。
3. 在本檔 §1 登記 Profile，並更新 `CREDITS.md`。
4. 更新本檔 Week0 班表或 bg 預設表。
5. Ren'Py：`define audio.bgm_*` 後於場景 `play music`。

推薦擴充（CC0，見 CREDITS）：Yoiyami First Light Particles、Playful Piano 等——**先登記再替換**，勿默默覆蓋既有四曲。

---

*更新：2026-07-12｜Week0 對照；Day1～3 Ren'Py 已落地 BGM＋幼犬 SFX*
