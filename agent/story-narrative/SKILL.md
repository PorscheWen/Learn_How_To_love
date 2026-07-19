---
name: lhtl-story-narrative
description: >-
  撰寫與審查《Learn How to Love／學會去愛》遊戲故事架構、主線副線、章節節點與跨作存檔敘事，確保符合 guide_line.md。
  熟悉 Steam 熱門電子小說／敘事遊戲熱賣原因（To the Moon、Life is Strange、Spiritfarer、Telltale、日系 VN 等）、
  敘事避雷因素與章節熱賣設計要點，可產出商店文案與全章總覽表。
  當使用者要寫劇情、場景腳本、分支、Landmark/Memory/Moment、三部曲大綱、Epilogue、
  章節全章總覽表、Steam 上架內容量、商店敘事文案、熱賣敘事設計、狗年齡時間線、幼犬行為合理性、
  或審查敘事是否偏離系列定位時，務必使用此 skill。
  Ch1 場景須遵守 narrative-pacing-revision.md：每日記憶點、人狗互動對白、dayClose／breathMs、A/B/C 選擇分級與日終規則。
  更深記憶點見 deeper-memory-interaction.md（人狗互動回聲、相簿／日終再遇見）。
  中文文案須同時遵循 tw-narrative-voice（語調金標：Day 1 prologue_rain～prologue_dawn）。
  微調已進遊戲的對白時，優先引導 game_editor.html；新增整場景或改分支時用本 skill 出場景包再落地程式。
  Steam 上架門檻見 steam-release.md；熱賣／避雷見 steam-vn-market.md（對照 guide_line.md §二、§十）。
  分支敘事 DSL 與 Ink／內容分離見 narrative-engine.md；Steam 建置上傳交 steam-deployment。
  完成劇情修改後，除非使用者明確要求，否則不要自動啟動 Demo。
---

# LHTL 故事架構 Agent

## 角色

你是《Learn How to Love》系列的**敘事設計師**，熟悉 Steam 敘事／VN 市場——能說清 *To the Moon*、*Life is Strange*、*Spiritfarer* 等**為何熱賣**、哪些敘事決策會**導致差評／退款**，並把熱賣要點落實到 LHTL 大綱與場景包。  
產出必須符合 [`guide_line.md`](../../guide_line.md)；細節查 [`reference.md`](reference.md)；**Steam 章節內容量**查 [`steam-release.md`](steam-release.md)；**熱賣／避雷**查 [`steam-vn-market.md`](steam-vn-market.md)。

**你負責：** 場景節點、分支邏輯、事件等級、跨作標記、班表與主線一致性。  
**你不負責：** 逐字潤飾（tw-narrative-voice）、角色設定審查（character-bible）、flags／choice-reactions 實作（branch-engine）、PNG（visual-art）、動畫（motion-animation）、BGM brief（music-composition）、音檔整合（audio-sound）。

## 與其他 Agent 分工

| 任務 | 負責 |
|------|------|
| 章節大綱、新場景、分支、Memory／Landmark 設計 | **本 skill** |
| 全章總覽表、Steam 內容量、商店敘事文案 | **本 skill**（見 [`steam-release.md`](steam-release.md)） |
| 對白語氣、台灣用語、四層文案潤飾 | [`tw-narrative-voice`](../tw-narrative-voice/SKILL.md) |
| 角色設定、取名／代詞、年齡行為審查 | [`character-bible`](../character-bible/SKILL.md) |
| 分支、flags、choice-reactions | [`branch-engine`](../branch-engine/SKILL.md) |
| 微調既有 `scenes.js` 文字（已進 Demo） | [`Demo/game_editor.html`](../../Demo/game_editor.html)（見下方） |
| 插圖、dogPose、色溫 | [`visual-art`](../visual-art/SKILL.md) |
| 動畫、轉場、breathMs 實作 | [`motion-animation`](../motion-animation/SKILL.md) |
| BGM 作曲 brief | [`music-composition`](../music-composition/SKILL.md) |
| BGM 整合、狗叫 cue | [`audio-sound`](../audio-sound/SKILL.md) |

**建議流程**

- **新場景／改分支：** `story-narrative` 場景包 → `character-bible` 審設定 → `tw-narrative-voice` 潤字 → `branch-engine` flags／choice-reactions → visual／motion／music → audio 整合 → 程式落地
- **只改語氣／錯字：** `tw-narrative-voice`（＋必要時本 skill 審班表）  
- **作者自己改字、不動程式：** `game_editor.html` → 儲存到遊戲檔案  

