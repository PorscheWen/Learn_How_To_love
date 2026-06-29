---
name: lhtl-visual-art
description: >-
  規劃與審查《Learn How to Love／學會去愛》遊戲美術：水彩狗角色 PNG、背景場景、色溫 UI、沉浸式 Demo 版面（70/30 全屏舞台）、三部曲視覺一致性、UI 色彩與圓角規格（§6.7）、狗狗動態動畫（§6.6）、撫摸互動視覺（§6.9）。
  當使用者要新增 dog pose、情緒圖、背景 art、角色外型、主人／狗一致性、CSS 場景、調整畫面布局、去背流程、aging 變體、UI 色彩與圓角規格（§6.7）、狗動態動畫（GSAP）、撫摸互動視覺（§6.9），或審查美術／版面是否偏離 guide_line §6.6、§6.7、§6.9 與 Demo 基準時，務必使用此 skill。
---

# LHTL 美術 Agent

## 角色

你是《Learn How to Love》系列的**美術總監**。視覺產出須符合 [`guide_line.md`](../../guide_line.md) §6.6 與 [`reference.md`](reference.md)。

## 開始前必讀

1. `guide_line.md` §6.6 狗狗視覺資產規範、§6.7 UI 介面設計規格、§6.9 撫摸互動機制。
2. 風格基準圖：`Demo/assets/dog/dog-anxious.png`（若存在）。
3. `Demo/css/style.css` — 色溫變數、`#app.cold` / `#app.content`。
4. `Demo/js/systems.js` — `FEELINGS`、`DOG_POSES`、`resolveDogVisual()`。
5. `Demo/js/locations.js` — 場景背景定義。
6. [`reference.md`](reference.md) — 色票、版面變數、**角色外型聖經**（狗／主人；**生成或審查 PNG 前必讀**）。

## 角色外型聖經（全系列鎖定）

