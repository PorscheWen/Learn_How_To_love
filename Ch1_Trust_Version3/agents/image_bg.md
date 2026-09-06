# Version3 背景命名與家族｜image_bg

> 風格／角色外型見 [`image.md`](image.md)；狗外型鎖定見 [`image_dog.md`](image_dog.md)（**Option B｜wiry**）  
> 人／狗 zoom 比例見 [`image_scale.md`](image_scale.md)；**S02 數字**在 `Renpy_game/game/scale.rpy`（`SCALE_S02`）  
> 對齊：[`game_guild.md`](game_guild.md) · `outline_trilogy_ch1_10sections.md`  
> **預設生圖：Cursor `GenerateImage`**；FLUX 2 Pro（`fal-ai/flux-2-pro`）僅備援  
> 路徑：`Ch1_Trust_Version3/assets/bg/`  
> **背景無人無狗**；狗疊層必須對齊 `dog-ref-canonical.png`（錨點 `assets/dog/refs/`，2026-07-25）。  
> **風格錨點：** `assets/bg/refs/`（四張定稿）＋下方 **BG ONE-LINER**

---

## 0.5 背景一句鎖定（BG ONE-LINER｜未來背景必貼）

自定稿歸納來源：`entrance-day` · `alley-day` · `corridor-day` · `living-night`  
錨點檔：`assets/bg/refs/ref-entrance-day.png` · `ref-alley-day.png` · `ref-corridor-day.png` · `ref-living-night.png`

```text
Thick-impasto impressionistic oil painting of quiet everyday Taiwanese residential spaces—warm amber lamp glow or sunlit ochre walls against cool indigo night sky or soft daylight; soft blended edges, tactile brush texture on wood floors, plaster walls, Monstera plants and navy sofa accents indoors, metal window bars and sidewalk potted plants outdoors; empty of people and dogs, no readable text—storybook visual-novel background, not a photograph, not anime.
```

| 共通特徵（四張共有） | 落地 |
|----------------------|------|
| 厚塗／可見筆觸 | impasto，禁寫實照片感 |
| 柔邊暈染 | soft blended edges，禁硬黑線 |
| 暖琥珀／赭石光 | 室內燈或日間牆面 |
| 冷靛夜外（有外景時） | 陽台／巷口天空對比 |
| 台灣日常住家語彙 | 木地板、鞋櫃、Monstera、鐵窗、騎樓盆栽 |
| 空場景 | 無人無狗無字 |

**產圖公式：** `BG ONE-LINER` ＋ `本場 place／light／構圖一句` ＋ reference（室內→`ref-living-night`；外景→`ref-alley-day`；走廊→`ref-corridor-day`；玄關→`ref-entrance-day`）。

---

## 0. 與 game_guild 對齊（背景產製原則）

| guild 規則 | 背景落地 |
|------------|----------|
| 十段主幹固定 | 只為 S01～S10 列 place；**不**為適應日記加多餘房間 |
| 軟分軌 | **同一 place／light**；信任高低**不**另產背景，改狗距離層 |
| 開場 ≤15 分 | P0 必須先有：`convenience`／`backdoor`／`living` |
| 場次 A（S01～S04） | `living` · `backdoor` · `gate` · `entrance` 齊即可試玩 |
| 結局差異 | S10 仍用 `living-night`；A～D 差在疊層／CG，不換房子 |

**禁止：** 為低／中／高信任各畫一套客廳。

---

## 1. 檔名格式（鎖定）

```text
bg-{place}-{light}.png
```

| 段 | 含義 | Version3 允許值 |
|----|------|-----------------|
| `place` | 地點／空間 | `living` · `convenience` · `backdoor` · `gate` · `entrance` · `stairwell` · `corridor` · `alley` · `cafe` · `kitchen` · `office` · `street` |
| `light` | 日夜／光暗 | `day` · `night` · `dusk` · `rain`（僅外景需天氣時） |

**範例：** `bg-living-night.png` · `bg-backdoor-night.png` · `bg-stairwell-night.png` · `bg-cafe-day.png`

### 劇情時段 ↔ light（審查必對）

| 劇情時段 | light | Section 例 |
|----------|-------|------------|
| 清晨／上午／午後白天 | `day` | S04 日間安靜、S05 早會、S06 走廊、S08 巷口、S09 咖啡廳 |
| 傍晚／夜／第一夜 | `night` | S01 加班夜、S02 後門、S03 大門、S07 生病夜、S10 停電／颱風夜 |
| 暮色玄關（可選） | `dusk`／`night` | 進門過渡可用 `entrance-night` |

