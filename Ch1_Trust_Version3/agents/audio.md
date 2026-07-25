# Version3 音樂／音效對照｜audio

> 對齊：`game_guild.md` · `image_bg.md` · `image_dog.md` · `outline_trilogy_ch1_10sections.md` · `section_*.md`  
> 資產路徑：`Ch1_Trust_Version3/assets/audio/`（可沿用／複製 V2 四曲 OGG）  
> 授權：專案 `assets/audio/CREDITS.md` · 幼犬聲：`assets/audio/sfx/CREDITS.md`  
> 原則：**僅 BGM（OGG loop）＋稀疏幼犬 one-shot**；不加雨聲／環境 loop／合成 whimper。  
> 畫面：**不播「升級叮」類信任 HUD 音**（對齊 guild 不顯示數字）。  
> 狗 SFX 對應 pose 時，外型仍須為 **Option B｜wiry**（見 `image_dog.md`）。

---

## 0. 與 game_guild 對齊（節奏）

| guild 規則 | 音訊落地 |
|------------|----------|
| 整章 60～85 分／十段 | 每段約 **1～2 次**換曲；整章約 **8～14 次** crossfade，勿每選項換 |
| 開場 ≤15 分（S01＋S02） | S01 `calm`／空白感 → S02 相遇可短暫 `melancholy` → 帶走後 `warm`／`tender` |
| 軟分軌 | **同 bg 不強制換 BGM**；高低信任用狗 SFX／pose，不另開 BGM 線 |
| 硬分歧 S09／S10 | 結局 A／B → `tender`／`warm`；C → `melancholy`／`calm`；D → `calm` |
| 無 Game Over | C／D **不**播失敗／懲罰音效 |

### 0.1 電影化節奏的音訊限制

- BGM 切換只綁定 Section 進場、關鍵動作、選項後情緒轉折或離場收束，不因每句旁白換曲。
- 驚嚇或壓力可短暫切 `tense`，但事件結束後須依反應回到 `calm`、`tender` 或 `warm`，避免整段持續壓迫。
- 軟分軌仍以狗 pose、`far／mid／near`、文字呼吸與稀疏 one-shot 為主；只有情緒方向真正改變時才換 BGM。
- `pause` 是畫面節奏，不等於加入環境音；停頓期間維持既有 BGM，禁止補雨聲、街聲或 ambient loop 填滿留白。
- 同一個信任拍原則上只設一個主要音樂轉折。S02 與 S08 是四拍演出樣板，不代表所有 Section 都必須增加換曲次數。

自然存檔點（場次）可讓 BGM 在邊界自然收束一拍：

| 場次 | 範圍 | 建議收束 Profile |
|------|------|------------------|
| A | S01～S04 | `warm`（平行安靜成立） |
| B | S05～S08 | `tender` 或 `warm`（鞋邊睡） |
| C | S09～S10 | 依結局（見 §3.10） |

---

## 1. 已 bundled BGM（實體檔）

| 檔案 | Profile 名 | 情緒 | Version3 建議用途 |
|------|------------|------|-------------------|
| `warm.ogg` | `warm` | 暖、安定、室內日常 | 客廳平行安靜、照顧後、日終、「晚上見」 |
| `calm.ogg` | `calm` | 安靜、沉、略緊 | S01 空白加班夜、S05 會議尖、S07 生病、薄冰 D |
| `tender.ogg` | `tender` | 柔軟、靠近 | 蹲等半步、護衛後、留下確認、結局 A／B |
| `melancholy.ogg` | `melancholy` | 低沉、孤獨 | **S02 後門一瞥**、結局 C 送走；勿整章濫用 |
| `sick-guard.ogg` | `sick_guard` | 深夜、脆弱、守候 | S07 生病守門，避免與 S03／S05 共用同一首 |
| `almost-gave.ogg` | `almost_gave` | 沉靜、猶豫、情緒高峰 | S09 理性清單與咖啡廳交接前 |
| `first-light.ogg` | `hopeful` | 淡光、承認留下 | 結局 A 掛勾與「再試一年」 |

### Profile 別名（劇本 → 實體）

