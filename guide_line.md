# Learn How to Love — 開發指南（Guide Line）

> **本文件範圍：** 系列大綱、架構流程、必要決策。  
> **不含：** Demo 逐日內容、場景表、資產清單、程式細節——見各章指南與 `agent/`。  
> **鎖定設定：** [`MEMORY.md`](MEMORY.md)（世界觀／角色）· [`.cursorrules`](.cursorrules)（程式規範）  
> **品質防線：** [`agent/`](agent/) Skills — **Cursor 與 Hermes 產出前必讀對應 skill**，確保結果符合預期。

---

## 一、系列定位

| 項目 | 內容 |
|------|------|
| **英文主標** | Learn How to Love |
| **中文主標** | 學會去愛 |
| **類型** | 情感敘事三部曲（非純寵物模擬器） |
| **一句話** | 家庭用十幾年學會愛的故事——操作時間、默契與無法 S/L 刷掉的選擇，非刷數值通關 |
| **Slogan** | 愛，是一起學會的事。 |

### 三部曲

| 篇章 | 副標 | 生命階段 | 核心 | 基調 |
|------|------|----------|------|------|
| Ch1 | First Steps | 幼犬 | **信任** | 暖、有笑 |
| Ch2 | Still Here | 中年 | **日常** | 靜、節奏 |
| Ch3 | Goodbye | 老犬 | **告別** | 克制、尊嚴 |

**視角：** 全程狗的感官（嗅覺、聽覺、身體），非 stat 面板語言。

### 市場差異（摘要）

三作可獨立可玩的完整人生史 · 跨作記憶個人化告別 · 中年日常深度 · 第三部才寫死亡 · 不道德綁架安樂抉擇。

---

## 二、核心設計原則（不可動搖）

1. **後果服務「學會愛」** — 疏忽改變關係與分支，非一刀 Game Over。  
2. **無 permadeath** — 第一、二部不會養死；死亡與告別**只屬 Ch3**。  
3. **Landmark 鎖定** — 重大選擇寫入跨作存檔，不可 S/L 刷完美。  
4. **眼淚來自默契與告別** — 非廉價彩虹橋、非三作皆催淚。  
5. **壞結局可重玩該章** — 不清零全系列進度。  
6. **檔案不從 backup 來** — `Learn_How_To_Love` 所需程式、場景、圖、音等，**一律走正式產線**（`Ch1_Trust/game/`、`art-pose.ps1`、Nous Portal、下載腳本）；**禁止**從工作區 `backup/`（含 `game_version1/`、`version1/`、`Demo/`）或 `Ch1_Trust/backup/` 複製補檔。備份僅供使用者手動封存；Agent 僅在使用者**明確**說「從 backup 還原」時才可複製指定檔案。

詳細角色、年齡、班表、文案分層 → [`MEMORY.md`](MEMORY.md)。

---

## 三、故事架構（大綱）

### Chapter 1 — 信任

意外相遇 → 教與陪、分離焦慮與修復 → 第一次默契。主人：25 歲長髮女性上班族，第一次養寵。

### Chapter 2 — 日常

生命快轉（結婚、孩子、父母老去）；狗從被教變成「教這個家怎麼活」；被忽略與再被看見。

### Chapter 3 — 告別

老犬照護；氣味閃回前兩作；安樂／治療／在家渡過三線完整；克制送別。

章節場景數、時長、逐日大綱 → 各 `Ch?_*/Ch?_guide_line.md`。

---

## 四、玩法與系統（概要）

| 階段 | 重心 | 機制 |
|------|------|------|
| 幼犬 | 教、建立規則 | Trust、如廁／社會化 |
| 中年 | 節奏、家庭事件 | Bond 默契、忽略／修復線 |
| 老犬 | 照護、取捨 | 氣味記憶閃回、敘事密度高 |

**長期指標：** Trust · Bond（五階）· Comfort  

**特別事件：** `章節節點 + Bond 門檻 + 感受 + flags` → Moment / Memory / **Landmark**（鎖定、跨作）

**跨作存檔欄位：** 狗名、常去地點、Landmark 清單、flags、Bond／Trust 關鍵選擇等。