**禁止：** 夜段劇情誤用 `*-day`（例：S02 後門用日間光）。

### 禁止檔名

| 勿用 | 原因 |
|------|------|
| `bg-apartment-night-living` | 一律 `place` 在前、`light` 在後 |
| `bg-bedroom-night` 當客廳主戰場 | 臥室戲可併 `living` 或另建 `bedroom` 家族；Ch1 優先 living |
| `bg-pet-shop`／`bg-petshop-*` 當主線 | V3 **主線非寵物店**（見切割表） |
| 同一 place 各 light 獨立重畫整套家具 | 必須從該 place **基準圖** img2img |
| `bg-trust-high-living` 這類信任後綴 | 信任不進檔名 |

---

## 2. 家族規則（同一 place＝同一張基準）

1. 每個 `place` 指定 **一張基準圖**（通常構圖最完整的 night 或 day）。
2. 同 place 其他 `light`：**只改日夜／光暗／天氣**，家具與空間結構對齊基準。
3. 產變體：Cursor `GenerateImage` 附基準圖；FLUX **edit／img2img** 僅作備援。
4. 背景：**無人、無狗、無動物、無文字／logo、無信任 HUD**。紙箱僅空箱／壓扁紙箱＋毛巾，禁鳥巢。道具可留：鞋、掛勾、牽繩空掛、耳機在椅背（無人物時）。

```text
基準 bg-living-night.png
  ├─ bg-living-day.png
  └─ （可選）bg-living-dusk.png
```

---

## 3. Version3 資產表（S01～S10）

### 3.1 P0（開場＋場次 A · 先產）

| 檔名 | Place | Light | 角色 | 用途（Section） |
|------|-------|-------|------|-----------------|
| **`bg-living-night.png`** | living | night | **living 基準** | S01 回家；S04／S07／S10 |
| `bg-living-day.png` | living | day | 自 night 變體 | S04 平行安靜；S05 視訊 |
| **`bg-backdoor-night.png`** | backdoor | night | **後門基準** | **S02** 卸貨後門／機車棚／紙箱邊 |
| **`bg-gate-night.png`** | gate | night | **大門基準** | **S03** 公寓大門外 |
| **`bg-street-night.png`** | street | night | 街景 | 可作街景／過場 |
| **`bg-stairwell-night.png`** | stairwell | night | 梯廳（夜） | S03 樓梯間段落使用 |
| `bg-convenience-night.png` | convenience | night | 超商基準 | S01／S02 店內（微波／結帳） |

### 3.2 P1（場次 B／C）

| 檔名 | Place | Light | 用途 |
|------|-------|-------|------|
| `bg-stairwell-day.png` | stairwell | day | **S06** 梯廳（日）／被看見；自 `bg-stairwell-night` 日光化，同構圖 |
| `bg-alley-day.png` | alley | day | **S08** 巷口轉角（走到轉角就好） |
| `bg-cafe-day.png` | cafe | day | **S09** 咖啡廳門口（差點送走） |
| `bg-entrance-night.png` | entrance | night | 玄關基準；**S03** 門檻／帶回屋內 |
| `bg-entrance-day.png` | entrance | day | S03 清晨；S04 `delayed_entry`；**S08** 穿帶／出門／返家；**S09** 週六扣帶出門 |
| `bg-kitchen-day.png` | kitchen | day | S04 門口記憶點（**已落地**） |
| `bg-kitchen-night.png` | kitchen | night | **S01** 開冰箱（自 day 夜化；**已落地**） |

### 3.3 P2（可省略／已補）

| 檔名 | Place | Light | 用途 |
|------|-------|-------|------|
| `bg-office-night.png` | office | night | S01 加班；可用黑場省略 |
| `bg-street-night.png` | street | night | 通勤巷路；若與 alley／backdoor 重複可併 |
| `bg-alley-night.png` | alley | night | S08 夜變體（**已落地**） |
| `bg-living-dusk.png` | living | dusk | living 暮色變體（**已落地**） |

### 3.4 與 V2 舊 place 的關係