| 劇本標籤 | Profile | OGG | 備註 |
|----------|---------|-----|------|
| `blank_night` | `calm` | `calm.ogg` | S01 一個人剛剛好 |
| `backdoor_glance` | `melancholy` | `melancholy.ogg` | S02 相遇 |
| `gate_border` | `calm` | `calm.ogg` | S03 大門 |
| `stair_border` | `calm` | `calm.ogg` | 舊別名（仍可用） |
| `shared_quiet` | `warm` | `warm.ogg` | S04 平行安靜 |
| `two_voices` | `calm` → `tender` | 兩曲 | S05 尖→低 |
| `guard_corridor` | `tender`／`calm` | | S06 護衛／尷尬 |
| `sick_guard` | 深夜 ambient → `tender` | `sick-guard.ogg` | S07 |
| `corner_walk` | `warm`／`calm` | | S08；硬拖用 `calm`@0.88 |
| `almost_gave` | 沉靜 ambient → 分歧 | `almost-gave.ogg` | S09 |
| `ending_back` | `tender` | `tender.ogg` | 結局 A |
| `ending_learning` | `warm`／`tender` | | 結局 B |
| `ending_handover` | `melancholy` | `melancholy.ogg` | 結局 C |
| `ending_thin_ice` | `calm` | `calm.ogg` | 結局 D |

**擴充別名（仍映射既有 OGG）：**

| Profile | OGG | 用途 |
|---------|-----|------|
| `night` | `calm.ogg` @0.93 | 深夜就寢 |
| `tense` | `calm.ogg` @0.88 | 衝突當下（短；禁 jump scare） |
| `sunset` | `tender.ogg` | 傍晚帶回／進門 |
| `hopeful` | `first-light.ogg` | S10 掛勾／「再試一年」 |

---

## 2. 背景（place／light）→ 預設 BGM

對齊 `image_bg.md` 的 `bg-{place}-{light}`。未標 `music` 時用此表；**劇情情緒優先於背景**。

| bg | 時段感覺 | 預設 Profile | OGG |
|----|----------|--------------|-----|
| `bg-office-night` | 加班空白 | `calm` | `calm.ogg` |
| `bg-convenience-night` | 超商夜 | `calm`；店員鉤子後可維持 | `calm.ogg` |
| `bg-backdoor-night` | **S02 相遇** | `melancholy` → 帶走後 `tender`／`warm` | `melancholy` → `tender`／`warm` |
| `bg-stairwell-night` | S03 臨時國界 | `calm`；「我還在」→ `tender` | `calm`／`tender` |
| `bg-living-night` | 夜客廳、S07、S10 | `warm`（陪伴）／`calm`（焦慮／薄冰） | `warm`／`calm` |
| `bg-living-day` | S04／S05 | `warm`；會議尖用 `calm` | `warm`／`calm` |
| `bg-kitchen-day` | 門口跟隨 | 繼承 living；靠近用 `tender` | — |
| `bg-entrance-night` | 進門過渡 | `tender`／`warm` | `tender`／`warm` |
| `bg-corridor-day` | S06 被看見 | `calm`；擋下後 `tender` | `calm`／`tender` |
| `bg-alley-day` | S08 巷口 | `warm`；僵住／硬拖 `calm`（`tense`） | `warm`／`calm` |
| `bg-cafe-day` | S09 差點送走 | `calm`；留下→`tender`；送走→`melancholy` | 分歧 |
| `bg-street-night` | 通勤（若用） | `calm`／`melancholy` | 勿搶 S02 後門主軸 |

### 情緒覆寫規則

| 劇情情緒 | Profile | Section 例 |
|----------|---------|------------|
| 一個人剛剛好／空白 | `calm` | S01 |
| 後門發現／沒能假裝沒看見 | `melancholy` | S02 開場 |
| 蹲等、半步、溫柔抱走 | `tender` | S02 A |
| 腳趕／硬抓／關浴室 | `calm`（`tense`）短 | Dist− |
| 平行安靜成立 | `warm` | S04 |
| 會議尖聲／甩開 | `calm` | S05 Tone− |
| 脫耳機、嗅線 | `tender` | S05 鉤子 |
| 走廊擋人、額頭頂腿 | `tender` | S06 |
| 生病守門 | `calm` → `tender` | S07 |
| 牽繩停等／鞋邊睡 | `warm`／`tender` | S08 |
| 留下 | `tender` | S09 |
| 送走 | `melancholy` | 結局 C |
| 背對睡 | `tender` | 結局 A |
| 薄冰門邊 | `calm` | 結局 D |

