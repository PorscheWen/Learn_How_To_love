# Version3｜人物／狗比例基準

> **場景 zoom 只改一處：** `Ch1_Trust_Version3/Renpy_game/game/scale.rpy`  
> **狗 pose 主尺＝頭距**（`script.rpy` 的 `DOG_POSE_SCALE`）；人仍用可見高（`CHAR_POSE_SCALE`）。  
> S02 → `SCALE_S02`（`s02_char()`／`s02_dog()`）；S04–S10 → `SCALE`（`sc_char()`／`sc_dog()`）。  
> 不要在 transform 寫死 zoom。換 PNG 填滿畫布**不會**讓螢幕上的立繪變大。

---

## 0. 怎麼算（鎖死）

| 符號 | 值 | 畫面高度 |
|------|----|----------|
| `CHAR_REF_H` | 1280 | 人畫布 ≈ **1280 × CHAR_POSE_SCALE × char_zoom** |
| `DOG_REF_H` | 1536 | 狗畫布 ≈ **1536 × DOG_POSE_SCALE × dog_zoom** |
| 腳底 | `yanchor 1.0`／`ypos 0.80` | 字幕框上緣；頭頂須留在 720p 內 |

`CHAR_POSE_SCALE` 讓同場人物**可見身高**接近。  
`DOG_POSE_SCALE` **不用全身可見高**：同場換 pose 時對齊**頭**（見 §0.1）。數字在 `script.rpy`。

### 0.1 狗頭距（未來一律用這個）

同場、同一 `dog_zoom` 下，玩家認的是臉。**新 pose、新場、重校：用頭當參考，不要對齊 PNG 外框、content bbox、胸寬、或 visH px。**

1. 先鎖該場**母尺 pose**（在場最久、或該場標準站／趴）。
2. 截同 zoom 畫面，比**耳根到下巴**或**兩耳之間頭寬**（整場只用一種）。Loop C 在兩眼都抓到時用**兩眼距**當頭距；畫布不同但臉畫一樣大、螢幕頭卻跳 → 只改該 pose 的 `DOG_POSE_SCALE`。
3. 只改該 pose 的 `DOG_POSE_SCALE`。遠近仍只改 `xalign`。
4. 同 PNG、不同裁切 → 另開標籤，勿改他場數字（S07 `s07_low` 0.43 vs S04 `s04_low` 0.369）。
5. **禁止**把站姿 visH 硬拉齊趴姿 visH（頭會縮小，或整隻變巨犬）。

| 場 | 頭距母尺 | 備註 |
|----|----------|------|
| S02 後門 | `s04-anxious` **0.551** | 新 pose 用頭對齊此張 |
| S06 走廊 | `s06-retreat` **0.557** | 已頭距 |
| S07 臥室 | `guard_door` **0.438** | `s07_low` 0.43；指尖 `nose_tip` 0.65＠`bedroom_nose` 0.30；禁 `s05_ear_flat` 回房 |
| S08 巷口 | `leash_wait`／`s08_tense` | `leash_wait` **0.677**／`s08_tense` **0.903**；場景尺改透視（§S08 巷口透視）：狗 zoom＝人 zoom×0.3346，隨腳底 y 變 |
| S09／S10 等 | 該場先鎖母尺 pose | **新 pose／重校一律頭距** |
| S04／S05 客廳 | 未重校前暫沿舊 visH 表 | **新建議禁止再開 63／76px 標靶** |

**不套同場頭距：** 抱狗合成、深度例外（廚房門檻 0.19、梯廳門墊 0.187）。**特寫仍比頭**：先對齊該場母尺，再另開較近 zoom。換場可換母尺，場內必須一致。

### 0.2 特寫鏡頭（可重用｜樣板 S07 `nose_tip`）

任何段只要這一拍值得靠近看（鼻、指、額、鞋邊……），都可以切特寫。**規格鎖死：**

1. **只顯示該場背景＋特寫層。** `hide` 予安／鄰居／第二隻狗／多餘道具，避免雙重手、雙重狗。
2. **放大。** 另開 `SCALE` 鍵，zoom ≈ 該場地板幼犬尺 ×**2.1～2.2**（S07：地板 0.139 → `bedroom_nose` **0.30**）。遠近仍不拿 zoom 假裝。
3. **頭距。** 特寫 pose 的頭對齊該場母尺後再靠近；禁止 visH 把全身縮成迷你狗。
4. **加入回憶。** 特寫拍結束時 `$ unlock_secret_photo("…")`；靜幀進 `gallery/secret-*.png`（油畫紀念照，構圖對齊特寫：頭／鼻／指）。標題婉轉，禁止親密％。