| V2 常用 | V3 態度 |
|---------|---------|
| `petshop`／`clinic`／`treestreet` | **非 Ch1 主幹**；勿當 Version3 優先產圖 |
| `street-night` 雨夜紙箱 | 相遇改 **`backdoor-night`**；勿再當 S02 主圖 |
| `living-*` | **沿用家族**；構圖可繼承，用途改對十段 |
| `clinic` | **S02 `vet_first` 短場**可用 `bg-clinic-night`；非十段主幹常駐 |

---

## 4. Section × bg 速查

| Sec | 建議 bg 序列 | light 注意 |
|-----|--------------|------------|
| 01 | `office-night`（可省）→ `convenience-night` → **`entrance-night`** → `living-night` → **`kitchen-night`** → `living-night` | 全夜；回家三拍：玄關／客廳坐下／廚房冰箱 |
| 02 | **`office-night`** → `convenience-night` → `street-night` → **`backdoor-night`** → `street-night` →（`vet_first`：**`clinic-night`**）／否則 **`entrance-night`** → `living-night` | 傍晚／夜；急診短場後進 S03 大門 |
| 03 | **`gate-night`** → **`entrance-night`** → `living-night` →（清晨）`entrance-day`／`living-day` | 夜→清晨；大門外／門內靠玄關過渡 |
| 04 | `living-day`（主）／`kitchen-day`（門口） | 日；夜安靜可用 living-night |
| 05 | `living-day` | 日 |
| 06 | `stairwell-day` → `entrance-day` | 日；與 S03 夜梯廳同構圖 |
| 07 | `living-night` → **`kitchen-night`（倒水）** → `living-night` → `office-night` | 病中夜；倒水切廚房 |
| 08 | **`entrance-day`** → **`alley-day`** → `entrance-day` → `living-day` → **`office-night`（週一）** | 外出日；尾鉤切辦公室 |
| 09 | `office-night` → **`living-night`（三晚）** → `living-day` → **`entrance-day`** → `cafe-day` | 猶豫夜回客廳 |
| 10 | 送走：`alley-night` → `entrance-night` → `kitchen-night` → `living-night`；留下：`street-night` → `entrance-night` → `living-night` → `kitchen-night` → `living-night` | 停電／颱風夜在客廳 |

**軟分軌提醒：** S05～S08 低／中／高信任共用上表 bg，只換狗 pose（見 `image.md` §0／§6.2）。

---

## 5. 各 place 構圖要點（生圖）

### living（基準：night）

- 海軍／深色沙發、暖燈、落地窗／陽台望城市、書櫃、植栽、米白地毯、木地板
- **可留空牆掛勾**（S10 鑰匙＋牽繩道具位）
- day：只改自然光；家具不動
- **立繪尺：** 人／狗見 [`image_scale.md`](image_scale.md)。全景站 `char_right`／`left` **0.36**；狗 **0.139**（幼犬比，far／mid／near 同尺）。S02 抱狗 `char_living` **0.32**（落地窗；合成圖不另疊狗）

### convenience

- 台灣超商店內：微波區、冷櫃色溫、高腳椅剪影；**禁可讀招牌文字**
- 無人無狗
- **立繪尺：** 店員／予安 **0.29**（櫃面到腰）。無狗；若加狗建議 **0.304**。見 `image_scale.md`

### backdoor（S02 核心）

- 卸貨後門／機車棚陰影、壓扁紙箱、垃圾桶輪廓、濕紙箱＋隔夜油氣氛
- **空場景**；狗由疊層表現「紙箱邊」
- 夜／傍晚冷靛＋一點遠燈
- **立繪尺（S02 對景）：** 予安 **0.31**（頭低於卸貨門楣）、狗 **0.12**（幼犬≈人×0.28；far／mid／near 同尺，四姿 bbox 對齊）。見 `scale.rpy`

### gate（S03 核心｜公寓大門）

- 台灣公寓**大門外側**：鐵門／門牌／騎樓磁磚、感應燈；留外套與水盤疊層空地
- 構圖朝向大門，巷口／馬路在背景一側
- 正式檔：`bg-gate-night.png` → `bg gate_night`
- 無人無狗無字
- **立繪尺：** S02／S03 抱狗 `char_gate` **0.28**（鐵門／木門框）。見 `image_scale.md`

### stairwell（舊資產）