---

## 3. Ch1 十段 BGM 班表（S01～S10）

每段：**開場 →（信任拍可換）→ 鉤子／收束**。Crossfade 約 1.5～2.5s。

### S01｜螢幕光比月亮亮

弧線：`calm`（空白）→ 鉤子後仍 `calm`（勿早轉暖）

| 節點 | bg | Profile |
|------|-----|---------|
| 加班／超商 | office／convenience-night | `calm`（`blank_night`） |
| 回家客廳 | living-night | `calm` |
| 收束「直到明天」 | living-night | `calm` |

### S02｜後門那一瞥

弧線：`melancholy` → `tender`／`warm`（想留下）

| 節點 | bg | Profile |
|------|-----|---------|
| 店員提醒／轉進後門 | convenience → **backdoor-night** | `melancholy` |
| 對視、蹲等、半步 | backdoor-night | `tender`（選 A）或維持 `melancholy`（B／C） |
| 抱走上樓 | entrance／living | `warm`／`tender` |

### S03｜大門的臨時國界

弧線：`calm` →（我還在）`tender` → 清晨鉤子 `warm` 輕

| 節點 | bg | Profile |
|------|-----|---------|
| 鋪外套、進屋 | gate-night | `calm`（`gate_border`） |
| 開門輕聲／補水 | gate-night | `tender` |
| 腳趕／吼 | gate-night | `calm`（`tense`）短 |
| 房門外睡 | entrance／living | `warm` 輕 |

### S04｜共享同一種安靜

弧線：`warm`（`shared_quiet`）

| 節點 | bg | Profile |
|------|-----|---------|
| 沙發／地板平行 | living-day | `warm` |
| 硬抱／關浴室 | living／bathroom 感 | `calm`（`tense`）短 → 仍回 living |
| 廚房門口記憶點 | kitchen／living | `tender` 短 |
| 場次 A 存檔收束 | living | `warm` |

### S05｜你的聲音有兩種

弧線：`calm`（尖）→ `tender`（低）

| 節點 | Profile |
|------|---------|
| 戴耳機開會 | `calm` |
| 耳機回授／主管點名 | 維持 `calm`；回授為文字記憶點，不新增尖銳 SFX |
| 用力甩開／會議語氣吼 | `calm`（`tense`） |
| 脫耳機、嗅線／拔插頭「喀」 | `tender`；「喀」維持字幕，不另播 one-shot |

### S06｜走廊上的第三者

弧線：`calm` → `tender`（擋下）

| 節點 | bg | Profile |
|------|-----|---------|
| 被搭話／伸手摸 | corridor-day | `calm` |
| 推車輪卡縫「喀、喀」 | corridor-day | 維持 `calm`；文字記憶點，不新增環境 SFX |
| 擋在中間、婉拒 | corridor-day | `tender` |
| 塞回屋／給摸 | corridor-day | `calm`（`tense`） |
| 額頭頂腿 | corridor-day | `tender` |

### S07｜她倒下的那天

弧線：`calm` → `tender`（我還在）

| 節點 | Profile |
|------|---------|
| 發燒／狗守門 | `calm`（`sick_guard`） |
| 耳鳴／狗叫穿進來 | 維持 `sick_guard`；耳鳴只寫體感，不加高頻音效 |
| 「吵死了」關客廳 | `calm`（`tense`） |
| 「我還在」 | `tender` |

### S08｜走到轉角就好

弧線：`warm`／`calm` → `tender`（鞋邊睡）

| 節點 | bg | Profile |
|------|-----|---------|
| 巷口出發 | alley-day | `warm`；低信任貼牆用 `calm` |
| 硬拖達標 | alley-day | `calm`（`tense`） |
| 停等、提早回家 | alley → living | `tender`／`warm` |
| 靠鞋睡 | living | `tender` |
| 場次 B 存檔收束 | living | `warm`／`tender` |

### S09｜差點交給別人

弧線：`calm` → 分歧

| 節點 | bg | Profile |
|------|-----|---------|
| 咖啡廳前、理智清單 | cafe-day | `calm`（`almost_gave`） |
| 狗拒絕陌生人 | cafe-day | `tender` 緊張感（勿恐怖） |
| **留下** | → living | `tender` |
| **送走（結局 C）** | cafe-day → living 空 | `melancholy` |