系統數值表、Feelings 全表、UI／音效／美術細規 → `agent/` 各 skill · `guide_line` 舊版細節已遷至該處。

---

## 五、技術方向（概要）

| 項目 | 方向 |
|------|------|
| **現行引擎** | Web（HTML/JS/CSS）→ 正式版 **Electron** 封裝 |
| **視覺** | 2.5D 水彩背景 + 透明 PNG 狗角色（兩層疊加） |
| **上架** | Steam；成就、Cloud Save、zh-TW／en 字串抽離 |
| **單章規模** | 主線 3–5h；場景 ~90–110／章 |

技術部署細節 → [`agent/steam-deployment/`](agent/steam-deployment/SKILL.md) · 敘事門檻 → [`agent/story-narrative/steam-release.md`](agent/story-narrative/steam-release.md)

---

## 六、製作工作流（四層分工）

本專案採 **Cursor（前端／引擎）+ Hermes（後台內容工廠）** 雙軌；設定鎖定由 `MEMORY.md` 與 `.cursorrules` 共用。

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Cursor Pro — 前端代碼與 UI 總監                              │
│    遊戲主邏輯、UI 渲染、存檔、即時 Debug、多檔重構               │
└─────────────────────────────────────────────────────────────┘
                              ↑ 內容備齊、驗證通過後落地
┌─────────────────────────────────────────────────────────────┐
│ 2. Hermes + Nous Portal — 後台內容與文本                       │
│    模型：deepseek-v4-flash（經 Nous Portal）                    │
│    異步大量產劇本、分支 JSON；吞入 MEMORY.md；跑 validate 驗邏輯 │
└─────────────────────────────────────────────────────────────┘
         │                                    │
         ▼                                    ▼