落地骨架（S07）：`hide yuan` → `show dog nose_tip at dog_bedroom_nose_cu` → `unlock_secret_photo("nose_touch")` → 切回地板 pose。回憶圖：`gallery/secret-nose-touch.png`。

新場複製：`scale.rpy` 加 `{place}_cu`；`script.rpy` 加 `dog_*_cu` transform（`sc_dog("{place}_cu")`）；`hidden_content.rpy` 登記 SECRET_PHOTO。

| 場 | pose | SCALE | transform | 回憶 |
|----|------|-------|-----------|------|
| S05 會後 | `sniff_wire` | `living_wire` **0.30** | `dog_living_wire_cu` | `sniff_wire`／`gallery/secret-sniff-wire.png`。開會中 sniff＠`dog_near` **不**特寫 |
| S06 護衛後 | `forehead_nudge` | `entrance_nudge` **0.28** | `dog_entrance_nudge_cu` | 既有 `forehead_nudge`。只看護衛；禁客廳 `dog_nudge`、禁地板 mid |
| S07 清晨 | `nose_tip` | `bedroom_nose` **0.30** | `dog_bedroom_nose_cu` | `nose_touch`／`gallery/secret-nose-touch.png` |

| 場 | pose | scale | 備註 |
|----|------|-------|------|
| S02 後門 | `s04-anxious` | **0.551** | 第一次見面；橫式填滿 |
| S02 後門 | halfstep／sniff-bento／ear-flat | 0.580／0.647／0.653 | 與 s04-anxious 同場對齊 |
| 後段備援 | 舊 `dog-anxious` | **1.575** | 留白尺；**禁**客廳 |
| **S04 客廳趴姿** | parallel（母尺） | **0.524** | 舊 visH，重校改頭距。ear-perk 0.414／chin-hover 0.558／head-turn **0.369**／chin-floor 0.424；`s04_low` **0.369**（勿用後門 0.551） |
| S04 尾隨 | `wag` 幀 | **0.750** | 對齊 parallel 可見高；勿用 halfstep |
| S04 合照／低信任站 | street-tense | **0.808** | 客廳約 76px（與 S05 站姿族同檔） |
| S04 門檻 | kitchen-door | 0.577 | `dog_kitchen_threshold` 深度例外 |
| **S05 早會** | chair-paw／stuck／ear_flat／stair_watch | **0.401／0.472／0.409／0.615** | 站姿約 76px（趴 63px 的 1.2 倍）；head-up 0.332／s05_anxious 0.369；sniff-wire 幀 0.605、靜態 0.401。會後特寫 zoom `living_wire` **0.30**。S06 開場 `s05_stair_watch` 另用 **0.82**（走廊頭距） |
| **S06 走廊人** | `carry_pup` | **1.056** | 對齊鄰居 idle 可見高（約 435px＠0.36）；`door_hold`／`block` 重產後約 1.0。彎腰 `neighbor lower` 可略矮 |
| **S07 臥室狗** | `s07_low`／`guard_door`／`nose_tip` | **0.43／0.438／0.65** | 頭距母尺 guard_door；指尖特寫 zoom **0.30**（`bedroom_nose`）。禁 `s05_ear_flat` 回房 |
| **S08 巷口狗** | `s08_tense`／`s08_explore`／`s08_startle`／`s08_resist`／`leash_wait`／`s08_threshold`／`s08_sniff_harness` | **0.903／0.903／0.903／0.903／0.677／0.449／0.457** | `leash_wait` 頭距對齊玄關開場 `s08_halfstep`。門檻／聞帶 864×958 裁底留白後重算倍率。遠近只改 xalign。禁 `street_tense` 0.808。聞帶禁巷口。人／狗 visH 見 §S08 確認 |

**同場遠近禁止換 zoom**，只用 `xalign`。**唯一例外：S08 巷口**（路面縱深明確，腳底 y 與 zoom 依地平線一起變，見 §S08 巷口透視）。

**S02：** 每場對齊門框／椅／櫃／路；後門幼犬可見高 ≈ 人 ×**0.28**（`SCALE_S02["backdoor"]["dog"] = 0.12`）。數字以 `SCALE_S02` 為準。

