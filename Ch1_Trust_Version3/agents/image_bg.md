# Version3 背景命名與家族｜image_bg

> 風格／角色外型見 [`image.md`](image.md)；狗外型鎖定見 [`image_dog.md`](image_dog.md)（**Option B｜wiry**）  
> 對齊：[`game_guild.md`](game_guild.md) · `outline_trilogy_ch1_10sections.md`  
> **預設生圖：Cursor `GenerateImage`**；FLUX 2 Pro（`fal-ai/flux-2-pro`）僅備援  
> 路徑：`Ch1_Trust_Version3/assets/bg/`  
> **背景無人無狗**；狗疊層必須對齊 `dog-ref-canonical.png`。

---

## 0. 與 game_guild 對齊（背景產製原則）

| guild 規則 | 背景落地 |
|------------|----------|
| 十段主幹固定 | 只為 S01～S10 列 place；**不**為適應日記加多餘房間 |
| 軟分軌 | **同一 place／light**；信任高低**不**另產背景，改狗距離層 |
| 開場 ≤15 分 | P0 必須先有：`convenience`／`backdoor`／`living` |
| 場次 A（S01～S04） | `living` · `backdoor` · `stairwell` 齊即可試玩 |
| 結局差異 | S10 仍用 `living-night`；A～D 差在疊層／CG，不換房子 |

**禁止：** 為低／中／高信任各畫一套客廳。

---

## 1. 檔名格式（鎖定）

```text
bg-{place}-{light}.png
```

| 段 | 含義 | Version3 允許值 |
|----|------|-----------------|
| `place` | 地點／空間 | `living` · `convenience` · `backdoor` · `stairwell` · `corridor` · `alley` · `cafe` · `kitchen` · `office` · `entrance` · `street` |
| `light` | 日夜／光暗 | `day` · `night` · `dusk` · `rain`（僅外景需天氣時） |

**範例：** `bg-living-night.png` · `bg-backdoor-night.png` · `bg-stairwell-night.png` · `bg-cafe-day.png`

### 劇情時段 ↔ light（審查必對）

| 劇情時段 | light | Section 例 |
|----------|-------|------------|
| 清晨／上午／午後白天 | `day` | S04 日間安靜、S05 早會、S06 走廊、S08 巷口、S09 咖啡廳 |
| 傍晚／夜／第一夜 | `night` | S01 加班夜、S02 後門、S03 樓梯間、S07 生病夜、S10 停電／颱風夜 |
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
| **`bg-stairwell-night.png`** | stairwell | night | **樓梯基準** | **S03** 臨時國界 |
| `bg-convenience-night.png` | convenience | night | 超商基準 | S01／S02 店內（微波／結帳） |

### 3.2 P1（場次 B／C）

| 檔名 | Place | Light | 用途 |
|------|-------|-------|------|
| `bg-corridor-day.png` | corridor | day | **S06** 公寓走廊／被看見 |
| `bg-alley-day.png` | alley | day | **S08** 巷口轉角（走到轉角就好） |
| `bg-cafe-day.png` | cafe | day | **S09** 咖啡廳門口（差點送走） |
| `bg-entrance-night.png` | entrance | night | 玄關過渡；S03→S04 進門 |
| `bg-kitchen-day.png` | kitchen | day | S04 門口記憶點（可選；或以 living 表現門檻） |

### 3.3 P2（可省略／後補）

| 檔名 | Place | Light | 用途 |
|------|-------|-------|------|
| `bg-office-night.png` | office | night | S01 加班；可用黑場省略 |
| `bg-street-night.png` | street | night | 通勤巷路；若與 alley／backdoor 重複可併 |
| `bg-alley-night.png` | alley | night | S08 夜變體（通常不需要） |

### 3.4 與 V2 舊 place 的關係

| V2 常用 | V3 態度 |
|---------|---------|
| `petshop`／`clinic`／`treestreet` | **非 Ch1 主幹**；勿當 Version3 優先產圖 |
| `street-night` 雨夜紙箱 | 相遇改 **`backdoor-night`**；勿再當 S02 主圖 |
| `living-*` | **沿用家族**；構圖可繼承，用途改對十段 |

---

## 4. Section × bg 速查