┌──────────────────────┐          ┌──────────────────────────┐
│ 3. 場景插圖            │          │ 4. 旁白配音與環境音          │
│ Portal Plus：FLUX 2 Pro │          │ Portal Plus：OpenAI TTS   │
│ 背景自動落盤            │          │ 對白／旁白 → .mp3 落盤       │
│ MJ --cref：主角立繪差分  │          │ 扣 Portal 內建點數           │
└──────────────────────┘          └──────────────────────────┘
```

### 1. 前端代碼與 UI 總監 — **Cursor Pro**

| 項目 | 說明 |
|------|------|
| **職責** | Unity／Godot／**Web** 遊戲主邏輯；Text 顯示、按鈕監聽；存檔／讀檔；即時 Debug |
| **工具** | Agent 模式、Composer、多檔跨檔重構 |
| **本專案落地** | `Ch1_Trust/game/js/`、`css/`；審稿後整合 Hermes 產出 |
| **規範** | [`.cursorrules`](.cursorrules) · `@lhtl-*` skills |

**原則：** Hermes 產草稿與素材；**Cursor 負責引擎整合、UI 手感、架構正確性。**

### 2. 後台內容與文本 — **Hermes Agent + Nous Portal（deepseek-v4-flash）**

| 項目 | 說明 |
|------|------|
| **職責** | 24h 背景異步大量產出劇情、分支 JSON；自動檢查邏輯漏洞 |
| **模型** | `deepseek-v4-flash`（透過 [Nous Portal](https://portal.nousresearch.com)） |
| **上下文** | 一次讀入 [`MEMORY.md`](MEMORY.md) + `agent/` 敘事規範 |
| **輸出** | Structured JSON／場景包；須通過 `Ch1_Trust/game/tools/validate-*.js` |
| **啟動** | `hermes setup --portal` · `hermes model deepseek-v4-flash` |

**原則：** 量大在 Hermes；結構化輸出後仍須 **validate 腳本 + Cursor 審稿**，不假設 100% 免修。**

### 3. 環境場景插圖 — **Nous Portal Plus × Midjourney 混合**

| 類型 | 管道 | 說明 |
|------|------|------|
| **背景／場景** | Portal Tool Gateway · **FLUX 2 Pro** | Hermes 生劇本時背景並行生圖 → `assets/bg/` |
| **主角立繪／表情差分** | **Midjourney** `--cref` | 角色一致性精雕；FLUX 角色鎖定較弱 |
| **落地** | Cursor | `locations.js`、CSS `.loc-*`、動態切換 pose |

美術規範 → [`agent/visual-art/`](agent/visual-art/SKILL.md)

### 4. 配音 — **Nous Portal Plus（OpenAI TTS）**

| 項目 | 說明 |
|------|------|
| **職責** | 狗狗聲音 `.mp3` → 專案音訊目錄 |
| **落地** | Cursor 綁定場景 cue · `agent/audio-sound` |

### 端到端流程

```
MEMORY.md + agent/*/SKILL.md（品質防線）
        ↓
Hermes（deepseek-v4-flash）→ 劇本 JSON + FLUX 背景 + TTS
        ↓
validate-*.js（邏輯／choice-reactions／班表）
        ↓
Cursor Pro（@lhtl-* skills）→ 落地 scenes.js、UI、存檔、整合音圖
        ↓
@lhtl-game-tester playtest → 章節指南更新
```

**cron／排程：** `tools/hermes/` 可定時跑測試；完整 pipeline 見 `tools/hermes/hermes.py`。

### 備份目錄（禁止當來源）

本專案所需檔案**不得**從備份目錄取得或複製，以免繞過產線與驗證。

| 項目 | 說明 |
|------|------|
| **現用路徑** | `Ch1_Trust/game/`（程式、`assets/`、驗證腳本） |
| **禁止當來源** | 工作區 `ClaudeCode_Project/backup/`（`game_version1/`、`version1/`、`Demo/` 等）· `Learn_How_To_Love/Ch1_Trust/backup/`（若存在） |
| **缺檔時** | 狗 pose → `game/tools/art-pose.ps1` + Midjourney · 背景 → Nous Portal FLUX · BGM → `download-bgm.ps1` · 劇本 → Hermes + validate |
| **Agent 禁止** | `Copy-Item`／`xcopy`／`robocopy` 從 backup 補進 `game/`；以 backup 當 baseline 初始化 |
| **備份定位** | 僅使用者手動封存；清理時**勿刪** backup |
| **例外** | 使用者**明確**指示「從 backup 還原 XXX」時，才可複製**指定**檔案，且須保留 backup 原檔 |

Cursor 規則：`.cursor/rules/lhtl-ch1-backup-protected.mdc`。

---

## 七、Agent Skills 品質防線（必用）

**路徑：** `C:\Users\BaoGo\Documents\ClaudeCode_Project\Learn_How_To_Love\agent`

無論 **Cursor** 寫碼或 **Hermes** 批次產內容，**開始任務前必讀**對應 `agent/*/SKILL.md`（及該 skill 引用的 `reference.md`）。Skills 是「怎麼做才符合 LHTL」的執行規格；`MEMORY.md` 是「不能做什麼」的設定鎖定。

### 為什麼必用

| 若跳過 skill | 常見後果 |
|--------------|----------|
| 劇情不經 `story-narrative` | 班表錯、Landmark 可 S/L、基調跑掉 |
| 對白不經 `tw-narrative-voice` | 簡繁混用、說教句、非台灣用語 |
| 分支不經 `branch-engine` | choice-reactions 鍵不一致、假選擇 |
| 美術不經 `visual-art` | 狗年齡 tier 錯、版面回退、硬描邊 |
| 落地不經 `game-tester` | 流程卡住、圖文不符未發現 |

### Cursor 呼叫方式

1. **@ skill**（已同步至 `.cursor/skills/`）：`@lhtl-ch1-agent`、`@lhtl-story-narrative`、`@lhtl-branch-engine`、`@lhtl-tw-narrative-voice`、`@lhtl-visual-art`、`@lhtl-audio-sound`、`@lhtl-game-tester` 等  
2. **直接路徑**：`agent/story-narrative/SKILL.md`  
3. **Ch1 大任務**：先 `@lhtl-ch1-agent` 拆週 → 再 @ 子 skill

### Hermes 呼叫方式

在系統提示或任務開頭註明：

> 必讀 `MEMORY.md` 與 `Learn_How_To_Love/agent/<skill>/SKILL.md`；產出須通過 `Ch1_Trust/game/tools/validate-*.js`。

### 任務 → Skill 對照

| 要做的事 | 必用 skill |
|----------|------------|
| Ch1 整章推進、WeekN 落地 | [`Ch1_agent`](agent/Ch1_agent/SKILL.md) → 子 skill |
| 新場景、分支、Landmark | [`story-narrative`](agent/story-narrative/SKILL.md) |
| flags、choice-reactions | [`branch-engine`](agent/branch-engine/SKILL.md) |
| 對白、語氣潤飾 | [`tw-narrative-voice`](agent/tw-narrative-voice/SKILL.md) |
| 角色／取名／代詞審查 | [`character-bible`](agent/character-bible/SKILL.md) |
| 狗圖、背景、UI | [`visual-art`](agent/visual-art/SKILL.md) |
| BGM、狗叫、cue | [`audio-sound`](agent/audio-sound/SKILL.md) |
| playtest、驗收 | [`game-tester`](agent/game-tester/SKILL.md) |
| Steam 建置上傳 | [`steam-deployment`](agent/steam-deployment/SKILL.md) |

完整一覽與組合範例 → [`agent/README.md`](agent/README.md) · 章節落地勾選 → [`agent/chapter-landing-checklist.md`](agent/chapter-landing-checklist.md)

### 驗收閘門（產出才算完成）

```
對應 agent skill 產出
        ↓
