# Learn How to Love — 專用 Agent

本資料夾包含 **Ch1 統籌**與多個**職責分離**的 Cursor Agent Skill，協作開發《學會去愛》三部曲。所有 agent 皆以 [`guide_line.md`](../guide_line.md) 為最高準則；**Chapter 1 細節**以 [`Ch1_Trust/Ch1_guide_line.md`](../Ch1_Trust/Ch1_guide_line.md) 為準。

## Agent 一覽

| Agent | 資料夾 | 職責 | 深入閱讀 |
|-------|--------|------|----------|
| **Ch1 統籌** | [`Ch1_agent/`](Ch1_agent/) | 全章節奏、進度對表、調度子 agent、週產線與驗收閘門 | [`SKILL.md`](Ch1_agent/SKILL.md) · [`reference.md`](Ch1_agent/reference.md) |
| **故事架構** | [`story-narrative/`](story-narrative/) | 主線／支線、場景節點、Landmark；**敘事 DSL** 見 `narrative-engine.md` | [`SKILL.md`](story-narrative/SKILL.md) · [`reference.md`](story-narrative/reference.md) |
| **分支引擎** | [`branch-engine/`](branch-engine/) | flags、choice-reactions、A/B/C 分級 | [`SKILL.md`](branch-engine/SKILL.md) |
| **繁體敘事語氣** | [`tw-narrative-voice/`](tw-narrative-voice/) | 繁體、台灣用語、親切溫柔（**Day 1 為語調金標**） | [`SKILL.md`](tw-narrative-voice/SKILL.md) · [`reference.md`](tw-narrative-voice/reference.md) |
| **美術風格** | [`visual-art/`](visual-art/) | 水彩狗 PNG、背景、色溫 UI；**資產管線**見 `art-asset-pipeline.md` | [`SKILL.md`](visual-art/SKILL.md) |
| **聲音設計** | [`audio-sound/`](audio-sound/) | OGG BGM、幼犬樣本、SCENE_CUES；**音訊管線**見 `audio-pipeline.md` | [`SKILL.md`](audio-sound/SKILL.md) |
| **音樂作曲** | [`music-composition/`](music-composition/) | BGM brief、AI 作曲 prompt | [`SKILL.md`](music-composition/SKILL.md) |
| **Steam 部署** | [`steam-deployment/`](steam-deployment/) | Electron、Steamworks、CI 上傳、成就／雲端存檔 | [`SKILL.md`](steam-deployment/SKILL.md) · [`reference.md`](steam-deployment/reference.md) |
| **遊戲測試** | [`game-tester/`](game-tester/) | 台灣玩家視角 playtest | [`SKILL.md`](game-tester/SKILL.md) · [`reference.md`](game-tester/reference.md) |

## 任務對照（快速選 skill）

| 要做的事 | 建議 |
|----------|------|
| **Ch1 整章推進、WeekN 落地、下一步、多 agent 協調** | [`Ch1_agent`](Ch1_agent/SKILL.md)（統籌）→ 再 @ 子 skill |
| 章節大綱、新場景、分支、Memory／Landmark | [`story-narrative`](story-narrative/SKILL.md) |
| Ink／敘事 DSL、內容與程式分離 | [`story-narrative/narrative-engine.md`](story-narrative/narrative-engine.md) |
| flags、choice-reactions、分支落地 | [`branch-engine`](branch-engine/SKILL.md) |
| 改對白、選項、副標、相簿、語氣潤飾 | [`tw-narrative-voice`](tw-narrative-voice/SKILL.md) |
| 微調**已進遊戲**的場景文字 | [`Demo/game_editor.html`](../Demo/game_editor.html) |
| 換狗圖、背景、CSS | [`visual-art`](visual-art/SKILL.md) |
| BGM、狗叫、cue | [`audio-sound`](audio-sound/SKILL.md) |
| BGM 作曲 brief、AI 作曲 | [`music-composition`](music-composition/SKILL.md) |
| 美術自動匯出、圖集、壓縮管線 | [`visual-art/art-asset-pipeline.md`](visual-art/art-asset-pipeline.md) |
| Steam 建置上傳、成就、Cloud Save | [`steam-deployment`](steam-deployment/SKILL.md) |
| 測試 Week1–3、playtest、圖文審查 | [`game-tester`](game-tester/SKILL.md) |

