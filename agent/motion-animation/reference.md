# LHTL 動畫參考表

> playable：`Ch1_Trust/game/css/style.css` · 節奏：`game.js` · 對照 `guide_line.md` §6.6

## 引擎留白常數

| 常數 | ms | 觸發 |
|------|-----|------|
| `SCENE_BREATH_MS` | 2200 | 預設 |
| `DAY2_BREATH_MS` | 2600 | `scene.day === 2` |
| `DAY_CLOSE_BREATH_MS` | 3000 | `dayClose: true` |
| `MEMORY_BEAT_BREATH_MS` | 2800 | memory beat |

場景包建議：重場 2600–3200；日終 `dayClose`；一般場可省略（用預設 2200）。

## 既有 keyframes

| 名稱 | 用途 | 週期／備註 |
|------|------|------------|
| `dogBreathe` | 預設呼吸 | 4.8s；scale 1→1.012 |
| `dogBob` | 開心／輕跳 | 0.55s–2.4s 依 mood |
| `dogAlert` | 警戒豎耳感 | 1.2s |
| `dogSniff` | 嗅聞 | 1.8–2.2s |
| `dogTremble` | 害怕／雷雨 | 0.35–0.5s |
| `dogLookBack` | 回頭望 | 2s；walk pose |
| `dogReactPulse` | 選項反應一次性 | 0.55s；`.dog.is-react` |
| `narrativeFadeIn` | 字幕進場 | 360ms |
| `rainMist` / `rainFall` / `stormFlash` | 天氣 decor | CSS only |

## Feeling → mood 動畫（`style.css`）

| mood class | 動畫 |
|------------|------|
| `.mood-content` / `.mood-attached` / `.mood-sleepy` | `dogBob` 2.4s |
| `.mood-excited` / `.mood-playful` | `dogBob` 0.55s |
| `.mood-alert` | `dogAlert` |
| `.mood-hungry` | `dogSniff` |
| `.mood-hurt` | 僅 filter 降飽和 |

## Pose → 動畫映射（Ch1 現行）

| src 包含 | 動畫 |
|----------|------|
| `walk` | `dogLookBack` |
| `thunder` | `dogTremble` |
| `toy`, `doorway` | `dogBob` 0.7s |
| `park` | `dogSniff` |
| `alert-ears`, `window` | `dogAlert` |
| `leash` | `dogTremble` 0.45s |
| `sock`, `park-play` | `dogBob` 0.65s |
| `phone-pose` | `dogBob` 2s |
| `bite-teach` | `dogBob` 0.85s |
| `follow-close` | `dogBob` 1.8s |
| `box` | `dogTremble` 0.5s + 降亮度 |

新 pose 優先**複用**上表，避免每 pose 獨創 keyframes。

## 互斥狀態

| 狀態 | 行為 |
|------|------|
| `.scene.has-choices` | 暫停 `dogBreathe`；狗略縮 ~8% |
| `.dog.is-petting` | `animation: none`；靜態 scale 1.02 |
| `.dog.is-react` | 一次性 `dogReactPulse` |

## GSAP（正式版／待實作）

| 觸發 | 動作 |
|------|------|
| Alert、Curious | 耳朵小角度 rotation |
| Content、Excited、Playful | 尾巴輕擺（transform-origin 尾根） |

Demo 現以 CSS 為主；引入 GSAP 時須保持微幅、不搶戲。