**S04–S10：** 人對齊 `image_bg.md` 對景（客廳 0.36、玄關 0.33、巷口 0.32、咖啡廳 0.36、廚房 POV 0.52）。同平面狗沿用後門幼犬比 `char × 0.12/0.31`（≈0.387），**不要**用舊公式 ×1.048（會跟人差不多高）。廚房門檻 0.19、梯廳門墊 0.187 為深度例外。機車道具維持 ×0.8，不要再乘。

---

## 1. S02 對景表（＝ `scale.rpy` 的 `SCALE_S02`）

改大小：打開 `Renpy_game/game/scale.rpy`，改對應 `char`／`dog`。抱狗合成圖跟人同尺、**不另疊狗**（`dog: None`）。

| 場 | 對齊什麼（`fit`） | 人 | 狗 | transform |
|----|-------------------|----|----|-----------|
| `office` | 椅背／桌面到腰；S02 開場站右側走道 | **0.28** | — | `char_office`（xalign 0.66） |
| `convenience` | 櫃面／高腳椅到腰 | **0.29** | — | `char_convenience*` |
| `street` | 左側木門框（頭頂低於門楣） | **0.23** | 合成 | `char_street`／`char_street_carry` 同尺 |
| `backdoor` | 卸貨門；幼犬≈人×0.28，四姿同高 | **0.31** | **0.12** | `char_backdoor_*`／`dog_backdoor_*` |
| `clinic` | 窗內木櫃檯（抱走） | **0.27** | 合成 | `char_clinic`（xalign 0.56／ypos 0.64） |
| `entrance` | 大門／鞋櫃到腰（抱走） | **0.33** | 合成 | `char_entrance_carry` |
| `living` | 落地窗（抱走） | **0.32** | 合成 | `char_living` |
| `gate` | 鐵門／木門框 | **0.28** | 合成 | `char_gate` |

- 同場鎖死：人一把、狗一把。走近只改位置，不改大小。
- 換場可以變（巷口遠、後門近），**不要**把後門尺抄到街上。
- 後門狗遠／中／近一律 `zoom 1.0` + `xzoom`／`yzoom`。四姿可見高靠 `DOG_POSE_SCALE` 對齊，不要再拆兩把 zoom。

### 之後配尺（新場若加獨立狗層）

```text
# 同平面幼犬（S02 後門現行；S04–S10 亦用此式）
dog_zoom = round(char_zoom * 0.12 / 0.31, 3)   # ≈ char × 0.387；可見高 ≈ 人×0.28～0.37

# 深度例外（門檻／門墊中遠景）勿套上式
# kitchen dog = 0.19；stairwell dog = 0.187
```

步驟：① 先把人對齊該場門框／櫃面／椅；② 同平面的狗用上式寫入 `SCALE_S02` 或 `SCALE`；③ 遠近只改 `xalign`。

### 例外

| 情況 | 作法 |
|------|------|
| 只抱狗、不另疊狗 | `dog: None`，只調該場 `char` |
| 狗在**中遠景**（廚房門檻、梯廳門墊） | 寫入 `SCALE` 固定值（0.19／0.187），勿套幼犬比 |
| 場上沒有狗 | 仍記入 `char` |

---

## 2. 每場基準表

**S02**＝`SCALE_S02`（見 §1）。**S04–S10**＝`SCALE`（人對景；狗幼犬比）。  
同場 far／mid／near **同一把狗尺**，只改 `xalign`。

### 後門 `backdoor`（S01 窺看／S02 相遇）｜對景

| 人 | 現行 | 狗 | 現行 | 備註 |
|----|------|----|------|------|
| `char_backdoor_*` | **0.31** | `dog_backdoor_*`（含 first） | **0.12** | 四姿 bbox 對齊（`s04-anxious`／halfstep／sniff-bento／ear-flat）；幼犬≈人×0.28 |

### 客廳 `living`（全景對景；S02 抱走對落地窗）

| 用途 | 人現行 | 狗現行 | 備註 |
|------|--------|--------|------|
| 全景站 | `char_right`／`left` **0.36**；`char_center` **0.384** | far／mid／near **0.139** | 幼犬比 |
| S02 抱狗進門 | `char_living` **0.32** | 合成 | 落地窗；勿套全景 0.36 |
| 坐椅 | `char_chair`／`sofa`／**`char_chair_left`（S05）** **0.304** | **0.139**；會後嗅線 `living_wire` **0.30** | 狗同客廳平面；S05 狗面左、人面右。會後 `sniff_wire`＠`dog_living_wire_cu`（hide 予安）；開會中 sniff 仍 `dog_near` |
| S09 告別 | `char_right_farewell` **0.36** | **0.139** | 翻轉用 xzoom |
| 關客廳（S07 選 B） | `char_right` **0.36** | **0.139**；`dog_sick_far` **0.32** | 沙發左；`s05_ear_flat` 0.409；**禁**舊 anxious 1.575 |