**章節落地驗收：** [`chapter-landing-checklist.md`](chapter-landing-checklist.md)

**組合範例：**「依 [`Ch1_agent`](Ch1_agent/SKILL.md) 落地 Week4，調 story + visual + game-tester」

## 使用方式

### 在 Cursor 中呼叫

1. **@ 提及 skill 名稱**（若已同步至 `.cursor/skills/`）：
   - `@lhtl-ch1-agent` — **Ch1 統籌**（節奏、進度、調度）
   - `@lhtl-story-narrative` — 劇情與班表
   - `@lhtl-branch-engine` — 分支與 flags
   - `@lhtl-tw-narrative-voice` — 繁體語氣
   - `@lhtl-visual-art` — 美術
   - `@lhtl-audio-sound` — 音效
   - `@lhtl-music-composition` — BGM 作曲
   - `@lhtl-steam-deployment` — Steam 建置與部署
   - `@lhtl-game-tester` — 測試與報告

2. **直接指定路徑**：例——「請依照 `agent/Ch1_agent/SKILL.md` 規劃 Week4 產線」。

3. **組合使用**：Ch1_agent 拆任務 → 子 skill 執行 → game-tester 驗收。

### 建議工作流（Ch1 新週）

```
Ch1_guide_line.md + Ch1_agent/reference.md（進度）
       ↓
Ch1_agent 拆週任務與閘門
       ↓
story-narrative  → 架構 + 場景包
       ↓
tw-narrative-voice → 四層文案
       ↓
visual-art ⫽ audio-sound
       ↓
Ch1_Trust/game/js/ …
       ↓
game-tester + chapter-landing-checklist
       ↓
Ch1_agent 更新 reference.md 進度
```

僅改語氣時可跳過 visual／audio。  
**章節落地後必跑：** `test-weekN-flow.js` + `validate-choice-reactions.js`（須 OK）。

## Demo／Ch1 程式對照

| 檔案 | 用途 |
|------|------|
| [`Ch1_Trust/game/js/scenes.js`](../Ch1_Trust/game/js/scenes.js) | **playable 主線**（優先） |
| [`Demo/js/scenes.js`](../Demo/js/scenes.js) | 對照／編輯器 |
| [`Ch1_Trust/game/tools/`](../Ch1_Trust/game/tools/) | `test-weekN-flow.js`、validate 腳本 |

## 檔案結構

```
agent/
├── README.md                      ← 本文件
├── chapter-landing-checklist.md
├── Ch1_agent/                     ← Ch1 統籌
│   ├── SKILL.md
│   └── reference.md               ← 進度、節奏、調度矩陣
├── story-narrative/
│   ├── narrative-engine.md          ← Ink／DSL 與內容分離
│   └── steam-release.md
├── branch-engine/
├── tw-narrative-voice/
├── visual-art/
│   └── art-asset-pipeline.md        ← 源檔分離、CLI 匯出
├── audio-sound/
│   └── audio-pipeline.md            ← 資料夾、FMOD、AI 音樂
├── music-composition/
├── steam-deployment/                ← Steamworks、CI 部署
└── game-tester/
```

## 權責邊界

- **Ch1_agent**：不取代子 agent 專業產出；負責排程、對表、驗收閘門與進度文件。
- **story-narrative**～**game-tester**：見各 `SKILL.md`；衝突時 **`guide_line.md` > `Ch1_guide_line.md` > story-narrative > 其餘**。

詳見 [`guide_line.md` §九 Agent Skills](../guide_line.md#agent-skills-與-cursor-協作)。
