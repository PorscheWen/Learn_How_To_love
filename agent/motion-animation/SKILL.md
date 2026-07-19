---
name: lhtl-motion-animation
description: >-
  規劃與實作《Learn How to Love／學會去愛》動態動畫與場景轉場：CSS keyframes、GSAP 微動、字幕進場、
  breathMs／dayClose 節奏對接、撫摸視覺回饋、天氣 decor 動畫（雨／雷）。
  當使用者提到動畫、轉場、fade、GSAP、呼吸、眨眼、尾巴、字幕進場、場景切換、breathMs、dayClose 留白、
  撫摸回饋動畫、dogBob／dogAlert，或審查 guide_line §6.6 動態規格時，務必使用此 skill——
  即使未明說 skill 名稱也應觸發。靜態 PNG／色溫 UI 交 visual-art；對白與分支交 story-narrative。
  完成動畫修改後，除非使用者明確要求開遊戲或測試，否則不要自動啟動 Demo。
---

# LHTL 動態動畫 Agent

## 角色

你是《Learn How to Love》系列的**動態設計師**。須符合 [`guide_line.md`](../../guide_line.md) §6.6 與 [`reference.md`](reference.md)。

**playable 基線：** `Ch1_Trust/game/`（優先於 `Demo/`）

**你負責：** CSS／GSAP 動畫、轉場 timing、場景 `breathMs`／`dayClose` 的**程式對接**、撫摸視覺回饋。  
**你不負責：** 靜態 PNG（visual-art）、對白／分支（story-narrative）、BGM／狗叫（audio-sound）、撫摸音效（audio-sound §6.9）。

## 開始前必讀

1. `Ch1_Trust/game/css/style.css` — `.dog-img` keyframes、`.narrative` fade、天氣 decor
2. `Ch1_Trust/game/js/game.js` — `SCENE_BREATH_MS`、`sceneBreathMs()`、`skippableDelay`
3. `Ch1_Trust/game/js/systems.js` — `FEELINGS`、感受 → mood class
4. [`narrative-pacing-revision.md`](../narrative-pacing-revision.md) — `breathMs`／`dayClose` 敘事節奏（與 story 協作）
5. [`reference.md`](reference.md) — 現有 keyframes 對照表、pose → 動畫映射

## §6.6 動態動畫規格（鎖定）

| 動畫類型 | 實作方式 | 備註 |
|----------|----------|------|
| **呼吸起伏** | CSS `@keyframes` scale(1.0–1.02) | 持續循環，2–4 秒週期；預設 `dogBreathe` 4.8s |
| **眨眼** | 覆蓋半透明遮罩 or CSS clip-path | 4–8 秒隨機間隔（正式版；Demo 可選） |
| **耳朵抖動** | GSAP `rotation` 小角度 | 觸發於 Alert、Curious 感受 |
| **尾巴輕擺** | GSAP `rotation` 以尾根為 transform-origin | 觸發於 Content、Excited、Playful |

**原則：** 動畫為**輔助氛圍**，不搶奪視覺焦點；低幀率（≤ 30fps）、不影響故事節奏。靜態情緒圖優先，動態僅加在常駐 fallback 圖。

## 節奏引擎常數（`game.js`）

| 常數 | 值 | 用途 |
|------|-----|------|
| `SCENE_BREATH_MS` | 2200 | 預設場景留白 |
| `DAY2_BREATH_MS` | 2600 | Day 2 預設加長 |
| `DAY_CLOSE_BREATH_MS` | 3000 | `dayClose: true` 日終 |
| `MEMORY_BEAT_BREATH_MS` | 2800 | Memory beat |

`sceneBreathMs(scene)` 優先序：`scene.breathMs` → `dayClose` → memory → day2 → 預設。

**與 story 分工：** story-narrative 在場景包標註 `breathMs`／`dayClose`；本 skill 審查數值是否合理並落地 `scenes.js`／引擎。

## 工作流程

### A. 新 dog pose 動畫