### 臥室 `bedroom`（S07 病床／門線）

| 用途 | 人現行 | 狗現行 | 備註 |
|------|--------|--------|------|
| 病床 | `char_bedroom` **0.18** | far／mid／near／shift／near_to_yuan **0.139**（同客廳地板）；指尖 `bedroom_nose` **0.30** | 沿床躺、頭右枕、面向左看狗（`xalign 0.78`／`ypos 0.76`）。狗遠近只改 xalign：far **0.20**／mid **0.30**／near **0.46**／shift **0.34**／near_to_yuan **0.52**。頭距母尺 `guard_door` **0.438**；低信任／選 B 回房 `s07_low` **0.43**＠far。指尖 `nose_tip` **0.65**＠`dog_bedroom_nose_cu`（頭對齊守門再靠近；禁地板 visH 0.384）。pose 跟旁白走，見 `section_07_sick_guard.md`。**禁**臥室 `s05_ear_flat`、禁舊 anxious 1.575 |

### 廚房 `kitchen`（POV；深度例外）

| 人現行 | 狗現行 | 建議 |
|--------|--------|------|
| `char_kitchen_near`／`sink` **0.52** | `dog_kitchen_threshold` **0.19** | 維持門檻小於人 |

### 超商 `convenience`（對景｜無狗）

| 人現行 | 若加狗 |
|--------|--------|
| **0.29** | 0.112 |

### 巷口／街 `street`

| 人現行 | 狗現行 | 備註 |
|--------|--------|------|
| `char_street`／`char_street_carry` **0.23** | 合成 | 左側門框；遇狗前與抱走同尺 |
| S08 巷口透視 `s08_yuan`（char zoom **0.001989×(腳y−430)**，0.294＠578→0.235＠548） | 狗＝人×**0.3346** | 2026-09-28 取代 `char_right_walk` 0.32／狗 0.124；見 §S08 巷口透視 |

### 辦公室 `office`（對景｜無狗）

| 人現行 | 若加狗 |
|--------|--------|
| **0.28** | 0.108 |

### 急診 `clinic`（S02 抱走）

| 人現行 | 狗 |
|--------|----|
| `char_clinic` **0.27** | 合成（窗內櫃檯；勿站右側玻璃門） |

### 公寓大門 `gate`（S02 抱走／S03 開場）

| 人現行 | 狗 |
|--------|----|
| `char_gate` **0.28** | 合成（鐵門／木門） |

### 梯廳 `stairwell`（深度例外）

| 狗現行 | 建議 |
|--------|------|
| `dog_far_stair` **0.187** | 維持門墊中遠景 |

### 玄關 `entrance`

| 人現行 | 狗現行 | 備註 |
|--------|--------|------|
| 日常 `char_right_entrance` **0.33** | **0.128**；S06 頂額 `entrance_nudge` **0.28** | S08 狗 xalign：far **0.54**／to_yuan **0.58**／mid **0.62**／near **0.66**（鞋櫃與予安之間、靠近牽繩）。S09 仍 far **0.60**／mid **0.66**／near **0.70**。人蹲 `leash`，見 §S08 確認。S06 護衛後 `forehead_nudge`＠`dog_entrance_nudge_cu`（hide 予安） |
| S02 抱走 `char_entrance_carry` **0.33** | 合成 | 大門／鞋櫃 |

### 走廊／護衛 `corridor`

| 人現行 | 狗現行 | 備註 |
|--------|--------|------|
| S06 `char_s06_neighbor` **0.22**／`char_s06_yuan` **0.60**（zoom **0.36**） | pair far／mid／near **0.42／0.50／0.54**；behind **0.66**；nudge **0.139** | 予安梯廳**外出襯衫＋樂福鞋**。同客廳幼犬比；遠近只改 xalign。狗頭距見 `image_dog.md` §3.8；人抱狗尺見 `CHAR_POSE_SCALE` |

### 巷口散步 `alley`