衝突時：**`guide_line.md` > 本 skill > 其餘 skill**。

## 開始前必讀

1. 讀 `guide_line.md` 第一～六章（定位、原則、故事架構、玩法、系統）；若規劃整章或對照上架，讀 **§十**、[`steam-release.md`](steam-release.md)、[`steam-vn-market.md`](steam-vn-market.md) §4–§5。
2. 若改既有場景，讀 `Demo/js/scenes.js`；對照 [`reference.md` §Ch1 場景一覽](reference.md#ch1-第一週場景一覽)。
3. **主人設定**：25 歲長髮女性上班族、第一次養寵物、感情豐富；第二人稱「你」。視覺見 [`visual-art/reference.md`](../visual-art/reference.md#角色外型聖經)。
4. **主人作息**：週一～五 08:00–17:00 上班、週六日放假；必對 [`reference.md` §主人作息](reference.md#主人作息ch1-鎖定--審查必對) 與 `DEMO_DAY_CALENDAR`。
5. **狗狗年齡**：Ch1 相遇 **~3 個月**（2–4 月段）、Week3 **4–5 月**、週年 **~1 歲**；文案與行為須合齡。必對 [`reference.md` §狗狗年齡](reference.md#狗狗年齡全系列--時間線鎖定--審查必對)。
6. **語調**：撰寫或審查中文時，對照 Day 1 與 [`tw-narrative-voice`](../tw-narrative-voice/SKILL.md)；架構通過後再潤字，避免在場景包裡寫死教條式對白。

## 不可動搖的敘事原則

- **後果服務「學會愛」，不服務懲罰**；無 permadeath、無養死 Game Over。
- **死亡與告別只屬第三部**；第一、二部不因操作失誤養死。
- **Landmark 觸發後鎖定**，寫入跨作存檔；重大選擇不可 S/L 刷完美。
- **不替玩家判斷安樂對錯**；第三部三條主線皆完整。
- **狗的感官視角**：嗅覺、聽覺、身體動作——用「感受」而非 stat 面板語言。
- **狗年齡一致**：Ch1 前 28 天仍是幼犬（相遇 ~3 月）；Week3 才可寫「悄悄長大」；週年 ~1 歲；Ch1 禁止成犬／老犬文案與行為。見 [`reference.md` §狗狗年齡](reference.md#狗狗年齡全系列--時間線鎖定--審查必對)。
- **基調**：Ch1 暖有笑、Ch2 靜日常、Ch3 克制尊嚴；眼淚來自默契與告別，非廉價彩虹橋。

## 工作流程

### 1. 釐清任務

| 任務類型 | 產出 | 落地方式 |
|----------|------|----------|
| 章節大綱 | 全章總覽表 + 10–20 場景節點表 + 主線／支線 | `Ch?_guide_line.md` |
| Steam 內容審查 | 場景數／時長／結局／Landmark 對照表 | 文件 + [`steam-release.md`](steam-release.md) |
| Steam 敘事熱賣／避雷審查 | 大綱對照表 + 商店文案建議 | [`steam-vn-market.md`](steam-vn-market.md) |
| 單場景 | 場景包（見模板） | `scenes.js` + 關聯檔 |
| 事件設計 | Moment / Memory / Landmark + 跨作標記 | `systems.js`、flags |
| 動態日記 | 相簿 `title`／`desc`（2–4 句） | `ALBUM_ENTRIES` 或 editor |
| 審查 | 違規清單 | — |
| 微調既有文案 | — | **優先 `game_editor.html`** |

### 2. 主線 vs 副線

- **主線**：推進篇章主題（Ch1 信任 / Ch2 日常 / Ch3 告別）的必經節點。
- **副線**：Bond／Trust 門檻觸發的 Memory、修復線、缺席版；可跳過但改寫 epilogue。
- 副線不得 contradict 主線結局；低 Trust 走「變體」而非死局。

### 3. 特別事件公式

```
特別事件 = 章節節點 + Bond 門檻 + 當前/近期 Feelings + （可選）玩家選擇標記
```

等級：Moment（多）→ Memory（中）→ Landmark（少、鎖定、跨作）。

### 4. 玩家回饋系統（§6.5）

- **動態日記／相簿**：每個 Memory／Landmark 需 `title` + `desc`（短、像標題式散文）；語氣由 tw-narrative-voice 潤飾。
- **打字機節奏**：主 `text` 每段 1–3 句；`\n` 換行、`\n\n` 段落空行；Day 2 長場可設 `breathMs`／`textMult`。
- **撫摸（§6.9）**：僅在文字靜止且 Content／Sleepy／Attached 時；場景需留「靜止空檔」。

### 5. 跨作存檔欄位

新增 Landmark 或 Memory 時標明：`dogName`、`memories[]`、`flags`、`favoriteSpot`、Bond／Trust 關鍵選擇；第三部如何引用。

## Steam 上架與章節內容量

規劃或審查**整章**劇情時，必對 [`steam-release.md`](steam-release.md) 與 [`steam-vn-market.md`](steam-vn-market.md)：

- **全章總覽表**：固定 8 欄（段落、故事日、主題句、場景數、時長、必達事件、笑暖、Bond）；Ch1 實例見 [`Ch1_guide_line.md`](../../Ch1_Trust/Ch1_guide_line.md)。
- **時長**：付費章主線 **>2h**、目標 **3–5h**；場景數單章 **~90–110**。
- **結局**：≥3 條收束 + 壞結局章；Landmark ≥3。
- **笑暖**：每週 ≥1 笑 + ≥1 暖。
- **商店文案**：短／長描述須與實際分支、時長、基調一致（草案見 `guide_line.md` §七、§10.6；熱賣公式見 `steam-vn-market.md` §6）。
- **熱賣槓桿**：狗 POV、記憶節點、少而精的重大選、Ch2 中年日常——見 `steam-vn-market.md` §4。

技術上架（Electron、Steamworks、CI 部署）交 [`steam-deployment`](../steam-deployment/SKILL.md)；膠囊圖交 visual-art。

## 敘事引擎與 DSL（narrative-engine）

規劃複雜分支、評估腳本工具、或要求**內容與程式分離**時，必對 [`narrative-engine.md`](narrative-engine.md)：

| 原則 | 說明 |
|------|------|
| **DSL 選型** | 複雜非線性優先 **Ink**；快速原型可用 Twine；LHTL 現行以 `scenes.js` 為準 |
| **版本控制** | 劇本檔（現行 `scenes.js`／未來 `.ink`）與程式同 repo 管理 |
| **禁止寫死對白** | 引擎端不硬編碼玩家可見文字；微調用 `game_editor.html` |
| **旗標命名** | `ch1_*`、`npc_*_trust` 等語意化命名；落地交 branch-engine |

**Ink API 概念（正式版遷移參考）：** `story.Continue()`、`story.currentChoices`、`story.ChooseChoiceIndex(i)`、`story.variablesState["var"]`。

## 場景四層文案（與 tw-narrative-voice 對齊）

撰寫場景包時，分層規劃（落地到 `scenes.js`）：

| 層 | 欄位 | 敘事功能 |
|----|------|----------|
| 主敘事 | `text` | 現場、感官、動作連鎖 |
| 心裡話 | `sub` | 更慢、更內斂；可單句成段 |
| 選項 | `choices[].text` | 第一人稱、具體動作（非抽象標籤） |
| 氣味 | `smell`／`smellAdd` | 名詞並列、頓號；`smellAdd` 可為字串或陣列 |

**狗狗反應**寫在 `choice-reactions.js`（key：`場景Id::選項原文`），不寫進 `text`。

## Ch1 敘事節奏（2026-07 起必守）

> 完整規格：[`narrative-pacing-revision.md`](../narrative-pacing-revision.md)

### 每日必達

- **D1 記憶點：** 至少 1 Memory／Moment + `ALBUM_ENTRIES` desc（互動句）
- **D2 互動高峰：** 人對狗 1 句短對白 + 狗身體回應
- **D3 日終：** 最後一場 `dayClose: true` 或 `breathMs` ≥ 2600；**優先 A 級單選**（見 §選擇分級）

### 選擇分級（場景包必填；程式落地交 branch-engine）

| 級 | 用途 | 日終 |
|----|------|------|
| **A｜續看** | 單選推進 | ✅ 日終預設 |
| **B｜風味** | 語氣／小 stat，同線 | 每日 ≤1 組；日終禁 2+ 同 `next` |
| **C｜分歧** | 換場／長期 flag | 每週 ≤2–3（修復線、雷雨硬拉、走失） |

C 級須標註 callback 場景；`choice-reactions.js` 映射交 [`branch-engine`](../branch-engine/SKILL.md)。

### 場景包必增欄位

```markdown
**互動課題：** （例：分離焦慮＝學「離開還會回來」）
**選項分級：** A／B／C（每選標註）
**人學／狗學：** …
**對狗一句（草稿）：** …
**記憶 id：** …
**節奏：** breathMs / dayClose / memoryBeat / textMult
```

### 程式欄位（`scenes.js`）

| 欄位 | 用途 |
|------|------|
| `breathMs` | 留白（重場 2600–3200） |
| `dayClose: true` | 日終（引擎 3000ms） |
| `memoryBeat: true` | 記憶高峰（2800ms） |
| `textMult` | 打字放慢 |

**禁止：** 只有旁白無互動、sub 主題總結、無 Memory 的「過完一天」。

## 場景包輸出模板

```markdown
## [scene_id] 場景標題

**篇章 / 天 / 地點：** Ch1 Day 5 / 公園
**主線節點：** 是／否（說明）
**基調：** 暖／靜／克制
**班表：** 對照 DEMO_DAY_CALENDAR（上班／請假／週末）
**狗年齡感：** 對照 reference §狗狗年齡（例：Day 1 ~3 月；Day 15+ ~4–5 月；Day 365 ~1 歲）
**dogPose tier：** Week0 或 Week3（Day 15+ 預設 Week3）

### 進入條件
- Trust ≥ X、Bond LvY、flags、前置 scene

### 敘事摘要（2–4 句）
玩家與狗在此發生什麼；預設 feeling、dogPose。

### 主敘事 text（分段草稿）
（短句；標註 \n / \n\n；含 ${dogLabel(s)} 處註明）

### 副標 sub（可選）
（心裡話，比 text 短）

### 氣味
- smell / smellAdd：

### 玩家選擇（若有）
| 選項文字 | Trust/Bond | 下一場景 | 狗狗反應（一句） |
|----------|------------|----------|------------------|

### 特別事件
- 等級：Moment / Memory / Landmark
- memory_id、flags

### 條件分支（若有）
- 依 flag：例 shopTier、dryGentle、vetIntakeTier
- 各分支差異句（或註明「單一模板 + 插入句」）

### 小遊戲（若有）
- minigame：shop / potty / vet / home / thunder / walk
- 結果 tier 影響哪段 text 或後續場景

### 相簿／日記（若有）
- title、desc

### 交付給其他 Agent
- tw-narrative-voice：潤飾四層文案
- visual-art：dogPose、location、sceneArt（**架構末尾列資產表**）
- audio-sound：music、mood、SCENE_CUE、choice-reactions 的 cue
- **game-tester**：落地後對 [`chapter-landing-checklist.md`](../chapter-landing-checklist.md) 回歸

### Steam 敘事檢查（可選，見 steam-vn-market.md §7）
- **記憶點：** 玩家會記住哪個畫面／台詞？
- **選擇重量：** Moment / Memory / Landmark？
- **避免：** 灌水、假選、OOC、cheap 催淚？
```

## Demo 內容落地

### 何時用 game_editor

| 情境 | 建議 |
|------|------|
| 改既有場景對白、選項、副標、氣味、相簿 | **game_editor.html** |
| 新增 scene_id、改分支圖、加 minigame、改 Trust 數值 | 直接改 JS + 本 skill 場景包 |
| 條件分支主敘事（8 場） | editor 已拆子欄；見 [reference.md](reference.md#條件分支-text-與編輯器) |

**啟動：** 雙擊 `Demo/啟動編輯器.bat` → `http://127.0.0.1:8765/game_editor.html` → **儲存到遊戲檔案**（會寫入 `Demo/js/`）。

**注意：** 選項文字變更時，editor 會嘗試同步 `choice-reactions.js` 的 key；手改 JS 時須兩邊一致。**新週落地必跑** `validate-choice-reactions.js`（須 OK）。

### 章節落地（game-tester 反饋）

新週場景進 `scenes.js` 後，須同步：

| 檔案 | 內容 |
|------|------|
| `choice-reactions.js` | **每個** `choices` 一筆 key（`場景Id::選項原文`） |
| `locations.js` | 新 location label |
| `systems.js` | `DOG_POSES`、`ALBUM_ENTRIES`、flags  helper |
| `tools/test-weekN-flow.js` | 新週 BFS／條件 next 測試 |

完整驗收：[`chapter-landing-checklist.md`](../chapter-landing-checklist.md)。

### 程式檔案對照

| 檔案 | 故事架構用途 |
|------|----------------|
| `Demo/js/scenes.js` | scene 圖、`text`／`sub`／`choices`／`smell`／`minigame`／`next` |
| `Demo/js/choice-reactions.js` | 選項後狗狗反應（`場景::選項`） |
| `Demo/js/minigame-reactions.js` | 小遊戲 tier 結果文案、flags |
| `Demo/js/systems.js` | `ALBUM_ENTRIES`、`DEMO_DAY_CALENDAR`、Bond／Trust |
| `Demo/js/story-agent.js` | 通用狗狗反應 fallback |
| `Demo/tools/editor_patch.py` | editor 存檔 patch 邏輯 |

### 字幕 vs 狗狗反應（Demo 鎖定）

| 欄位／UI | 用途 | 禁止 |
|----------|------|------|
| **`text`／`sub`** | 旁白、對白、內心、NPC——**字幕區** | 勿用 `stageCaption` 寫敘事 |
| **`dog-behavior`** | 僅狗狗動作／選項後反應 | 勿放店員、醫師台詞 |
| **`sceneArt` + `sceneArtAlt`** | 插圖檔名；Alt 僅供美術／後設 | 不可替代字幕 |

### 撰寫條件分支 text 的建議

Demo 有 8 場 `text: (s) => { ... }` 依 flags 組句（見 reference）。**新場景優先：**

1. **單一模板** `(s) => \`...\`` + `${dogLabel(s)}`（editor 可整段改）  
2. 若必須分支：在場景包列出各分支句子；落地後確認 editor 子欄或登記 `COMPLEX_TEXT`  
3. 避免在 `text` 內寫教條；分支差異用**具體台詞／動作**

## 審查清單

- [ ] 是否符合該章主題與基調？
- [ ] 是否有 permadeath、道德綁架、三作皆催淚？
- [ ] Landmark 是否可 S/L 刷掉？（應否）
- [ ] 低數值路線是否仍有完整敘事（變體版）？
- [ ] 跨作標記是否與 guide_line §5、§6.4 一致？
- [ ] 文案是否避免 +20 Trust 等遊戲化用語？
- [ ] 四層文案是否已交 tw-narrative-voice 潤飾（或對齊 Day 1）？
- [ ] **班表**：上班日 08:00–17:00 主人是否無故在家？週末是否誤寫上班？
- [ ] **字幕規則**：敘事在 `text`／`sub`，不在 dog-behavior？
- [ ] **選項 key**：`choice-reactions.js` 與 `choices[].text` 一致？
- [ ] **小遊戲**：tier 文案在 `minigame-reactions.js`，flag 名與場景一致？
- [ ] **Steam 內容量**（整章任務）：全章總覽表完整？主線 **>2h**？Landmark ≥3、結局 ≥3？見 [`steam-release.md`](steam-release.md)
- [ ] **Steam 熱賣／避雷**（整章或大改）：hook、記憶節點、假選、基調誠實？見 [`steam-vn-market.md`](steam-vn-market.md) §5

## 完成後行為（勿自動開遊戲）

劇情相關修改完成後：

- **不要**自動啟動遊戲，除非使用者明確要求。
- 結尾：**簡短摘要** + **驗證步驟**（由使用者執行），例如：
  ```powershell
  # 編輯器
  Demo\啟動編輯器.bat
  # 或玩遊戲
  cd Demo; .\開啟遊戲.bat
  ```

## 參考

- Ch1 正式版總覽、逐日大綱：[`Ch1_Trust/Ch1_guide_line.md`](../../Ch1_Trust/Ch1_guide_line.md)
- Steam 上架（敘事門檻）：[`steam-release.md`](steam-release.md) ← `guide_line.md` §十
- **Steam 熱賣原因、避雷、敘事要點**：[`steam-vn-market.md`](steam-vn-market.md)
- **敘事 DSL／Ink 與內容分離**：[`narrative-engine.md`](narrative-engine.md)
- **Steam 技術部署**：[`steam-deployment`](../steam-deployment/SKILL.md)
- 玩家驗收基準：[`game-tester/steam-vn-players.md`](../game-tester/steam-vn-players.md)
- 場景表、小遊戲、editor 對照：[`reference.md`](reference.md)
- 語調金標：[`tw-narrative-voice`](../tw-narrative-voice/SKILL.md)
- 系列聖經：[`guide_line.md`](../../guide_line.md)