- 現代化公寓梯廳：保留檔案，S03 主幹不再使用
- 可留外套／紙盤水的空間感（道具也可疊層）
- 無人無狗
- **立繪尺：** S03 門外狗窩 `dog_far_stair` **0.187**（深度例外：門墊中遠景）。見 `image_scale.md`

### corridor（S06）

- 公寓走廊：門排、地板、日光或窗光
- 留「擋在中間」的站位空間（中央偏左／右清空）
- 日光須保留牆面與地磚筆觸，禁止大面積洗白／過曝
- **立繪尺：** 人多 `char_right` **0.36**；狗 pair／behind **0.139**（幼犬比，同尺）。見 `image_scale.md`

### alley（S08）

- 巷口轉角、樹／電杆、機車可能經過的空間感
- **道具疊層（已接）：** `prop/scooter-parked.png`（進巷即顯示，停放空車）；`prop/scooter-pass.png`（轉角呼嘯切過，驚嚇拍短暫出現後 hide；transform **×0.8**）
- 巷口進場：`yuan walk`（走路）＋狗 `dog_behind_walk`（身後不願前進）→ 依信任慢慢前移 → 轉角機車嚇退回身後；樹下停等才切 `yuan leash`（蹲）
- **立繪尺：** `char_right_walk` **0.32**；狗 walk **0.124**（幼犬比；far／mid／near／behind 同尺）。見 `image_scale.md`
- 柔和日間光、曝光平衡；禁曝白牆面、禁文字

### cafe（S09）

- 咖啡廳**門口／外觀**為主（交牽繩發生在門外）
- 禁可讀店名；留牽繩交接的站位空間
- 疊層：同事左（`char_left_cafe`）、予安右（`char_right_cafe`）、狗依劇情 near_guard／near_home／mid
- **立繪尺：** 人 **0.36**；狗 **0.139**（幼犬比；guard／home／mid 同尺）。見 `image_scale.md`

### entrance（S03 門檻；S08／S09 出門）

- 台灣公寓**玄關內側**：門板（貓眼／門把）、地墊、鞋櫃、空牆掛勾
- 構圖朝向大門，留地墊旁空地給狗疊層（`dog_entrance_far`／`mid`；S09 用 `*_s09`）
- night：暖壁燈；day：清晨／日間門縫側光，家具不動
- **用途：** 門內外過渡（S03）；穿胸背帶、跨門檻、返家解帶（S08）；週六扣帶出門（S09）
- 無人無狗無字
- **立繪尺：** 人 `char_right_entrance` **0.33**；狗 **0.128**（幼犬比；far／mid 同尺）。見 `image_scale.md`

### kitchen（可選）

- 小廚房＋門檻線清晰（S04「只到門口」）
- 與 living 建材色一致
- **立繪尺：** 人 `char_kitchen_near`／`sink` **0.52**（POV）；狗門檻 `dog_kitchen_threshold` **0.19**（深度例外，勿套 1.048）。見 `image_scale.md`

### office（S01／S02 加班；S07／S09 可短用）

- 夜間隔間、桌燈、椅背、窗外城市；無人無狗無字
- **立繪尺：** `char_office` **0.28**（椅背／桌高到腰）。S02 開場 `xalign 0.66` 站桌椅右側走道。無狗；若加狗建議 **0.293**。予安用 `headphones_off`。勿套 `char_center`

### street（S01／S02 巷口過場）

- 台灣住宅巷：左側木門／一樓窗、路寬約一台車、盆栽與路燈
- 無人無狗無字
- **立繪尺：** `char_street`／`char_street_carry` **0.23**（頭頂低於左側門框；抱狗合成、不另疊狗）。勿套 `char_center`

### clinic（S02 `vet_first` 短場）

- 夜間巷口**動物醫院外觀**：玻璃門／大面窗望進等候區；冷靛夜 vs 暖琥珀室內燈
- **必備：** 門楣燈箱招牌（僅醫療十字＋爪印符號，**禁可讀文字／店名**）；木櫃檯＋檯燈；等候椅；體重秤；空牽繩掛勾；不可辨識海報色塊；診療室門縫／不鏽鋼台邊暗示
- 外：濕石板／騎樓感、街燈、停放機車、盆栽；**無人無狗無動物**
- 正式檔：`bg-clinic-night.png` → `bg clinic_night`
- **立繪尺：** S02 抱狗 `char_clinic` **0.27**（窗內木櫃檯：`xalign 0.56`／`ypos 0.64`；勿站右側玻璃門）。見 `image_scale.md`