| 人現行 | 狗現行 | 備註 |
|--------|--------|------|
| 透視 **0.001989×(腳y−430)** | 人×**0.3346** | 2026-09-28 起改站位點 `S08_ALLEY_PT`＋ease 走位（舊 behind 0.88／far 0.56／mid 0.63／near 0.68、同尺 0.32／0.124 已廢）。硬拖仍維持狗在身後。見 §S08 巷口透視 |

### S08 人／狗尺（2026-09-13 確認｜頭距，不重產）

720p 實測 content visH（`DOG_REF_H`／`CHAR_REF_H` × pose × 場景尺）。**不改** `scale.rpy` 的 0.33／0.32／0.128／0.124。

| 場 | 人 | 狗場景尺 | 人 visH | 狗 visH（代表 pose） | 幼犬／人 |
|----|----|----------|---------|----------------------|----------|
| 玄關 | `leash` 蹲＠`char_right_s08` **0.33**×pose **0.70** | **0.128**；腳 `ypos 0.87`（人 0.80） | **258** | 躺 `s04_low` **58**／站 `s08_halfstep` **102**／坐 `leash_wait` **90** | `leash_wait` 頭對齊 halfstep；蹲人／門 ≈ **0.60** |
| 巷口（**已由 §S08 巷口透視取代**） | ~~`walk`／`leash_yank`＠`char_right_walk` 0.32~~ | ~~0.124~~ | 舊 走 386 | 舊 87 | 2026-09-28 改透視：人 353→284px、狗 69→56px、`leash_yank` pose **0.95** |
| 巷口蹲下 | `leash_street`（同 leash PNG，foot 裁切）＠`yuan_yanked`，pose **0.70** | 透視 | 蹲 **200**＠557 | `leash_wait` 58–60 | 蹲≈站姿 ×0.65（約 1.05 m） |
| 辦公室週一 | `headphones` **0.28** | 無狗 | **331** | — | — |

**狗 pose（頭距母尺＝開場 `s08_halfstep`；`leash_wait` **0.677** 對齊此張／`s08_tense` 0.903）：**

| 標籤 | scale | visH＠該場 | 鎖定 |
|------|-------|------------|------|
| `s04_low` | **0.369** | 玄關躺 **58** | 橫躺 visH≈58。**禁**改客廳 `s04_low`；**禁**拿 S07 `s07_low` 0.43 進玄關 |
| `s08_halfstep` | **0.529** | 玄關站 **102** | 同 PNG `halfstep`；S08 開場頭距母尺。**禁**改全域 0.580 |
| `halfstep` | **0.580** | （S02／S07／S10） | S08 不用此尺 |
| `harness_bite`／`leash_wait`／`drink_bowl` | **0.658／0.677／0.84** | 78／90／98 | `leash_wait` 頭對齊 halfstep。喝水是側身全身，舊 0.564 的 visH 66 比同場站姿小一截；2026-09-28 改 **0.84**（動畫幀玄關約 98，頭低下，不高過 halfstep 102）。碗底 `foot=1238` |
| `s08_tense`／`s08_explore`／`s08_startle`／`s08_resist` | **0.903** | 巷口站 **87** | 864 畫布；牽繩族 +15%。`s08_explore` 探路；`s08_startle` 驚嚇、`s08_resist` 抗拒走。**禁** `street_tense` 0.808 |
| `s08_threshold` | **0.449** | 玄關站半跨 | 864×958（裁底緣透明）；倍率 0.54×958/1152 |
| `s08_sniff_harness` | **0.457** | 低頭聞帶 | 864×958（裁底緣透明）；倍率 0.55×958/1152；**禁**巷口 |
| `shoe_sleep` | **0.414** | 躺 **55** | 對齊 `s04_low` 橫躺 visH；先 hide yuan |

**人：** `walk` 站姿 `CHAR_POSE_SCALE` **1.0**。`leash_yank` 864 畫布站姿 **0.95**（2026-09-28：舊 0.75 只對齊畫布高，內容高比 walk 滿，實測矮 22%；改用內容高對齊）。蹲姿 `leash`／`squat_side` **0.70**（864 畫布幾乎填滿，1.0 會讓 visH 接近大門）。巷口蹲用 `leash_street`（同 PNG、foot=1063）。

### S08 巷口透視（2026-09-28｜`alley_day` 依背景道路重排）

