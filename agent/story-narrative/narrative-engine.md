# 敘事引擎參考（narrative-engine）

> GitHub 生態：`inkle/ink`、`Twine`、`Yarn Spinner`、`renpy`、Unity/Godot dialogue system  
> **LHTL 現行：** `scenes.js` + `choice-reactions.js` + `flags`（見 branch-engine）。本文件為**業界 DSL 最佳實踐**與正式版遷移參考。

---

## 1. 敘事 DSL 選擇

| 工具 | 適用 | 特點 |
|------|------|------|
| **Ink** (`inkle/ink`) | 複雜分支、狀態、非線性 | 《80 Days》等業界標準；可整合 Unity、Godot、Web |
| **Twine** | 快速原型 | 視覺化；產出 HTML |
| **Yarn Spinner** | Unity 專案 | 語法親民、劇本協作友善 |
| **Ren'Py** | 傳統 VN | Python DSL；適合全 VN 路線 |

**LHTL 建議：** 維持現行 `scenes.js` 至 Ch1 穩定；**三部曲正式版或協作擴章**時評估 **Ink**——與 Web/Electron 棧相容，利於內容與程式分離。

---

## 2. 工作流程（Ink 為例）

| 階段 | 做法 |
|------|------|
| **撰寫** | Inky 或 VS Code Ink 擴充 → `.ink` 檔 |
| **版本控制** | `.ink` 與程式同 repo；diff 可追蹤對白變更 |
| **整合** | `inkjs` runtime；編譯 `.ink` → JSON |
| **執行** | `story.Continue()` 取下一句；`story.currentChoices` 取選項；`story.ChooseChoiceIndex(i)` 選擇；`story.variablesState["var"]` 讀寫變數 |

### 與 LHTL 對照

| Ink 概念 | LHTL 現行 |
|----------|-----------|
| `variablesState` | `state.flags`、`trust`、`bond` |
| `currentChoices` | `scenes[].choices` |
| knot／stitch | `scene_id` 節點圖 |
| 條件分歧 | `next: (s) => ...`、`flags.*` |

---

## 3. 內容與程式分離

- **禁止**在遊戲引擎端寫死對白；所有玩家可見文字應來自腳本層（現行：`scenes.js`／未來：`.ink` 或 `zh-TW.json`）。
- 微調已進遊戲的單場文字 → `game_editor.html`；新增整場景 → 場景包（story-narrative）再落地。

---

## 4. 變數與旗標命名

一致規範，避免後期難維護（branch-engine 落地）：

| 模式 | 範例 |
|------|------|
| 章節 + 事件 | `ch1_found_key`、`ch1_thunderPath` |
| NPC + 關係 | `npc_anna_trust`、`neighborMet` |
| minigame tier | `shopTier`、`vetTier`、`biteTier` |

**禁止：** `flag1`、`temp`、`x` 等無語意命名。

---

## 5. Pitfalls

- 複雜分支全堆在 `game.js` → 應上移到 DSL 或 `scenes.js` 資料驅動。
- 選項文字不同、結果相同且無 flavor → 假選擇（game-tester P1）。
- Ink 遷移時須保留 `choice-reactions` 的狗狗反應契約（`場景Id::選項原文`）。

---

## 6. 相關 Agent

| 任務 | Agent |
|------|-------|
| 場景包、班表、Landmark | story-narrative |
| flags、choice-reactions 實作 | branch-engine |
| 繁體對白潤飾 | tw-narrative-voice |