---

## 6. 產圖流程（建議）

```powershell
# 1) P0 基準：living-night、backdoor-night、stairwell-night、convenience-night
# 2) living-day 自 living-night img2img
# 3) P1：corridor / alley / cafe
```

### living 變體要點

- **基準保持：** 沙發、暖燈、窗、書櫃、植栽、地毯、木地板、油畫厚筆觸  
- **day：** 日間較亮自然光  
- **night：** 暖金燈 × 冷靛夜空（基準勿隨意覆寫）  
- S10 停電變體：可另產 `bg-living-night` 的「燈暗／手電」edit，或同一張壓暗處理——**仍屬 living 家族**

---

## 7. 引擎標籤（若用 Ren'Py／等同）

檔名連字 → 標籤用底線：

| PNG | 標籤例 |
|-----|--------|
| `bg-living-night.png` | `bg living_night` |
| `bg-backdoor-night.png` | `bg backdoor_night` |
| `bg-gate-night.png` | `bg gate_night` |
| `bg-stairwell-night.png` | `bg stairwell_night` |
| `bg-convenience-night.png` | `bg convenience_night` |
| `bg-street-night.png` | `bg street_night` |
| `bg-clinic-night.png` | `bg clinic_night` |
| `bg-stairwell-day.png` | `bg stairwell_day` |
| `bg-alley-day.png` | `bg alley_day` |
| `bg-cafe-day.png` | `bg cafe_day` |
| `bg-entrance-night.png` | `bg entrance_night` |
| `bg-entrance-day.png` | `bg entrance_day` |
| `bg-kitchen-day.png` | `bg kitchen_day` |
| `bg-kitchen-night.png` | `bg kitchen_night` |
| `bg-living-dusk.png` | `bg living_dusk` |
| `bg-alley-night.png` | `bg alley_night` |

---

## 8. 審查清單

- [ ] 已貼 **BG ONE-LINER**（`image_bg.md` §0.5）並附對應 `assets/bg/refs/` reference
- [ ] 檔名符合 `bg-{place}-{light}.png`
- [ ] 同 place 家具／構圖對齊基準
- [ ] 僅光暗／日夜差異，不是另一間房子
- [ ] **時段正確**（早／午→day；傍晚／夜→night）
- [ ] 無人無狗無字、無信任 HUD
- [ ] S02 主圖為 **backdoor**（非 V2 雨夜紙箱街）
- [ ] 軟分軌未為信任高低複製多套 bg
- [ ] S02 立繪對景尺：巷口／後門／診所／超商未套客廳 `char_center`／`char_left`／`char_right`
- [ ] 未自動開遊戲

---

## 9. 背景重產紀錄

### 2026-07-25｜全量重產（BG ONE-LINER）

- **備份：** `assets/_backup_unused/bg/_backup_20260725_125336/`（重產前 13 張原檔）
- **公式：** BG ONE-LINER ＋ place／light／構圖一句 ＋ `assets/bg/refs/` 對應 reference
- **尺寸：** 全部落地 **2048×1152**
- **ref 對應：**
  - 室內 living／office／convenience → `ref-living-night`
  - 玄關 entrance → `ref-entrance-day`
  - 外景 alley／street／gate／backdoor／cafe → `ref-alley-day`（cafe／gate 另附 entrance）
  - 走廊 corridor／stairwell → `ref-corridor-day`

| 檔名 | place | light | 備註 |
|------|-------|-------|------|
| `bg-living-night.png` | living | night | living 基準 |
| `bg-living-day.png` | living | day | 自 night 變體 |
| `bg-entrance-day.png` | entrance | day | 玄關基準 |
| `bg-entrance-night.png` | entrance | night | 自 day 變體 |
| `bg-alley-day.png` | alley | day | 外景錨點 |
| `bg-corridor-day.png` | corridor | day | 走廊錨點 |
| `bg-gate-night.png` | gate | night | S03 大門 |
| `bg-backdoor-night.png` | backdoor | night | S02 |
| `bg-cafe-day.png` | cafe | day | S09 |
| `bg-convenience-night.png` | convenience | night | S01／S02 |
| `bg-office-night.png` | office | night | S01／S07 |
| `bg-street-night.png` | street | night | 街景 |
| `bg-stairwell-night.png` | stairwell | night | 舊資產保留重產 |
| `bg-kitchen-day.png` | kitchen | day | 可選補產｜S04 門檻 |
| `bg-alley-night.png` | alley | night | 可選補產｜alley 夜變體 |
| `bg-living-dusk.png` | living | dusk | 可選補產｜living 暮色 |