> 本場是「同場遠近只改 xalign」的**唯一例外**：巷口有明確的路面縱深，人／狗／機車沿路往樹影、轉角移動時，**腳底 y 與 zoom 一起變**。數字唯一來源：`scale.rpy` 的 `S08_ALLEY`／`S08_ALLEY_PT`；transform：`s08_yuan`／`s08_yuan_move`／`s08_dog`／`s08_dog_move`／`scooter_parked`／`scooter_pass`。

**量測（720p，PIL 對 `bg-alley-day.png` 縮 1280×720）：**

| 項目 | 值 | 用途 |
|------|----|------|
| 左側近木門 | 高 **198px**、門底 y **496** | 真實約 2.05 m → 門平面約 97 px/m |
| 遠木門（右後小屋） | 高 **104px**、門底 y **463** | 兩門等高反推地平線 |
| 地平線 | y ≈ **430** | 198/(496−h)=104/(463−h) → h≈426；取 430（遠屋窗台、屋基線交會） |
| 鏡頭高 | ≈ **0.68 m** | (496−430)/97 |
| 路面 | 左人行道緣 y≈605−0.139x；右花台弧緣 x≈815–850（y 580–640） | 人狗腳底須在兩緣之間（舊版狗站進右側花台盆栽） |
| 樹幹根部 | 約 (975, 572)，在右側花台上 | 樹影落在路中偏右 x≈650–900 |
| 字幕區 | y 572 以下（say_window 高 148） | 腳底上限 578 |

**公式：**

```text
人 1.62 m 可見高 = 1.62/0.68 × (腳y − 430) = 2.382 × (腳y − 430) px
walk 可見高 = 1197.5 × char_zoom            → char_zoom = 0.001989 × (腳y − 430)
狗 dog_zoom = char_zoom × 0.3346            → 同深度坐姿 leash_wait ≈ 人 × 0.195（約 32 cm，2–3 月齡短腿幼犬）
停放機車（車高 1.15 m，內容 754px）          zoom = 0.002243 × (輪胎y − 430)
呼嘯機車（騎士＋車 1.4 m，內容 1001px）       zoom = 0.002057 × (輪胎y − 430)
```

zoom 與腳底 y 成線性，所以 `ease` 同時插值 `ypos` 與 `xzoom／yzoom` 就是正確透視（越往後越小、越高）。

**舊版實測問題（2026-09-28 before 截圖）：**

| 問題 | 舊值 | 新值 |
|------|------|------|
| 人比背景大 | walk 可見高 384px＠腳 560（透視應 310px，大 24%） | 353px＠578 → 284px＠548 |
| 狗相對人偏大 | 狗／人 0.22（tense 85px／leash_wait 86px） | 0.195（69px＠580 → 56px＠553） |
| 站位不在路上 | 予安 xalign 0.74 踩右側花台弧緣；狗 0.88 站進花台盆栽 | 全程在路面 |
| 腳底不同一條線 | walk 腳 560、狗 572、explore 556、resist 559、蹲 554（PNG 腳下透明列） | `foot=` 裁掉腳下透明列，腳底＝ypos |
| 被扯那拍人變矮 | `leash_yank` 298px vs walk 384px（-22%） | `CHAR_POSE_SCALE` 0.75→**0.95**（內容高對齊 walk，略前傾 -1.5%） |
| 行進方向與劇情相反 | 朝左走、樹影／轉角在身後；空機車停在左前，從未「經過」 | 朝右上（樹影／轉角）走；空車移到左側人行道緣中景，劇情「經過空機車」確實從它前面走過 |
| 沒有移動 | 換位置用 Dissolve 交叉淡化 | `*_move` ease 走位；換 pose 才 Dissolve 0.5 |

**站位（`S08_ALLEY_PT`，畫布中心 x／腳底 y）：**

