# Ch1 敘事節奏修訂規格（2026-07 起）

> **主軸：** 透過人狗互動，一步步學會去愛（Ch1 = 建立信任）。  
> **玩家體感：** 每天都有記憶點；不倉促、不草草收工。  
> **權威 playable：** `Ch1_Trust/game/`（Demo 同步 Week1 核心場景）。  
> **統籌：** [`Ch1_agent/reference.md`](Ch1_agent/reference.md) §一·二 · [`Ch1_agent/SKILL.md`](Ch1_agent/SKILL.md)

---

## 一、每日必達（story-narrative 架構 · tw-narrative-voice 潤字 · game-tester 驗收）

| # | 項目 | 標準 |
|---|------|------|
| D1 | **記憶點** | 每天至少 1 個 Memory／Moment（`addMemory` + `ALBUM_ENTRIES`） |
| D2 | **互動高峰** | 至少 1 場：人對狗短對白（「」）+ 狗身體回應（text 或 choice-reaction） |
| D3 | **日終收束** | 當天最後一場：`dayClose: true` 或 `breathMs` ≥ 2600；具體畫面，非主題句 |

### 記憶點公式

```
具體物件／地點 + 人狗互動 + 一句可引用台詞 + 相簿 desc（互動句，非「這是成長」）
```

### 一日節奏模板

```
① 日開場（時間 + 小動作）
② 2～4 時段（每段有功能，不灌水）
③ 互動高峰（對話 + 選擇重量）
④ 日終場（慢、dayClose）
⑤ Memory 落地（相簿）
```

---

## 二、文案分層（tw-narrative-voice）

| 欄位 | 字型／色（UI） | 寫什麼 | 禁止 |
|------|----------------|--------|------|
| **text** | 現場 · Noto Sans · 米白 | 動作、聲音、狗身體 | 主題總結、「這叫作開始」 |
| **sub** | 內心 · 襯線斜體 · 暖金 | 一句新感受／自我審視 | 重複 text 情緒、說教、雞湯 |
| **choices** | — | 具體動作；可含「」 | 抽象標籤（「溫柔處理」） |
| **choice-reactions** | — | 狗即時身體反應 + cue | 只解釋心情 |

### 人對狗對話（每天至少考量 1 句）

| 類型 | 用途 | 範例 |
|------|------|------|
| 道歉 | 搞砸後修復 | 「對不起……我不是在吼你。」 |
| 試探 | 不確定 | 「可以……再靠近一點嗎？」 |
| 承諾 | 分離／信任 | 「會回來。真的。」 |
| 承認不會 | 認同讀者 | 「我也不知道怎麼教……」 |
| 命名／儀式 | 關係 | 低聲念名字 |
| 自我打斷 | 看見急躁 | 「不行！你怎么——」又收住 |

