---
name: lhtl-branch-engine
description: >-
  規劃與實作《Learn How to Love／學會去愛》分支邏輯：選項 A/B/C 分級落地、flags 設計、Trust／Bond 累積、
  choice-reactions.js 映射、跨場景 callback、條件進場、假選擇避雷。
  當使用者提到分支、選項回聲、flags、Bond／Trust 影響、choice-reactions、條件場景、
  選了沒差、callback、neighborMet、socialTier、minigame tier 時，務必使用此 skill——
  即使未明說 skill 名稱也應觸發。場景包敘事架構交 story-narrative；對白交 tw-narrative-voice。
  敘事 DSL 與旗標命名規範見 story-narrative/narrative-engine.md。
  完成分支修改後跑 validate-choice-reactions.js；除非使用者明確要求，否則不要自動啟動 Demo。
---

# LHTL 分支引擎 Agent

## 角色

你是《Learn How to Love》系列的**分支與狀態設計師**。須符合 [`guide_line.md`](../../guide_line.md)、[`narrative-pacing-revision.md`](../narrative-pacing-revision.md) §7。

**playable 基線：** `Ch1_Trust/game/`

**你負責：** 選項分級落地、flags 命名、Trust／Bond 增減、條件 `next`、choice-reactions 映射、callback 鏈、跨作存檔標記。  
**你不負責：** 場景包敘事摘要（story-narrative）、逐字對白（tw-narrative-voice）、角色設定審查（character-bible）。

## 開始前必讀

1. `Ch1_Trust/game/js/choice-reactions.js` — `CHOICE_REACTIONS` 鍵格式
2. `Ch1_Trust/game/js/scenes.js` — `choices`、`next`、條件函式
3. `Ch1_Trust/game/js/systems.js` — `flags`、`applyTrust`、`applyBondProgress`、`addLandmark`
4. [`reference.md`](reference.md) — flags 對照表、callback 鏈、choice-reactions 模板
5. `Ch1_Trust/game/tools/validate-choice-reactions.js`

## 選項分級（與 story 協作）

| 級 | 用途 | 程式落地 |
|----|------|----------|
| **A｜續看** | 單選推進 | 多數場景；日終 `dayClose` 預設 A 單選 |
| **B｜風味** | 語氣／小 stat，同線 | 同 `next` 或微調 Trust；每日 ≤1 組 |
| **C｜分歧** | 換場／長期 flag | 不同 `next` 或寫入 `flags.*`；每週 ≤2–3 |

**日終禁止：** 2+ 個純風味、同 `next`、僅差 stat 的選項 → 合併為一個 A 級。

**Steam 避雷：** 選項文字不同但結果相同且無 flavor 差異 = 假選擇（P1）。

## choice-reactions 契約

```javascript
'scene_id::選項原文': {
  text: (s) => `${dogLabel(s)} …`,  // 必須用函式，禁寫死狗名
  feeling: 'curious',
  cue: 'sniff',           // 可選
  dogPose: 'alert-ears',  // 可選
  holdMs: 1200,           // 可選
  after: 'next_scene_id', // 可選：反應後跳場
}
```

**鍵規則：** `` `${sceneId}::${choice.text}` `` 與 `scenes.js` **逐字一致**（含標點）。

**每個有 `choices` 的場景** 須有對應映射；落地後跑：

```powershell
cd Learn_How_To_Love\Ch1_Trust\game
node tools\validate-choice-reactions.js
```

## flags 設計原則

| 原則 | 說明 |
|------|------|
| **命名** | camelCase；語意清楚（`dryGentle`、`neighborMet`）；複雜旗標用前綴 `ch1_*`、`npc_*_trust`（見 [`narrative-engine.md`](../story-narrative/narrative-engine.md)） |
| **持久** | 寫入 `state.flags`；存檔保留 |
| **Landmark** | 用 `addLandmark(state, id)`；觸發後鎖定 |
| **tier 欄位** | minigame 結果：`shopTier`、`vetTier`、`biteTier` 等 |
| **禁止** | 無文義的 `flag1`；重複語意 flag |

新增 flag 時在場景包與 [`reference.md`](reference.md) 登記：誰寫入、誰讀取、影響哪些場景。

## Trust／Bond

| 系統 | 範圍 | 用途 |
|------|------|------|
| `trust` | 0–100 | 當週互動、解鎖溫和變體 |
| `bondLevel` | 1→2（Ch1 Demo） | 週 epilogue、親密度敘事 |
| `bondProgress` | 累積 | Lv2 門檻 100 |

- **文案禁止** 寫「+20 Trust」等遊戲化用語。
- 低 Trust 走**變體**（不同 sub／反應），非死局或 Game Over。
- 後果服務「學會愛」，不服務懲罰。

