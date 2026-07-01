# Learn How to Love — 專用 Agent



本資料夾包含四個**職責分離**的 Cursor Agent Skill，協作開發《學會去愛》三部曲。所有 agent 皆以 [`guide_line.md`](../guide_line.md) 為最高準則（含 §九 Agent Skills 使用重點）。



## Agent 一覽



| Agent | 資料夾 | 職責 | 深入閱讀 |

|-------|--------|------|----------|

| **故事架構** | [`story-narrative/`](story-narrative/) | 主線／支線、場景節點、Landmark、跨作存檔、班表與小遊戲敘事鏈 | [`SKILL.md`](story-narrative/SKILL.md) · [`reference.md`](story-narrative/reference.md)（場景表、editor、flags） |

| **繁體敘事語氣** | [`tw-narrative-voice/`](tw-narrative-voice/) | 繁體、台灣用語、親切溫柔（**Day 1 為語調金標**） | [`SKILL.md`](tw-narrative-voice/SKILL.md) · [`reference.md`](tw-narrative-voice/reference.md) |

| **美術風格** | [`visual-art/`](visual-art/) | 水彩狗 PNG、背景、色溫 UI、三部曲視覺一致性 | [`SKILL.md`](visual-art/SKILL.md) |

| **聲音設計** | [`audio-sound/`](audio-sound/) | OGG BGM、幼犬 CC0 樣本、SCENE_CUES one-shot | [`SKILL.md`](audio-sound/SKILL.md) |



## 任務對照（快速選 skill）



| 要做的事 | 建議 |

|----------|------|

| 章節大綱、新場景、分支、Memory／Landmark | [`story-narrative`](story-narrative/SKILL.md) |

| 改對白、選項、副標、相簿、語氣潤飾 | [`tw-narrative-voice`](tw-narrative-voice/SKILL.md)（＋必要時 story-narrative 審班表） |

| 微調**已進遊戲**的場景文字 | [`Demo/game_editor.html`](../Demo/game_editor.html)（`Demo/啟動編輯器.bat`） |

| 換狗圖、背景、CSS | [`visual-art`](visual-art/SKILL.md) |

| BGM、狗叫、cue | [`audio-sound`](audio-sound/SKILL.md) |



**組合範例：**「依 [`story-narrative`](story-narrative/SKILL.md) + [`tw-narrative-voice`](tw-narrative-voice/SKILL.md) 改寫 `day4_vet`」



## 使用方式



### 在 Cursor 中呼叫



1. **@ 提及 skill 名稱**（若已同步至 `.cursor/skills/`）：

   - `@lhtl-story-narrative` — 撰寫或審查劇情（含班表、小遊戲 tier）

   - `@lhtl-tw-narrative-voice` — 繁體語氣與台灣用語

   - `@lhtl-visual-art` — 產出美術規格或審查 PNG／CSS

   - `@lhtl-audio-sound` — 設計 BGM profile 或狗音效



2. **直接指定路徑**：例——「請依照 `agent/story-narrative/SKILL.md` 審查 Day 4 獸醫線」。



3. **組合使用**：story → tw-narrative-voice（潤字）→ visual-art → audio-sound。



### 建議工作流



```

guide_line.md（準則）

       ↓

story-narrative  → 場景包：分支、flags、跨作標記、班表

       ↓

tw-narrative-voice → 四層文案潤飾（text / sub / choices / smell）

       ↓

visual-art       → dogPose、sceneArt、色溫

       ↓

audio-sound      → BGM、DOG_SAMPLES、SCENE_CUES

       ↓

Demo/js/scenes.js、choice-reactions.js、minigame-reactions.js、systems.js …

       ↓

（可選）game_editor.html  → 作者微調已落地文案

```



僅改語氣時可跳過 visual／audio，不必走完整三階流程。



## Demo 程式對照（story-narrative 落地）



| 檔案 | 用途 |

|------|------|

| [`Demo/js/scenes.js`](../Demo/js/scenes.js) | 場景圖、`text`／`sub`／`choices`／`minigame` |

| [`Demo/js/choice-reactions.js`](../Demo/js/choice-reactions.js) | 選項後狗狗反應（key = `場景Id::選項原文`） |

| [`Demo/js/minigame-reactions.js`](../Demo/js/minigame-reactions.js) | 小遊戲 tier 結果文案、`vetTier` 等 flags |

| [`Demo/js/systems.js`](../Demo/js/systems.js) | `DEMO_DAY_CALENDAR`、`ALBUM_ENTRIES` |

| [`Demo/game_editor.html`](../Demo/game_editor.html) | 可視化編輯；條件分支 `text` 見 [reference §條件分支](story-narrative/reference.md#條件分支-text-與編輯器) |



Ch1 七天場景與小遊戲 flags 速查：[`story-narrative/reference.md`](story-narrative/reference.md)。



## 檔案結構



```

agent/

├── README.md                 ← 本文件

├── story-narrative/

│   ├── SKILL.md              ← 場景包、審查清單、editor 分工

│   └── reference.md          ← Day 1–7 場景表、班表、小遊戲 ↔ flags

├── tw-narrative-voice/

│   ├── SKILL.md

│   └── reference.md

├── visual-art/

│   ├── SKILL.md

│   └── reference.md

└── audio-sound/

    ├── SKILL.md

    └── reference.md

```



## 權責邊界（避免越界）



- **story-narrative**：不決定 PNG 色票或 Web Audio 參數；改完劇情後**不自動啟動 Demo**（除非使用者明確要求）。

- **tw-narrative-voice**：不新增主線分支、不改 Trust／Bond；專注字詞與語氣。

- **visual-art**：不寫對白或改 Trust／Bond 數值。

- **audio-sound**：不新增主線分支；僅依 story 與 visual 的 mood／location 配樂。



衝突時：**`guide_line.md` > `story-narrative` > 其餘 skill**。



檔案分開維護、使用時按需組合即可；詳見 [`guide_line.md` §九 Agent Skills](../guide_line.md#agent-skills-與-cursor-協作)。