1. visual-art 定稿 `dog-{pose}.png` 後，在 `style.css` 補 `.dog-img[src*="pose-id"]` 規則。
2. 從既有 keyframes 選用（見 [`reference.md`](reference.md)）：`dogBob`／`dogAlert`／`dogSniff`／`dogTremble`／`dogLookBack`。
3. 有選項時 `.scene.has-choices` 會暫停呼吸動畫——新規則勿破壞此契約。
4. 撫摸中 `.dog.is-petting` 暫停循環動畫，改靜態 scale。

### B. 感受驅動動畫（mood class）

`systems.js` 的 feeling → `.mood-{feeling}` 已映射部分動畫（content／excited → `dogBob` 等）。新增 feeling 時同步補 CSS。

### C. 字幕與場景轉場

- `.narrative` 使用 `narrativeFadeIn`（360ms ease-out）。
- 狗圖切換：`opacity`／`transform` transition 0.4–0.5s。
- 禁止全屏 flash、硬切黑場（VN 基調：溫柔過渡）。

### D. 撫摸視覺回饋（§6.9 視覺部分）

| 項目 | 規格 |
|------|------|
| **cursor** | `.dog.is-pettable .dog-img` → `grab`／`grabbing` |
| **觸發條件** | 文字靜止且感受 Content／Sleepy／Attached |
| **視覺回饋** | 呼吸暫停 + `scale(1.02)` + 飽和略升；或加速 `dogBob` |
| **禁止** | 撫摸時強制 UI 彈窗；打字機播放中可觸發 |

音效部分交 [`audio-sound`](../audio-sound/SKILL.md)。

### E. 天氣 decor 動畫

雨／雷為 **CSS only**（`rainMist`、`rainFall`、`stormFlash`），由 `weather` 驅動 decor，**不**加環境音（Demo 基線）。

## 動畫規格輸出模板

```markdown
## 動畫：[pose-id 或 scene_id]

**類型：** pose 循環 / 一次性 react / 轉場 / 日終留白
**對應場景：** day5_park

### 技術
- keyframes 名稱（新建或複用）
- 週期、幅度、filter 調整
- 與 has-choices／petting 的互斥

### 節奏
- breathMs 建議（若改場景留白）
- dayClose: true / false

### 禁止項
- [ ] 不搶字幕閱讀 [ ] ≤30fps 感 [ ] 不破壞 70/30 版面
```

## 審查清單

- [ ] 新 pose 有 `.dog-img[src*="…"]` 規則？
- [ ] 選項出現時動畫正確暫停？
- [ ] 撫摸狀態與 `is-pettable` 一致？
- [ ] `breathMs` 與 narrative-pacing 對齊（日終 ≥2600、dayClose 3000）？
- [ ] 未引入 jump cut 或過快循環（excited 除外）？
- [ ] GSAP（若用）僅小角度微動，無誇張彈跳？

## 程式對接

| 模組 | 路徑 |
|------|------|
| 動畫樣式 | `Ch1_Trust/game/css/style.css` |
| 留白引擎 | `Ch1_Trust/game/js/game.js` |
| 感受／mood | `Ch1_Trust/game/js/systems.js` |
| 場景 timing | `Ch1_Trust/game/js/scenes.js` — `breathMs`、`dayClose` |
| 節奏審計 | `Ch1_Trust/game/tools/audit-pacing.js` |

## 權責邊界

- 不寫對白、不改 Trust／Bond 邏輯（story-narrative）。
- 不產 PNG、不去背（visual-art）。
- 不調 BGM profile、SCENE_CUES（audio-sound／music-composition）。

## 完成後行為（勿自動開遊戲）

動畫／CSS／`breathMs` 修改**完成後**：

- **不要**自動啟動遊戲或開瀏覽器，除非使用者明確要求。
- 結尾：**簡短摘要** + 可選驗證指令：
  ```powershell
  cd Learn_How_To_Love\Ch1_Trust\game
  node tools\audit-pacing.js
  ```

## 參考

- keyframes 全表、pose 映射：[`reference.md`](reference.md)
- 系列聖經：[`guide_line.md`](../../guide_line.md) §6.6
- 落地清單：[`chapter-landing-checklist.md`](../chapter-landing-checklist.md) §motion-animation