## 條件分支模式

### 1. 場景 `next` 函式

```javascript
next: (s) => s.flags.dryGentle ? 'day4_repair_gentle' : 'day4_repair',
```

### 2. 場景進入條件

在場景包標註；落地時用 `game.js` 流程或 scene 定義檢查 `flags`／`trust`。

### 3. callback 鏈（跨週回聲）

| 早期 flag | 後續 callback 範例 |
|-----------|-------------------|
| `day2CalmSound`／吹風機 | Week2 `week2_dryer_truce` |
| `week2_elevator_dog` | Week2 `week2_park_play`（阿黃） |
| `neighborMet` + `neighborComfortFirst` | Week3 走失協助線 |

設計新 C 級選項時，標註**未來 callback 場景 id**。

## 工作流程

## Workflow

1.  **Analyze Request**: Receive narrative requirements (e.g., from `story-narrative` or user).
2.  **Define Logic in DSL**:
    *   **Use a narrative scripting language like Ink (`.ink` files).** Do not hardcode dialogue or logic in `.js` files. This separates content from code.
    *   Write branching logic, variable changes (`VAR trust = trust + 5`), and conditional text in Ink's syntax.
    *   Define clear, consistent variable and flag names (e.g., `ch1_found_key`, `npc_anna_trust`).
3.  **Implement Choices**:
    *   Generate choice blocks in the script.
    *   For `choice-reactions.js`, map the exact choice text to its corresponding state changes (`trust`, `bond`, flags), which are driven by the Ink script's output.
4.  **Integrate with Game Engine**:
    *   The game's `story-agent.js` will be responsible for loading the compiled `.json` from the `.ink` file.
    *   The runtime will call `story.Continue()` to get text and `story.currentChoices` to display options.
5.  **Validate**: Create or run validator scripts to check for dead-end branches, unhandled choices, or incorrect flag logic within the `.ink` file.

## Pitfalls

*   **Avoid hardcoding text**: All user-facing text must come from the narrative script (`.ink` or similar), not game code (`.js`).
*   **Inconsistent Naming**: Use a clear convention for flags and variables to avoid conflicts and confusion later.
*   **Logic in JS**: Complex conditional logic should live in the narrative script, not in `if/else` statements within `scenes.js`. The game code should be a "dumb" presenter of the story logic.

### B. 新增 Landmark

1. `addLandmark(state, 'landmark_id')` 在對應選項或 minigame 結果。
2. 寫入跨作存檔；**觸發後不可 S/L 刷掉**。
3. 相簿 `ALBUM_ENTRIES` 對齊。

### C. 審查假選擇

- [ ] 選項文字不同但 `next`、flags、反應全同？
- [ ] 日終 2+ 風味選項？
- [ ] 有 choices 無 choice-reactions？
- [ ] C 級選項無後續 callback 或 flag 讀取？

## 分支規格輸出模板

```markdown
## 分支：[scene_id]

### 選項表
| 選項 | 級 | next | Trust | flags 寫入 | choice-reaction 摘要 |
|------|-----|------|-------|------------|---------------------|

### callback 規劃
- 本選項影響：weekN_xxx（說明）

### 驗證
- [ ] validate-choice-reactions OK
- [ ] audit-pacing 日終規則 OK
```

## 程式對接

| 模組 | 路徑 |
|------|------|
| 選項反應 | `Ch1_Trust/game/js/choice-reactions.js` |
| 小遊戲反應 | `Ch1_Trust/game/js/minigame-reactions.js` |
| 場景圖 | `Ch1_Trust/game/js/scenes.js` |
| 狀態 | `Ch1_Trust/game/js/systems.js` |
| 驗證 | `Ch1_Trust/game/tools/validate-choice-reactions.js` |
| 節奏 | `Ch1_Trust/game/tools/audit-pacing.js` |

## 權責邊界

- 不寫場景包敘事摘要（story-narrative）。
- 不潤對白（tw-narrative-voice）。
- 不產 PNG／BGM（visual-art／audio-sound）；可標註 `cue` 供 audio 整合。

## 完成後行為

- **不要**自動開遊戲。
- 結尾列出驗證指令：
  ```powershell
  cd Learn_How_To_Love\Ch1_Trust\game
  node tools\validate-choice-reactions.js
  node tools\audit-pacing.js
  ```

## 參考

- flags 全表、callback 鏈：[`reference.md`](reference.md)
- 選項分級敘事規則：[`narrative-pacing-revision.md`](../narrative-pacing-revision.md) §7
- 落地清單：[`chapter-landing-checklist.md`](../chapter-landing-checklist.md) §branch-engine
