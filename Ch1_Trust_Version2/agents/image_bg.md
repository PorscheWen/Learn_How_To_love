# Version2 背景命名與家族｜image_bg

> 風格／角色外型仍見 [`image.md`](image.md)  
> 模型：**FLUX 2 Pro**（`fal-ai/flux-2-pro`）  
> 路徑：`Ch1_Trust_Version2/assets/bg/`（Ren'Py `game/assets` 為 junction）

---

## 1. 檔名格式（鎖定）

```text
bg-{place}-{light}.png
```

| 段 | 含義 | 允許值（可擴充） |
|----|------|------------------|
| `place` | 地點／空間 | `living` · `street` · `treestreet` · `entrance` · `petshop` · `clinic` · `kitchen` · `bathroom` … |
| `light` | 日夜／光暗 | `day` · `night` · `dusk` · `rain`（僅街景等需天氣時） |

**範例：** `bg-living-night.png` · `bg-living-day.png` · `bg-street-night.png` · `bg-treestreet-day.png` · `bg-clinic-day.png` · `bg-petshop-day.png`

### 劇情時段 ↔ light（審查必對）

| 劇情時段 | 應用 light | 例 |
|----------|------------|-----|
| 清晨／上午／午後白天 | `day` | Day2 清晨便便、Day7 日間路程 `treestreet-day` |
| 傍晚趕回家／夜／第一夜 | `night` | Day1 雨夜後客廳；Day2 日終 |
| 雨夜街景 | `night`（街） | Day1 巷口 `bg-street-night` |
| 日間診所 | `day`（clinic） | Day7 候診 `bg-clinic-day` |

**禁止：** 雨夜下班回家仍用 `bg-living-day`（亮白天光）。

### 禁止

| 勿用 | 原因 |
|------|------|
| `bg-apartment-night-living`（詞序亂） | 一律 `place` 在前、`light` 在後 |
| `bg-bedroom-night` 當客廳 | 客廳家族統一用 `living` |
| `bg-pet-shop`（多連字） | 用 `petshop` |
| 同一 place 各張獨立重畫整套家具 | 必須從該 place 的 **基準圖** img2img |

---

## 2. 家族規則（同一 place＝同一張基準）

1. 每個 `place` 指定 **一張基準圖**（通常是最完整構圖的那張，如 `bg-living-night`）。
2. 同 place 的其他 `light` 變體：**只改日夜／光暗／天氣**，家具、空間結構、油畫筆觸必須對齊基準。
3. 產變體：FLUX **edit／img2img**，參考基準（本機路徑改 data-URI；見 `tools/flux_living_from_night.py`）。
4. 背景：**無人、無狗、無動物、無文字／logo**。紙箱僅可空箱＋毛巾，禁鳥巢。

```text
基準 bg-living-night.png
  ├─ bg-living-day.png     ← 同公寓，改為日間／較亮
  └─ （未來）bg-living-dusk.png
```

---

## 3. 目前資產表

| 檔名 | Place | Light | 角色 | 用途 |
|------|-------|-------|------|------|
| **`bg-living-night.png`** | living | night | **基準** | Day1 就寢；Day2 日終 |
| `bg-living-day.png` | living | day | 自 night 變體 | Day2 清晨～取名；Day7 收紙箱 |
| **`bg-street-night.png`** | street | night | **街夜基準** | Day1 巷口／帶回家 |
| `bg-street-day.png` | street | day | 自 night 光暗變體感 | Day3 去寵物店日間巷口 |
| `bg-treestreet-day.png` | treestreet | day | 樹蔭人行道 | Day7 去診所路程 |
| `bg-entrance-night.png` | entrance | night | 玄關／陽台基準 | （延伸場景） |
| `bg-petshop-day.png` | petshop | day | 明亮店內基準；**無入口** | Day3 寵物店 |
| `bg-clinic-day.png` | clinic | day | 獸醫候診室內 | Day7 候診／收養問句 |

### 舊檔對照（已廢止）

| 舊檔名 | 新檔名 |
|--------|--------|
| `bg-apartment-night-living.png` | `bg-living-night.png` |
| `bg-apartment-living-floor.png` | `bg-living-day.png` |
| `bg-bedroom-night.png` | 併入 `living`（刪） |
| `bg-street-rain-night.png` | `bg-street-night.png` |
| `bg-pet-shop.png` | `bg-petshop-day.png` |
| `bg-entrance-night.png` | 不變 |

---

## 4. Ren'Py 標籤

檔名連字 → image 名用底線：

| PNG | `scene` 標籤 |
|-----|----------------|
| `bg-living-night.png` | `scene bg living_night` |
| `bg-living-day.png` | `scene bg living_day` |
| `bg-street-night.png` | `scene bg street_night` |
| `bg-street-day.png` | `scene bg street_day` |
| `bg-treestreet-day.png` | `scene bg treestreet_day` |
| `bg-entrance-night.png` | `scene bg entrance_night` |
| `bg-petshop-day.png` | `scene bg petshop_day` |
| `bg-clinic-day.png` | `scene bg clinic_day` |
| `bg-petshop-day.png` | `scene bg petshop_day` |

定義見 `Renpy_game/game/definitions.rpy`。

---

## 5. 產圖流程

```powershell
# living：以 night 為基準產 day
python Ch1_Trust_Version2\tools\flux_living_variants.py

# 其他獨立基準（text-to-image／edit）
python Ch1_Trust_Version2\tools\flux_oil_bgs.py
```

### living 變體 prompt 要點

- **基準保持：** 海軍沙發、暖燈、落地窗陽台＋城市、書櫃、Monstera、米白地毯、深色木地板、油畫厚筆觸  
- **day：** 日間／較亮自然光，可保留空紙箱＋毛巾；禁鳥巢  
- **night：** 暖金燈 × 冷靛夜空（基準勿隨意覆寫）

### petshop 要點

- 明亮店內；貨架＋櫃檯；**無入口／無對外門**；禁可讀文字

---

## 6. 審查清單

- [ ] 檔名符合 `bg-{place}-{light}.png`
- [ ] 同 place 家具／構圖對齊基準
- [ ] 僅光暗／日夜差異，不是另一間房子
- [ ] **時段正確**（早／午→day；傍晚／夜→night）
- [ ] 無人無狗無字
- [ ] Ren'Py `definitions.rpy` 與劇本 `scene` 已同步
- [ ] 未自動開遊戲

---

*更新：2026-07-12｜時段對照＋Day1～2 用途*