### S10｜把鑰匙分給心跳

弧線：依結局鎖定（原則本段不再扣 trust）

| 結局 | Profile | 畫面對齊 |
|------|---------|----------|
| A 背靠 | `tender`（`ending_back`） | 背對睡；鑰匙＋牽繩 |
| B 選定 | `warm`／`tender` | 睡近仍確認 |
| C 已在 S09 | 維持 `melancholy`；空屋 `calm` | 冰箱嗡嗡（無狗 SFX） |
| D 薄冰 | `calm`（`ending_thin_ice`） | 門邊睡、不看「晚上見」 |

---

## 4. 幼犬 SFX（稀疏 one-shot）

路徑：`assets/audio/sfx/`。**有狗在場的關鍵 beat 才播一次**；S01 無狗不播。Version3 已落地 `whimper`／`murmur`／`soft`／`bark`／`growl` 五類。

| 情緒／beat | cue 池 | Section 例 |
|------------|--------|------------|
| 後門害怕／對視 | soft／whimper／murmur（依選項擇一） | S02 |
| 警戒半步／貼牆 | soft／sigh | S02／S08 低 |
| 吃飯抬眼 | soft | S02 |
| 樓梯間不安 | murmur | S03（已落地） |
| 平行安靜（極稀） | sigh | S04 可省略 |
| 被尖聲嚇到 | whimper 短 | S05 尖聲分支（已落地） |
| 嗅耳機線 | soft | S05 鉤子 |
| 躲腿後／頂額 | soft | S06 額頭輕碰（已落地） |
| 守門輕吠 | bark（一次） | S07（已落地） |
| 巷口僵住 | whimper | S08 機車驚嚇（已落地） |
| 拒絕陌生人 | growl／低鳴（一次） | S09 高信任分支（已落地） |
| 背對入睡 | sigh（極輕）或靜音 | S10 A |
| 送走後空屋 | **不播**幼犬聲 | 結局 C |

**禁止：** weather 雨聲疊層、連續 ambient dog loop、合成 whimper、信任「升級叮」。

---

## 5. 引擎落地約定

```text
play_bgm(profile)   # melancholy／warm／calm／tender（含別名）
dog_sfx(cue)        # whimper／murmur／soft／sigh／yip／bark／growl
stop_bgm()
```

- 同 profile 重進場景不重播；換曲 crossfade 1.5～2.5s  
- 主選單可靜音  
- 資產可先從 V2 四曲複製至 `Ch1_Trust_Version3/assets/audio/`，並更新 CREDITS

---

## 6. 撰寫／審查清單

- [ ] 新場景有標 `music`（或可從 bg＋情緒推得）
- [ ] S02 後門用 `melancholy`，帶走後有 crossfade 離開
- [ ] 每段換曲 ≤2 次；勿每個選項換
- [ ] 軟分軌未為高／低信任各開一條 BGM 線
- [ ] 衝突用 `calm`／`tense`，不用 jump scare
- [ ] 結局 C／D 無失敗懲罰音；C 空屋不播狗聲
- [ ] 新 OGG 必須更新 `CREDITS.md`
- [ ] 無信任 HUD 音效

---

## 7. 新增曲目流程

1. 下載／匯出 **OGG**（建議 48kHz、可 seamless loop）。
2. 存成 `assets/audio/{profile}.ogg`。
3. 在本檔 §1 登記 Profile，並更新 `CREDITS.md`。
4. 更新本檔十段班表或 bg 預設表。
5. 引擎定義後於場景播放。

---

## 8. 與 Version2 切割

| | Version3 | Version2 |
|--|----------|----------|
| 班表 | **S01～S10** | Day1～7 雨箱週 |
| 開場曲 | S01 `calm`；S02 `melancholy`（後門） | Day1 雨巷 `melancholy` |
| 主場景 | backdoor／stairwell／corridor／cafe | street／petshop／clinic |
| 結局 | A～D 四套收束 Profile | Day7 收養兩調 |

---

*更新：2026-07-17｜對齊 game_guild.md＋image_bg.md（十段 BGM、四結局、軟分軌）*
