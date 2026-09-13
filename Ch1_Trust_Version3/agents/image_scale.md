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
2. 截同 zoom 畫面，比**耳根到下巴**或**兩耳之間頭寬**（整場只用一種）。
3. 只改該 pose 的 `DOG_POSE_SCALE`。遠近仍只改 `xalign`。
4. 同 PNG、不同裁切 → 另開標籤，勿改他場數字（S07 `s07_low` 0.43 vs S04 `s04_low` 0.369）。
5. **禁止**把站姿 visH 硬拉齊趴姿 visH（頭會縮小，或整隻變巨犬）。

| 場 | 頭距母尺 | 備註 |
|----|----------|------|
| S02 後門 | `s04-anxious` **0.551** | 新 pose 用頭對齊此張 |
| S06 走廊 | `s06-retreat` **0.557** | 已頭距 |
| S07 臥室 | `guard_door` **0.438** | `s07_low` 0.43；指尖 `nose_tip` 0.65＠`bedroom_nose` 0.30；禁 `s05_ear_flat` 回房 |
| S08 巷口 | `leash_wait`／`s08_tense` | 已頭距；visH 見 §S08 確認；硬拖維持 behind |
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
| **S08 巷口狗** | `s08_tense`／`leash_wait`／`harness_bite` | **0.572／0.556／0.572** | 頭距；站 visH 可低於坐。遠近只改 xalign。禁 `street_tense` 0.808。人／狗 visH 見 §S08 確認 |

**同場遠近禁止換 zoom**，只用 `xalign`。

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
| S08 `char_right_walk` **0.32** | walk **0.124** | SCALE alley；人／狗尺確認見下節 |

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
| 日常 `char_right_entrance` **0.33** | **0.128**；S06 頂額 `entrance_nudge` **0.28** | S08／S09 同尺。S08 狗 xalign：far **0.60**／mid **0.66**／near **0.70**。人蹲 `leash`，見 §S08 確認。S06 護衛後 `forehead_nudge`＠`dog_entrance_nudge_cu`（hide 予安） |
| S02 抱走 `char_entrance_carry` **0.33** | 合成 | 大門／鞋櫃 |

### 走廊／護衛 `corridor`

| 人現行 | 狗現行 | 備註 |
|--------|--------|------|
| S06 `char_s06_neighbor` **0.22**／`char_s06_yuan` **0.60**（zoom **0.36**） | pair far／mid／near **0.42／0.50／0.54**；behind **0.66**；nudge **0.139** | 予安梯廳**外出襯衫＋樂福鞋**。同客廳幼犬比；遠近只改 xalign。狗頭距見 `image_dog.md` §3.8；人抱狗尺見 `CHAR_POSE_SCALE` |

### 巷口散步 `alley`

| 人現行 | 狗現行 | 備註 |
|--------|--------|------|
| **0.32** | **0.124** | behind **0.88**／far **0.56**／mid **0.63**／near **0.68** 同尺。硬拖維持 behind，勿 far 走到人前。人／狗 visH 見下節 |

### S08 人／狗尺（2026-09-13 確認｜頭距，不重產）

720p 實測 content visH（`DOG_REF_H`／`CHAR_REF_H` × pose × 場景尺）。**不改** `scale.rpy` 的 0.33／0.32／0.128／0.124。

| 場 | 人 | 狗場景尺 | 人 visH | 狗 visH（代表 pose） | 幼犬／人 |
|----|----|----------|---------|----------------------|----------|
| 玄關 | `leash` 蹲＠`char_right_s08` **0.33** | **0.128**；腳 `ypos 0.87`（人 0.80） | **368** | 躺 `s04_low` **58**／站 `halfstep` **111**／坐 `leash_wait` **74** | 站 ≈ **0.30**（幼犬比 0.28～0.37） |
| 巷口 | `walk`＠`char_right_walk` **0.32** | **0.124**；人狗腳同 `ypos 0.80` | 走 **386** | `s08_tense` **64**／`leash_wait` **72** | 站／坐頭距已對 |
| 巷口樹下 | 切回 `leash`，**仍 alley 0.32** | 同上 | 蹲 **357** | 跟上 `leash_wait` **72** | 蹲／走頭 **136～147**，`CHAR_POSE_SCALE` **1.0** |
| 辦公室週一 | `headphones` **0.28** | 無狗 | **331** | — | — |

**狗 pose（頭距母尺＝`leash_wait` 0.556／`s08_tense` 0.572）：**

| 標籤 | scale | visH＠該場 | 鎖定 |
|------|-------|------------|------|
| `s04_low` | **0.369** | 玄關躺 **58** | 與 `shoe_sleep` 0.414 同為橫躺 visH≈55～58。**禁**改客廳 `s04_low`；**禁**拿 S07 `s07_low` 0.43 進玄關 |
| `halfstep` | **0.580** | 玄關站 **111** | 躺→站 visH 約一半是姿勢，不是縮放跳號 |
| `harness_bite`／`leash_wait`／`drink_bowl` | **0.572／0.556／0.564** | 74／74／64 | 扣帶後族；喝水低頭 visH 略矮 |
| `s08_tense` | **0.572** | 巷口站 **64** | 可低於坐姿 `leash_wait` 72（頭距優先）。**禁**把站 visH 拉齊坐姿、禁 `street_tense` 0.808 |
| `shoe_sleep` | **0.414** | 躺 **55** | 先 hide yuan |

**人：** `leash`／`walk` 皆 `CHAR_POSE_SCALE` **1.0**。樹下蹲 visH 只少約 8%，頭幾乎同大——保持可讀，**不要**為「蹲比較矮」再縮人。

**禁止：** 用 zoom 假裝遠近；為玄關去改客廳 `s04_low`；巷口用無背帶 pose。

### 咖啡廳 `cafe`

| 人現行 | 狗現行 | 備註 |
|--------|--------|------|
| **0.36** | **0.139** | guard／home／mid 同尺 |

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

*更新：2026-09-13｜特寫鏡頭可重用（§0.2）＋回憶 sniff_wire／forehead_nudge／nose_touch；狗 pose 主尺＝頭距*