| 點 | 位置 | 劇情 |
|----|------|------|
| `yuan_start` | (430, 578) | 剛出門、左前 |
| `yuan_halfstep` | (480, 573) | 「往前半步，停住，再等」 |
| `yuan_step` | (545, 569) | 低信任「再往前一點」 |
| `yuan_pass` | (640, 561) | 從空機車前經過（車頭左前；2026-09-28b） |
| `yuan_center` | (770, 555) | 離開牆邊、走到路中（樹影邊） |
| `yuan_yanked` | (540, 562) | 車經過時趕快往後拉一步；原地蹲下 |
| `yuan_drag1`／`yuan_drag2` | (800, 552)／(840, 548) | 選 B 硬拖往轉角（停在樹幹左側，避免與樹幹重疊） |
| `yuan_home1`／`yuan_home2` | (560, 567)／(420, 577) | 選 C 朝左折返 |
| `dog_behind_start` | (315, 580) | 她身後半步（約 0.5 m） |
| `dog_shuffle`／`dog_follow` | (365, 578)／(440, 575) | 貼牆挪半腳／跟兩步 |
| `dog_beside` | (505, 575) | 到她側邊、往前半個身位 |
| `dog_sniff_scooter` | (608, 534) | 高信任聞空機車車尾（2026-09-28b） |
| `dog_behind_pass` | (560, 566) | 經過空車時收回她腿後 |
| `dog_explore` | (880, 548) | 路中往樹影探路（她前方約 0.6–1.2 m） |
| `dog_heel` | (670, 554) | 被往後拉近，仍在她前面；抗拒原圖面左、繩朝她 |
| `dog_wait_mid`／`dog_wait_shade` | (830, 560)／(885, 553) | 選 A 自己走一公尺（從她身前經過）→ 樹影下甩身 |
| `dog_drag1`／`dog_drag2` | (725, 557)／(765, 553) | 選 B 被拖（維持身後） |
| `dog_home1`／`dog_home2` | (470, 572)／(320, 580) | 選 C 在前帶路 |
| `scooter_parked` | 輪胎線 (70, 640)，顯示 zoom × **0.8** | 畫面左下角，比公式再小兩成（2026-09-28k） |
| `scooter_pass` | (1010, 500)→(840, 610)→(600, 760)，zoom 鎖定、約 2.4 秒 | 右中再偏右，順著路面往前，大小不變（2026-09-28k） |

**2026-09-28b 機車重排（使用者：「無人的摩托車擺放位置合理些；騎車經過的位置應該在予安要牽狗過去的前面出現」）：**

- **空車位置理由：** 左側牆邊由左而右是盆栽排（x 0–450）→木門＋台階（465–560）→盆栽（555–600）→電線桿（603–632）→深色木屋牆面（640–780，**無門**）→盆栽（780–830）→小門（830–850）。舊點 (570, 545) 擋在木門台階正前方、像停在人家門口。新點 (700, 520) 停在電線桿右側、木屋牆前的路緣：台灣巷弄最常見的停車位（靠電桿、貼牆、不擋門）；車身 x≈606–800，電桿底被車身擋住（電桿在車後，遮擋關係正確），盆栽只在車後露出，不「停進」盆栽；木門與小門都不擋。輪胎 y 520 在左人行道緣（y≈605−0.139x＝508）與路面交界。
- **仍可「經過」與「聞」：** 予安 `yuan_pass` (640, 561) 從車頭左前走過（比車近鏡頭，車頭仍露出）；高信任狗 `dog_sniff_scooter` (608, 534) 鼻尖朝車尾。
- **呼嘯機車路線：** 巷道往右上縮向遠端（樹幹左側 x≈870–950、y≈470–505 露出路面）＝「轉角那頭」。車從那裡出現（她前方約 2.5 m，正是狗剛才探路的方向），斜切過她前方那段路，再貼左側、從她與空車之間（y 542：比狗 560／她 555 遠、比空車 520 近）往左前出畫。台灣靠右行駛，迎面來車走畫面左側，與巷道幾何一致；3/4 正面朝左前的 `scooter-pass` 正好符合此行進方向。`show … behind yuan, dog`，經過她身後時被人狗擋住，不蓋人。純側面「右→左等深橫切」在此背景不成立：右側 y≈530 是花台／樹根與右側屋前盆栽，左側 y≈535 已是人行道。
- **狗走位：** 中／高信任「到她側邊」、選 A「自己走一公尺」、選 C「在前帶路」改用走姿 `s08_explore`（原本坐姿 `leash_wait` 滑過去）；新走姿圖落地後再換。

**2026-09-28c 新圖尺：** `walk_behind`（`char-yuan-walk-leash-behind.png`）內容高 1436（頭頂列 39、腳底列 1475）＝`walk`，pose **1.0**、`foot=1476`，同一站位點換圖身高不跳。`s08_walk`（`dog-s08-walk.png`）1024×1536，pose **1.204**＝0.903×1536/1152（與 explore 畫布同像素尺），`foot=1501`；側面站姿內容高 705 px（explore 684）。`scooter-pass-side.png` 1280×1024、內容高 1000＝`scooter-pass`（可沿用 `prop_k["pass"]`），目前不用。
**`walk_behind` 牽繩末端：** 畫布約 (970, 1282)＝各「狗在身後」拍中 `s08_tense` 胸背帶扣環的平均相對位置（實算 x 931–1030、y 1267–1281）。