validate-*.js 全 OK（branch／班表／時序）
        ↓
game-tester 審查（必要時）
        ↓
合併進 Ch1_Trust/game/
```

**衝突時：** `guide_line.md` > `MEMORY.md` > `story-narrative` > 其餘 skill。

### Skill 索引（摘要）

| Skill | 職責 |
|-------|------|
| `Ch1_agent` | 全章節奏、調度 |
| `story-narrative` | 場景架構、Landmark、Steam 內容量 |
| `branch-engine` | flags、choice-reactions |
| `tw-narrative-voice` | 繁體台灣語氣 |
| `character-bible` | 角色一致性 |
| `visual-art` / `audio-sound` / `music-composition` | 美術、音效、作曲 |
| `game-tester` | playtest |
| `steam-deployment` | Electron、Steamworks、CI |

---

## 八、命名與 Steam（摘要）

- **主標：** Learn How to Love（已定）  
- **標籤：** Emotional、Story Rich、Choices Matter、Dogs、Indie  
- **付費章：** 主線 >2h、目標 3–5h；Landmark ≥3／章  
- **技術必備：** Electron、Steamworks、zh-TW／en、Cloud Save  

商店文案草案、審查清單全文 → [`agent/story-narrative/steam-release.md`](agent/story-narrative/steam-release.md)

---

## 九、專案文件地圖

| 文件 | 用途 |
|------|------|
| **`guide_line.md`** | 本文件：大綱、架構、工作流 |
| **`MEMORY.md`** | 世界觀／角色鎖定（Hermes 必讀） |
| **`.cursorrules`** | 程式契約（Cursor 必守） |
| **`Ch?_*/Ch?_guide_line.md`** | 各章場景、時長、逐日 |
| **`agent/*`** | **品質防線**：Cursor／Hermes 必用 Skills（見 §七） |
| **`tools/hermes/`** | 本地編排、Nous Portal 門戶 |
| **`backup/`（工作區）** | 封存參考；**勿**當 LHTL 檔案來源（見 §二·6、§六） |
| **`Ch1_Trust/backup/`** | Ch1 封存（若存在）；同上 |

---

## 十、後續里程碑（文件外）

- [ ] 跨作存檔欄位規格（程式用）
- [ ] Electron + Steamworks 接入
- [ ] zh-TW.json 字串抽離
- [ ] Hermes 批次產線對接 validate 全通過
- [ ] Ch2／Ch3 章節指南與 aging 資產規劃

---

*最後更新：2026-07-10（§二·6、§六 備份禁止當來源）。*