**台灣口語句長（2026-07）：** 安撫／承諾宜 ≥4 字；禁單字「在」「好」。詳 [`.cursor/skills/lhtl-tw-narrative-voice/reference.md`](../../.cursor/skills/lhtl-tw-narrative-voice/reference.md#人對狗對白句長台灣口語)。

### 互動課題表（場景包必填）

```
互動課題｜人學什麼｜狗學什麼｜關鍵動作｜對狗一句話
```

---

## 三、程式節奏（story-narrative 欄位 · 落地 scenes.js）

| 欄位 | 用途 | 預設／建議 |
|------|------|------------|
| `breathMs` | 留白 ms | 重場 2600–3200；引擎預設 2200 |
| `dayClose: true` | 日終場 | 引擎 3000ms |
| `memoryBeat: true` | 記憶高峰 | 引擎 2800ms |
| `textMult` | 打字放慢 | 情緒重場 1.2–1.5 |

**引擎（`game.js`）：** `SCENE_BREATH_MS=2200` · text→sub 停頓 ×1.1。

**CSS：** `.narrative-text`（現場）／ `.narrative-sub`（內心）— 見 `Ch1_Trust/game/css/style.css`。

---

## 四、禁止清單（P0 缺陷）

- text 與 sub 講同一種情緒（像自言自語）
- sub／text 主題句：「生活是一格一格」「充實感不是大事」「還不知道怎麼相信」（若 text 已寫慌）
- 字幕寫「相簿裡已有……」（Week2 起禁 Day N；Week1 仍可用 Day 但優先「第 N 天／週 X」）
- 一天連跳多短場 + 預設 1.2s 留白（已改 2.2s，重場須自訂）
- 有 choices 無 `choice-reactions` 映射

---

## 五、已落地範例（P0 參照）

| 場景 | 記憶／日終 | 要點 |
|------|------------|------|
| `day3_morning`～`night_after` | 尿墊、靠膝 | 承諾對白、清理道歉、dayClose |
| `day6_quiet` | `day6_quiet_day` | 「我回來了」、dayClose |
| `week2_calendar` | `week2_calendar` | 對螢幕說話、dayClose |
| `week3_intro` 等 | — | 刪主題總結、改互動對白 |

---

## 六、驗收（game-tester）

### 自動化

```powershell
cd Ch1_Trust/game
node tools/validate-choice-reactions.js
node tools/test-week1-flow.js
```

### 每天改完三問

1. 今天讀者會記得哪個畫面或哪句對白？
2. 今天最後一場有沒有「停下來」的感覺？
3. 像「過完一天」還是「跳過幾張卡」？

### P1 待辦

- 全章掃描空洞 sub、缺對話場景
- Week2 其餘日 `dayClose` 補齊
- 手動 playtest 節奏

---

## 七、三層體驗框架（防「一直在選、沒完沒了」）

> **日子感** ≠ 場景多；**不疲憊** = 多數時間在「看日子流過」，少數時刻才「替主人做決定」。

### 7.1 三層設計

| 層 | 目的 | 落地 |
|----|------|------|
| **時間錨點** | 讀者知道「週幾、什麼時段、這週發生過什麼」 | `DEMO_DAY_CALENDAR`、text 寫「週五早晨／週四深夜」、Week2 起禁 Day N；`smell`／`music`／`location` 換場；跨週 callback |
| **選擇節食** | 不是每格都要做決定 | 見 §7.2 A/B/C 分級；日終禁 2+ 個**純風味**選項 |
| **收束儀式** | 每天有句號、每週有章節 | `dayClose` + `breathMs` ≥ 2800；`weekN_epilogue`；`addMemory`／相簿 |

### 7.2 選項分級（場景包必填）

| 級 | 用途 | 一週上限 | 範例 |
|----|------|----------|------|
| **A｜續看** | 推進敘事，單選 | 多數場景 | 「深吸一口氣——得請假出去買」 |
| **B｜風味** | 語氣／小 stat，同線 | 每日 0–1 組 | 拖鞋輕／重、安撫用語 |
| **C｜分歧** | 換場或長期 flag | 每週 ≤2–3 | `day3_night` 修復線、雷雨硬拉、走失 |

**日終規則：**
- `dayClose: true` 的場景 → **優先 A 級單選**（「明天早晨……」）
- 若日終為 **B/C 互動高峰**（如 `week2_neighbor_after` 三選、影響 `neighborMet`）→ 可保留多選，但須是**有意義分歧**，非三個續看變體
- **禁止**：日終 2+ 個僅差 stat、同 `next` 的風味選項 → 合併為一個 A 級

### 7.3 週節奏密度

| 週 | 場景密度 | 選擇策略 |
|----|----------|----------|
| W1 | 較密（建立信任） | C 集中 Day3 夜、Day4 啃角、Day6 雷雨；其餘 A 為主 |
| W2–3 | 以週計、日終收束 | 日終合併純風味選項；Landmark 週保留 C |
| W4／週年 | 疏 + 蒙太奇 | 週年快轉，不逐日演 |

### 7.4 審計工具

```powershell
cd Ch1_Trust/game
node tools/audit-pacing.js
```

檢查：主線日終 `dayClose`、日終多選風險、主題句、空洞 sub。

---

## 八、Agent 分工

| Agent | 負責 |
|-------|------|
| **Ch1_agent** | 排產、對表、更新 reference §一·二 |
| **story-narrative** | 互動課題、A/B/C 標註、Memory 缺口、場景欄位 |
| **tw-narrative-voice** | 對白、分層、刪總結句 |
| **game-tester** | 三問、audit-pacing、validate、playtest 報告 |