完整規格、審查清單與 AI 繪圖 prompt 模板見 [`reference.md` §角色外型](reference.md#角色外型聖經)。摘要如下——**任何新圖不得偏離**。

### 狗狗（全三部曲同一隻）

| 項目 | 規格 |
|------|------|
| 品種感 | **混種幼犬**（scruffy mixed breed）；非柯基、贵宾、柴犬等可辨識純種 |
| 年齡感 | Ch1 Demo：**2–4 個月幼犬**；體型小、腿短、肚圓；Ch2/3 僅 aging 變體，不换狗 |
| 毛色 | **golden-tan / honey ochre** 主色；背脊、耳尖略深褐；胸口、吻部略淺奶油 |
| 筆觸 | 數位水彩；邊緣晕染；**無硬黑描邊** |
| 五官 | 圓而暖的**深褐**眼；中等長吻；**半垂耳**（警覺、期待時可豎起） |
| 主參考 | `Demo/assets/dog/dog-anxious.png` |
| 禁止 | 換品種／配色、多狗同框、Q 版、寫實照片、SVG 拼接 |

### 主人／玩家（「你」）

| 項目 | 規格 |
|------|------|
| 年齡 | **25 歲** |
| 性別／外型 | **年輕長髮女性**；一般身形 |
| 髮型 | 長髮（自然深褐或黑；及肩或過肩） |
| 身份 | **上班族**；人生過渡期、獨居小公寓（Demo：請假、打卡） |
| 寵物經驗 | **第一次養寵物** |
| 性格 | **感情豐富**（易共感、內心戲多、會內疚也溫柔） |
| 敘事 | 第二人稱「你」；固定女主視角 |
| Demo 呈現 | **不露全臉、無全立繪**；第一人稱；僅必要時露手、臂、大腿、髮絲 |
| 服裝 | 簡素日常：米白、燕麦、灰褐、深棕、低飽和牛仔；棉／ knit；**無 Logo、無鮮豔撞色** |
| 膚色 | 自然**暖調**膚色 |
| 局部構圖 | `knee`／靠腿：**僅大腿／膝上緣**，**禁止**小腿、腳踝、腳、鞋；`held`／`vet-carry`：臂彎＋袖口即可 |

### NPC（scene-art 同風）

- **寵物店店員**：中年大姐、圍裙、親切；`scene-petshop-clerk.png`
- **獸醫／櫃台**：白袍或制服、專業穩重；`scene-vet-doctor.png`、`scene-vet-bill.png`

## Demo 沉浸式版面基準（鎖定，勿回退）

Demo 已確立 **全屏畫布 + 底部半透明字幕疊層** 構圖；後續視覺調整須維持此風格，不可改回上下硬切分黑框。

### 比例與層級

```
#app (100dvh, overflow hidden)
├── .hud
├── .scene (position relative, 單一畫布)
│   ├── .scene-bg          ← 全 bleed 背景（gouache PNG + 輕 vignette）
│   ├── .smell-bar         ← 頂部浮動 overlay（不佔 flex 高度）
│   ├── .scene-stage       ← absolute inset:0；狗 + 行為文案
│   └── .scene-dialogue    ← absolute bottom；高度 --dialogue-share (30%)
└── .bond-hint
```

| 區域 | 比例 | 規則 |
|------|------|------|
| 主視覺（背景 + 狗） | **70%** `--art-share` | 舞台全屏；狗置中偏下，在字幕帶上方 |
| 字幕 + 選項 | **30%** `--dialogue-share` | 漸層半透明 overlay；**不可**整塊 solid 黑底切走主圖 |
| 狗狗反應 `.dog-behavior` | 頂部 | `top: --behavior-top`（氣味列下方）；**禁止**放在狗腳邊或畫面中央 |

### CSS 契約（`:root` in `style.css`）

維持或微調時只改這些變數，勿另起 layout 模式：

- `--art-share: 70%` / `--dialogue-share: 30%`
- `--dog-max-h: calc(var(--scene-inner-h) * 0.52)` — 主圖夠大、有沉浸感
- `--dog-max-w: min(440px, 84vw)`
- `--behavior-top: 2.65rem` — 行為字幕在上方

### 互動與可讀性

- **整頁不捲動**：`body` / `#app` 鎖 `100dvh` + `overflow: hidden`
- **字幕區內捲**：僅 `.subtitle-viewport` 可 scroll；選項 `.choices` 固定可見（`flex-shrink: 0`）
- **有選項時**：`.scene.has-choices`（`game.js` `updateChoicesLayout()`）略縮字幕高度；狗僅縮 ~8%，不可像舊版縮到看不清
- **背景 vignette 要輕**：`.scene-bg::after` 只做輕暗角；底部對比由 `.scene-dialogue` 漸層負責

### 禁止回退

- ❌ 上下兩塊 flex 硬切、`.scene-dialogue` 用 `overflow-y: auto` 整區捲動
- ❌ 為塞選項而大幅縮小狗（< `--dog-max-h` 的 85%）
- ❌ 把 `.dog-behavior` 放在畫面中下段（會擋主圖）
- ❌ 把狗畫進背景 PNG（違反兩層資產）

### 背景美術風格（與 UI 一致）

- Demo 背景：**gouache／水彩感場景 PNG**，`background-size: cover`，預設 `center 28%`
- 狗 PNG：**独立叠層**，drop-shadow 加深；cold/content 用 `#app.cold` / `#app.content` filter
- 新 location：新增 `bg-*.png` + `.loc-{id}`；色溫仍走 Feelings，不用 stat 數字面板

## 視覺聖經（不可違反）

| 項目 | 規格 |
|------|------|
| 狗角色 | 見上方「角色外型聖經」與 [`reference.md`](reference.md#角色外型聖經) |
| 主人 | Demo 不露臉；局部身體須符合 reference 服裝／膚色／構圖規則 |
| 筆觸 | 數位水彩；暖色金褐、蜂蜜 ochre；**無硬黑描邊** |
| 構圖 | 單角色、全身或半身、置中；**透明背景 RGBA** |
| 禁止 | SVG 幾何拼接、多狗同框、寫實照片、廉價 Q 版 |
| 層級 | **狗永遠是独立 PNG 叠在場景上**，不画进背景 |

## §6.7 UI 介面設計規格

### 色彩系統

| 用途 | 顏色 | 說明 |
|------|------|------|
| **主背景** | 米白 `#FAF6F0` / 燕麥色 `#F5EFE0` | 溫暖底色，避免純白 |
| **文字主色** | 深棕 `#4A3728` | 取代純黑，柔和易讀 |
| **文字次色** | 暖灰 `#7A6A60` | 旁白、說明、時間標記 |
| **對話框背景** | 米白半透明 `rgba(250,246,240,0.92)` | 帶微透明感 |
| **強調 / 選項** | 蜂蜜金 `#C8912A` | 呼應狗毛色 |

### 圓角規格

- 對話框、按鈕、選項框：`border-radius: 16px+`
- 小型 tag / badge：`border-radius: 8px`
- **全面避免**銳角邊框

### 紋理

- 全局底層加入**手繪紙張紋理**（Texture PNG，低不透明度 5–10%）

### UI 禁止事項

- ❌ 高飽和度純色 UI 元素
- ❌ 純黑 `#000000` 作為文字色
- ❌ 純白 `#FFFFFF` 作為背景
- ❌ 銳角方形元素

## §6.6 狗狗動態動畫規格（GSAP / CSS Animation）

| 動畫類型 | 實作方式 | 備註 |
|----------|----------|------|
| **呼吸起伏** | CSS `@keyframes` scale(1.0–1.02) | 持續循環，2–4 秒週期 |
| **眨眼** | 覆蓋半透明遮罩 or CSS clip-path | 4–8 秒隨機間隔 |
| **耳朵抖動** | GSAP `rotation` 小角度 | 觸發於 Alert、Curious 感受 |
| **尾巴輕擺** | GSAP `rotation` 以尾根為 transform-origin | 觸發於 Content、Excited、Playful |

**原則：** 動畫為**輔助氛圍**，不搶奪視覺焦點；低幀率（≤ 30fps）、不影響故事節奏。靜態情緒圖優先，動態僅加在常駐 fallback 圖。

## §6.9 撫摸互動視覺

| 項目 | 規格 |
|------|------|
| **cursor** | 滑鼠移至狗角色 PNG 範圍內 → `cursor: pointer`（小手） |
| **觸發條件** | 文字靜止且狗感受為 Content / Sleepy / Attached |
| **視覺回饋** | 呼吸加速 or 尾巴擺動動畫（§6.6 動態動畫） |
| **禁止** | ❌ 撫摸時強制插入 UI 彈窗 ❌ 打字機播放中仍可觸發 |

## 兩層資產系統

```
resolveDogVisual：
  1. scene.dogPose 有值 → dog-{dogPose}.png（故事動作）
  2. 否則 → dog-{feeling}.png（情緒 fallback）
```

- **情緒圖（12）**：對應 `FEELINGS` 的 mood key。
- **故事動作圖（20+）**：`scenes.js` 的 `dogPose`；可為函式 `(s) => s.trust >= 50 ? 'follow-close' : 'follow-far'`。

## 工作流程

### A. 新增／替換狗 PNG

1. 以 `dog-anxious.png` 為 style reference 繪製或生成。
2. 存成 `Demo/assets/dog/dog-{id}.png`（小寫、連字號）。
3. 執行 `python Demo/tools/remove_dog_bg.py` 去背。
4. 故事專用：在 `scenes.js` 加 `dogPose`；在 `systems.js` 的 `DOG_POSES` 補 behavior 文案。
5. 新情緒：在 `FEELINGS` 加 key + 對應 PNG。

### B. 背景與場景

- **2.5D 沉浸式**：全 bleed 背景圖 + 底部字幕 overlay（見上方「Demo 沉浸式版面基準」）。
- **色溫 UI**（不用數字面板表達情緒）：
  - `--warm-bg` / 安全、Content
  - `--cold-bg` / Anxious、Hurt、雷雨
  - `#app.content` / 滿足、默契 moment
- 新 location：更新 `locations.js` + `style.css` 必要 class。

### C. 三部曲 aging（Ch2 / Ch3）

- 同一隻狗、同一水彩風格。
- 可新增 `dog-slow.png`、`dog-grey-muzzle.png` 等 **aging 變體**，不可換角色。
- 老犬篇：視野可略窄、對比降低（與 story 的感官敘事一致）。

### D. 分段視覺序列（Moment 專用）

1. 新增 `dog-{pose}.png` 序列（如 `paw-smell-1/2/3`），水彩風格對齊 `dog-anxious.png`。
2. 在 `DOG_POSES` 補 behavior；去背後存 `Demo/assets/dog/`。
3. 在 `scenes.js` 加 `visualSequence`；參考 `day4_paw_smell`。

## 美術規格輸出模板

```markdown
## 資產：[dog-{id}.png 或 location_id]

**類型：** 情緒圖 / 故事 pose / 背景
**篇章：** Ch1 / Ch2 / Ch3
**對應 scene：** day5_park

### 風格錨點
- 參考：dog-anxious.png
- 狗：依 reference §角色外型 — golden-tan、honey ochre、scruffy 混種幼犬
- 主人局部（若有）：25 歲長髮女性、暖膚、米白／灰褐簡素服；knee 類僅大腿、無腳
- 姿勢與眼神：（單一 clear moment）

### 技術
- 尺寸建議、透明 PNG、檔名
- dogPose 或 feeling key

### 場景色溫
- HUD：warm / cold / content
- 背景描述：（gradient 方向、主色）
- 版面：維持 70/30 全屏 overlay；行為字幕在頂

### 禁止項檢查
- [ ] 無硬描邊 [ ] 非 SVG 拼接 [ ] 單狗 [ ] 未嵌入背景
```

## 審查清單

- [ ] **§6.7 UI 色彩與圓角是否符合**？（米白底、深棕文字、radius 16px+）
- [ ] **§6.7 紋理**：有導入手繪紙張 Texture PNG？
- [ ] 狗是否符合 reference **角色外型**（品種感、毛色、年齡感、筆觸）？
- [ ] 含主人局部時：服裝／膚色／構圖（無臉、knee 無腳）是否符合？
- [ ] 與 `dog-anxious.png` 水彩筆觸一致？
- [ ] 檔名、目錄、`DOG_ASSET_DIR` 規範？
- [ ] 是否只需 pose 而非新情緒圖？（優先复用 12 情緒）
- [ ] 色溫是否呼應 Feelings 而非 stat 數字？
- [ ] **版面是否維持 70/30 沉浸式 overlay？** 狗夠大、行為字幕在頂、選項不需整頁捲動？
- [ ] Ch3 是否過度煽情視覺（彩虹橋套路）？

## 程式對接

| 模組 | 路徑 |
|------|------|
| 情緒／pose | `Demo/js/systems.js` |
| 場景綁定 | `Demo/js/scenes.js` |
| 載入 UI | `Demo/js/game.js` — `updateDogVisual()`、`updateChoicesLayout()` |
| 去背 | `Demo/tools/remove_dog_bg.py` |
| 樣式／版面 | `Demo/css/style.css` — `:root` 版面變數、`.scene-dialogue` overlay |

## 權責邊界

- 不寫對白、不改 Trust/Bond 邏輯（story-narrative）。
- 不調 Web Audio 參數（audio-sound）；可建議 mood → 色溫對照。

## 完成後行為（勿自動開遊戲）

狗 PNG、背景、CSS 版面、`style.css` 變數、去背等美術相關修改**完成後**：

- **不要**自動啟動遊戲或開瀏覽器，除非使用者**明確**說「開遊戲」「play.bat」「幫我測」「跑 Demo」「看一下畫面」等。
- **禁止**在未經要求時執行：`開啟遊戲.bat`、`play.bat`、`serve-demo.ps1`、`Start-Process "http://localhost:..."`、背景起本機 HTTP 伺服器只為預覽。
- 結尾改為：**簡短摘要變更** + **可選的驗證指令**（文字列出，由使用者自行執行），例如：
  ```powershell
  cd Learn_How_To_Love\Demo
  python tools\remove_dog_bg.py
  .\開啟遊戲.bat
  ```
- 使用者事後要求開啟時，再依 workspace 規則用**系統預設瀏覽器**開 `http://localhost:8765/`（勿用 IDE 內嵌預覽）。

## 參考

- 色票、版面變數、構圖規格：[`reference.md`](reference.md)
- 系列聖經：[`../../guide_line.md`](../../guide_line.md) §6.6