重產後 `refs/` 四張錨點已同步為本次正式圖縮圖用途之同構圖檔。可選三張於 2026-07-25 依同一公式補齊。

### 2026-08-02｜S06 走廊改梯廳日景

- `bg-corridor-day.png` 退役 → 移入 `assets/_backup_unused/bg/_backup_20260802/`
- 新圖 `bg-stairwell-day.png`：以 `bg-stairwell-night.png` 為參考圖，
  NanoBanana（`nano-banana-2`，edit 模式，`tools/nanobanana-edit.py`）日光化，
  電梯／樓梯／窗／盆栽／大門構圖完全對齊夜版 → S03 夜與 S06 日同一梯廳，場景連續
- `script.rpy`：`image bg corridor_day` → `image bg stairwell_day`；S06 開場 scene 同步改

### 2026-08-02｜stairwell-day 電梯／門口對調

- `bg-stairwell-day.png`：NanoBanana edit（`nano-banana-2`）將**左側電梯**與**右側木門**對調
  → 現為左門口（壁燈＋地墊）／中央樓梯窗／右電梯
- 對調前原檔：`assets/_backup_unused/bg/_backup_20260802/bg-stairwell-day_before_swap.png`

### 2026-08-02｜stairwell-night 自 day 同步夜景

- `bg-stairwell-night.png`：以對調後的 `bg-stairwell-day.png` 為參考，
  NanoBanana（`nano-banana-2`，edit）轉夜景，構圖對齊日版
  → 左門口／中央樓梯窗／右電梯；窗外夜空＋城市燈
- 同步前原檔：`assets/_backup_unused/bg/_backup_20260802/bg-stairwell-night_before_day_sync.png`
- S03 `dog_far_stair`：`xalign 0.22`（靠左側門墊），勿落在中央樓梯口

### 2026-08-04｜clinic-night 重產（招牌／櫃檯／擺設）

- `bg-clinic-night.png`：夜間動物醫院外觀＋玻璃窗望進等候區
  → 門楣燈箱（十字＋爪印、無字）、木櫃檯＋檯燈／螢幕、等候椅、體重秤、空牽繩掛勾、抽象海報
- 舊檔備份：`assets/_backup_unused/bg/_backup_clinic_20260804_015626/`
- 畫布對齊其他 V3 夜景：`2048×1152`

### 2026-09-06｜S02 改對景（每場固定一把尺）

完整表見 **[`image_scale.md`](image_scale.md)**。數字只改 `Renpy_game/game/scale.rpy`（S02＝`SCALE_S02`；S04–S10＝`SCALE`）。人對齊該場門框／椅／櫃；幼犬可見高 ≈ 人 ×0.28～0.37（`dog = char × 0.12/0.31`）。機車道具維持 ×0.8。

| place | 人 zoom | 狗 | 對齊 |
|-------|---------|----|------|
| office | **0.28** | — | 椅／桌到腰 |
| convenience | **0.29** | — | 櫃面到腰 |
| street | **0.23** | 合成 | 左側門框；遇狗前＝抱走 |
| backdoor | **0.31** | **0.12** | 幼犬≈人×0.28；四姿同高 |
| clinic | **0.27** | 合成 | 玻璃門 |
| entrance 抱走 | **0.33** | 合成 | 大門／鞋櫃 |
| living 抱走 | **0.32** | 合成 | 落地窗 |
| gate | **0.28** | 合成 | 鐵門／木門 |
| living 全景 | **0.36** | **0.139** | S04–S10 對景；遠近同尺 |
| kitchen POV | **0.52** | **0.19** | 深度例外 |
| stairwell | — | **0.187** | 深度例外 |
| entrance 日常 | **0.33** | **0.128** | 幼犬比 |
| alley 散步 | **0.32** | **0.124** | 幼犬比 |
| cafe | **0.36** | **0.139** | 幼犬比 |

---

*更新：2026-09-06｜S04–S10 對景收入 scale.rpy `SCALE`；狗幼犬比*
