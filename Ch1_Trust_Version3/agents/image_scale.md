# Version3｜人物／狗比例基準

> **數字只改一處：** `Ch1_Trust_Version3/Renpy_game/game/scale.rpy`  
> S02 → `SCALE_S02`（`s02_char()`／`s02_dog()`）；S04–S10 → `SCALE`（`sc_char()`／`sc_dog()`）。  
> 不要在 `script.rpy` 寫死 zoom。換 PNG 填滿畫布**不會**讓螢幕上的立繪變大。

---

## 0. 怎麼算（鎖死）

| 符號 | 值 | 畫面高度 |
|------|----|----------|
| `CHAR_REF_H` | 1280 | 人畫布 ≈ **1280 × char_zoom** |
| `DOG_REF_H` | 1536 | 狗畫布 ≈ **1536 × DOG_POSE_SCALE × dog_zoom** |
| 腳底 | `yanchor 1.0`／`ypos 0.80` | 字幕框上緣；頭頂須留在 720p 內 |

`DOG_POSE_SCALE` 用來讓各 pose 的**可見內容**同高。數字在 `script.rpy`。

| 場 | pose | scale | 備註 |
|----|------|-------|------|
| S02 後門 | `s04-anxious` | **0.551** | 第一次見面；橫式填滿 |
| S02 後門 | halfstep／sniff-bento／ear-flat | 0.580／0.647／0.653 | 與 s04-anxious 同場對齊 |
| 後段備援 | 舊 `dog-anxious` | **1.575** | 留白尺；**禁**客廳 |
| **S04 客廳趴姿** | parallel（母尺） | **0.524** | ear-perk 0.414／chin-hover 0.558／head-turn **0.369**／chin-floor 0.424／**head-up 0.332** |
| S04 尾隨 | `wag` 幀 | **0.750** | 對齊 parallel 可見高；勿用 halfstep |
| S04 門檻 | kitchen-door | 0.577 | `dog_kitchen_threshold` 深度例外 |
| **S05 早會** | 全姿對齊 parallel | **客廳 ≈63px** | 予安 `char_chair_left`；狗 `dog_near`／`mid`／`far` 面左。chair-paw 0.334／chair-stuck 0.394／sniff-wire 幀 0.605；`s05_anxious` 0.369／`s05_ear_flat` 0.341／`s05_stair_watch` 0.477 |

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
| 坐椅 | `char_chair`／`sofa`／**`char_chair_left`（S05）** **0.304** | **0.139** | 狗同客廳平面；S05 狗面左、人面右 |
| S09 告別 | `char_right_farewell` **0.36** | **0.139** | 翻轉用 xzoom |
| 病床 | `char_right` **0.36** | sick **0.139** | 同尺只改 xalign |

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
| S08 `char_right_walk` **0.32** | walk **0.124** | SCALE alley |

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
| 日常 `char_right_entrance` **0.33** | **0.128** | S08／S09 同尺 |
| S02 抱走 `char_entrance_carry` **0.33** | 合成 | 大門／鞋櫃 |

### 走廊／護衛 `corridor`

| 人現行 | 狗現行 | 備註 |
|--------|--------|------|
| **0.36** | pair／behind **0.139**；nudge **0.139** | 同客廳幼犬比 |

### 巷口散步 `alley`

| 人現行 | 狗現行 | 備註 |
|--------|--------|------|
| **0.32** | **0.124** | far／mid／near／behind 同尺 |

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
| 06 | entrance／living pair；nudge | — |
| 07 | living 病床；kitchen 門檻 | office |
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
6. 禁止把 A 場的 zoom 抄到 B 場。後門換 pose 仍大小不一：改 `DOG_POSE_SCALE`（content bbox），不要拆兩把場景 zoom。

---

*更新：2026-09-06｜S05 早會三姿；S04 客廳趴姿對齊 parallel；S02 後門改 `s04-anxious`；數字見 scale.rpy／script.rpy*