| Sec | 建議 bg 序列 | light 注意 |
|-----|--------------|------------|
| 01 | `office-night`（可省）→ `convenience-night` → `living-night` | 全夜 |
| 02 | `convenience-night` → **`backdoor-night`** →（過渡）`entrance-night`／`living-night` | 傍晚／夜 |
| 03 | **`stairwell-night`** → 房門走廊可併 stairwell／entrance | 夜→清晨可切 living-day 鉤子 |
| 04 | `living-day`（主）／`kitchen-day`（門口） | 日；夜安靜可用 living-night |
| 05 | `living-day` | 日 |
| 06 | `corridor-day` | 日 |
| 07 | `living-night` | 病中夜 |
| 08 | `alley-day` → `living-day`／`living-night` | 外出日 |
| 09 | `cafe-day` →（留下）`living-*` | 日 |
| 10 | `living-night` | 停電／颱風夜；結局睡姿靠疊層 |

**軟分軌提醒：** S05～S08 低／中／高信任共用上表 bg，只換狗 pose（見 `image.md` §0／§6.2）。

---

## 5. 各 place 構圖要點（生圖）

### living（基準：night）

- 海軍／深色沙發、暖燈、落地窗／陽台望城市、書櫃、植栽、米白地毯、木地板
- **可留空牆掛勾**（S10 鑰匙＋牽繩道具位）
- day：只改自然光；家具不動

### convenience

- 台灣超商店內：微波區、冷櫃色溫、高腳椅剪影；**禁可讀招牌文字**
- 無人無狗

### backdoor（S02 核心）

- 卸貨後門／機車棚陰影、壓扁紙箱、垃圾桶輪廓、濕紙箱＋隔夜油氣氛
- **空場景**；狗由疊層表現「紙箱邊」
- 夜／傍晚冷靛＋一點遠燈

### stairwell（S03 核心）

- 現代化公寓一樓梯廳：樓梯、髮絲紋電梯門、住家門縫光
- 室內燈具必須可見：嵌燈、壁燈與電梯上方柔和 LED；暖琥珀照明對比樓梯窗外冷靛夜色
- 可留外套／紙盤水的空間感（道具也可疊層）
- 無人無狗

### corridor（S06）

- 公寓走廊：門排、地板、日光或窗光
- 留「擋在中間」的站位空間（中央偏左／右清空）
- 日光須保留牆面與地磚筆觸，禁止大面積洗白／過曝

### alley（S08）

- 巷口轉角、樹／電杆、機車可能經過的空間感
- 柔和日間光、曝光平衡；禁曝白牆面、禁文字

### cafe（S09）

- 咖啡廳**門口／外觀**為主（交牽繩發生在門外）
- 禁可讀店名；留牽繩交接的站位空間

### kitchen（可選）

- 小廚房＋門檻線清晰（S04「只到門口」）
- 與 living 建材色一致

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
| `bg-stairwell-night.png` | `bg stairwell_night` |
| `bg-convenience-night.png` | `bg convenience_night` |
| `bg-corridor-day.png` | `bg corridor_day` |
| `bg-alley-day.png` | `bg alley_day` |
| `bg-cafe-day.png` | `bg cafe_day` |

---

## 8. 審查清單

- [ ] 檔名符合 `bg-{place}-{light}.png`
- [ ] 同 place 家具／構圖對齊基準
- [ ] 僅光暗／日夜差異，不是另一間房子
- [ ] **時段正確**（早／午→day；傍晚／夜→night）
- [ ] 無人無狗無字、無信任 HUD
- [ ] S02 主圖為 **backdoor**（非 V2 雨夜紙箱街）
- [ ] 軟分軌未為信任高低複製多套 bg
- [ ] 未自動開遊戲

---

## 9. 2026-07-19 背景重產紀錄

| 檔名 | 修正結果 |
|------|----------|
| `bg-alley-day.png` | S08 巷口改柔和日光、平衡曝光；保留轉角、電杆、街樹與機車通行空間 |
| `bg-corridor-day.png` | S06 走廊壓低洗白高光，改暖中性厚筆油畫 |
| `bg-street-night.png` | 雨夜街景由偏寫實概念圖改為深靛＋暖燈的厚筆印象派 |
| `bg-stairwell-night.png` | S03 改現代公寓梯廳，加入嵌燈、壁燈與電梯 LED，保留外套／水盤疊層空間 |

目前 `assets/bg/` 共 **10 張正式背景**，皆為遊戲引用資產；不保留 `*-regen` 中介圖。

---

*更新：2026-07-19｜背景風格統一、曝光修正、現代梯廳落地與資產清理*