**朝向：** 原圖一律面左。行進朝右上 → walk／leash_yank／狗走姿 `face="r"`（翻面）；蹲 `leash_street` 與 `s08_startle` 用 `face="l"`（看狗／看機車離去；startle 牽繩往右上正好連到予安）；選 C 折返全部 `face="l"`。

**移動規則：** 第一次出場用 `s08_yuan(pt)`／`s08_dog(pt)`（靜態）；同 tag 已在場才用 `*_move(pt, t=…)`（ATL 承接前一個狀態）。同 pose 移位不加 transition；換 pose 加 `Dissolve(0.5)`。

**不受影響：** 玄關 `entrance_day` 各拍（量測：蹲姿 257px／門 425px、腳 553 vs 門底 503，透視比例合理，未改）；`s08_tense` 加 foot 裁切後在玄關返家拍（`dog_entrance_far_s08`）下移約 4px，可忽略。`SCALE["alley"]` 保留但目前無 transform 使用。

**禁止：** 用 zoom 假裝遠近（S08 巷口透視除外：那是依地平線算出的真遠近，不是假裝）；為玄關去改客廳 `s04_low`；巷口用無背帶 pose；蹲姿跟人／門同一高度。

### 咖啡廳 `cafe`

| 人現行 | 狗現行 | 備註 |
|--------|--------|------|
| **0.36** | **0.139** | guard／home／mid 同尺。`cafe_refuse` **1.523**／`cafe_tense` **1.026**（頭框對齊後牽繩族 +15%） |

---

## 3. Section 速查（誰在哪一場）

| Sec | 有人＋狗的場 | 只有人 |
|-----|----------------|--------|
| 01 | — | office／convenience／street／backdoor 窺看／entrance／living／kitchen |
| 02 | **backdoor**；抱狗＝street／clinic／entrance／living／gate 合成 | office／convenience／street |
| 03 | stairwell 狗窩；entrance 進門 | gate 抱狗合成 |
| 04 | living 椅（聲響趴姿同高）；kitchen 門檻（深度例外） | — |
| 05 | living | — |
| 06 | **stairwell** 人狗 pair；entrance 頂額／進門 | — |
| 07 | **bedroom** 病床／門線；living 關客廳；kitchen 倒水 | office |
| 08 | entrance；alley 散步；living | office 週一 |
| 09 | living 告別；entrance；cafe | office |
| 10 | living 睡姿；kitchen 門檻；entrance | alley／street 路徑 |

---

## 4. 改 zoom 時

1. **S02：** 只改 `scale.rpy` 的 `SCALE_S02`。**S04–S10：** 只改 `SCALE`。再核對本檔數字是否一致。  
2. 同場 `dog_far`／`mid`／`near` **同 zoom**，只改 `xalign`。同一標籤切遠近時，一律 `zoom 1.0` + `xzoom`／`yzoom`，**不要**有的用 `zoom`、有的用 `xzoom`（會疊乘變很小）。  
3. 不要為了舊客廳 185px 標靶重跑 `recalibrate_sprites.py`。  
4. **不要再對「其餘場」乘一次 0.8。**機車道具維持現尺。  
5. 落地改 transform 後同步本表「現行」欄。  
6. 禁止把 A 場的 zoom 抄到 B 場。後門／同場換 pose 仍大小不一：改 `DOG_POSE_SCALE` **對齊頭距**（§0.1），不要對 content bbox、不要拆兩把場景 zoom。同場人物身高不一：改 `CHAR_POSE_SCALE`，不要重畫「變大」。

---

*更新：2026-09-28c｜S08 新圖 `walk_behind`／`s08_walk` 接線；側面機車備用*  
*前次：2026-09-28b｜S08 空機車改停電線桿旁路緣；呼嘯機車改從巷道遠端出現、切過她前方*  
*前次：2026-09-28｜S08 巷口改背景透視（地平線 430、人 1.62 m、狗＝人×0.195）＋站位點 ease 走位；`leash_yank` 0.95；S08 牽繩族 foot 裁切*  
*前次：2026-09-20｜S08 玄關狗 far 0.54／mid 0.62（鞋櫃與予安之間）；`leash_wait` 0.677 頭距對齊開場 halfstep*
