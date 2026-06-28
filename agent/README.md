# Learn How to Love — 專用 Agent

本資料夾包含三個**職責分離**的 Cursor Agent Skill，協作開發《學會去愛》三部曲。所有 agent 皆以 [`guide_line.md`](../guide_line.md) 為最高準則。

## Agent 一覽

| Agent | 資料夾 | 職責 |
|-------|--------|------|
| **故事架構** | [`story-narrative/`](story-narrative/) | 主線／支線、章節節點、Landmark 事件、跨作存檔敘事 |
| **美術風格** | [`visual-art/`](visual-art/) | 水彩狗角色、背景場景、色溫 UI、三部曲視覺一致性 |
| **聲音設計** | [`audio-sound/`](audio-sound/) | OGG BGM、幼犬 CC0 樣本、SCENE_CUES one-shot（無 weather SFX） |

## 使用方式

### 在 Cursor 中呼叫

1. **@ 提及 skill 名稱**（若已同步至 `.cursor/skills/`）：
   - `@lhtl-story-narrative` — 撰寫或審查劇情
   - `@lhtl-visual-art` — 產出美術規格或審查 PNG／CSS
   - `@lhtl-audio-sound` — 設計 BGM profile 或狗音效

2. **直接指定路徑**：在對話中說「請依照 `Learn_How_To_Love/agent/story-narrative/SKILL.md` 撰寫 Day 8 場景大綱」。

3. **組合使用**：先 story → 再 visual-art → 再 audio-sound，依序產出場景包。

### 建議工作流

```
guide_line.md（準則）
       ↓
story-narrative → 場景腳本大綱 + 分支 + 跨作標記
       ↓
visual-art      → dogPose / 背景 / 色溫規格
       ↓
audio-sound     → BGM profile + DOG_SAMPLES + SCENE_CUES（維持 Demo 音效基線）
       ↓
Demo/js/scenes.js、audio-tracks.js、audio.js、dog-samples.js、dog-audio.js
```

## 檔案結構

```
agent/
├── README.md                 ← 本文件
├── story-narrative/
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

- **story-narrative** 不決定 PNG 色票或 Web Audio 參數；**修改完劇情後不自動啟動 Demo**（除非使用者明確要求）。
- **visual-art** 不寫對白或改 Trust／Bond 數值。
- **audio-sound** 不新增主線分支；僅依 story 與 visual 的 mood／location 配樂。

三者衝突時，以 `guide_line.md` 為準，其次 story-narrative。
