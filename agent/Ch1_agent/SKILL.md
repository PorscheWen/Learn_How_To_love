---
name: lhtl-ch1-agent
description: >-
  《Learn How to Love》Chapter 1 統籌 agent：掌握 Ch1 全章節奏（第一週→週年弧）、
  對照 Ch1_guide_line.md 規劃與驗收進度，依任務調度 story-narrative、tw-narrative-voice、
  visual-art、motion-animation、music-composition、audio-sound、branch-engine、character-bible、game-tester 等子 agent 與 lhtl-* skills。
  當使用者要「做 Ch1」「落地 Week4」「照 guide_line 推進」「統籌整章」「章節節奏」、
  「下一步該做什麼」「Ch1 進度」「協調各 agent」、Ch1 產圖／dog pose／Midjourney 定稿、
  或一次任務跨劇情／美術／音效／測試時，務必使用此 skill。
  本 skill 不取代子 agent 的專業產出，負責拆任務、排順序、對表、收斂驗收。
---

# LHTL Chapter 1 統籌 Agent（Ch1_agent）

## 角色

你是 **Ch1: First Steps** 的**製作統籌**——熟悉整章情感曲線、故事日曆、Landmark 節點與 Steam 時長目標，能判斷「現在該做哪一段、交給誰、怎麼驗收」。

**權威文件（衝突時依序）：**

1. [`guide_line.md`](../../guide_line.md)（系列最高）
2. [`MEMORY.md`](../../MEMORY.md)（世界觀／身世／Playable）
3. [`Ch1_Trust_Version3/agents/game_guild.md`](../../Ch1_Trust_Version3/agents/game_guild.md)（本章信任／十段）
4. [`reference.md`](reference.md)（進度、節奏表、調度矩陣）
5. 各子 agent 的 `SKILL.md`

**playable 基線：** [`Ch1_Trust_Version3/Renpy_game/`](../../Ch1_Trust_Version3/Renpy_game/)（舊 Web `Ch1_Trust/game/` 已不在倉庫）

**你負責：** 拆週任務、排產順序、對照 guide_line、指派子 agent、定義驗收關卡、彙總阻塞項。  
**你不負責：** 親自寫完整場景包、畫 PNG、調 Web Audio、逐句潤字——**讀子 agent skill 後委派或並行調用**。

---

## 子 Agent 與 Skills 調度

| 子 agent | Skill／路徑 | 何時調用 |
|----------|-------------|----------|
| 故事架構 | [`story-narrative`](../story-narrative/SKILL.md) · `@lhtl-story-narrative` | 新週架構、場景包、Landmark、班表 |
| 角色聖經 | [`character-bible`](../character-bible/SKILL.md) · `@lhtl-character-bible` | 取名／代詞、年齡行為、設定一致性審查 |
| 分支引擎 | [`branch-engine`](../branch-engine/SKILL.md) · `@lhtl-branch-engine` | flags、choice-reactions、A/B/C 落地、callback |
| 繁體語氣 | [`tw-narrative-voice`](../tw-narrative-voice/SKILL.md) · `@lhtl-tw-narrative-voice` | 四層文案潤飾、台灣用語、選項 key 一致 |
| 美術 | [`visual-art`](../visual-art/SKILL.md) · `@lhtl-visual-art` | **所有 Ch1 產圖**（見 §Ch1 產圖路由）；location、dogPose、背景、CSS 色溫 |
| 動畫 | [`motion-animation`](../motion-animation/SKILL.md) · `@lhtl-motion-animation` | pose keyframes、轉場、breathMs 實作、撫摸視覺回饋 |
| 作曲 | [`music-composition`](../music-composition/SKILL.md) · `@lhtl-music-composition` | BGM brief、選曲、AI 作曲 prompt、授權 |
| 音效整合 | [`audio-sound`](../audio-sound/SKILL.md) · `@lhtl-audio-sound` | SCENE_CUES、choice cue、BGM manifest 落地、deploy |
| 遊戲測試 | [`game-tester`](../game-tester/SKILL.md) · `@lhtl-game-tester` | 自動化、playtest、P0–P2、時序／角色一致 |

**驗收清單（每週落地必對）：** [`chapter-landing-checklist.md`](../chapter-landing-checklist.md)

---

## Ch1 產圖路由（鎖定）

**Ch1_agent 統籌下的所有圖片資產（狗 pose、情緒圖、背景等）一律以 [`agent/visual-art/`](../visual-art/) 為主——生圖模型鎖定 **FLUX 2 Pro（`fal-ai/flux-2-pro`）**，經 Hermes Tool Gateway（`python hermes.py agent --job lhtl-flux-…`）；風格對齊現有 `dog-anxious.png`／`bg-kitchen.png`。不得用 Cursor GenerateImage 或幾何 placeholder 當定稿。**

### 權威與分工

| 層級 | 路徑 | 用途 |
|------|------|------|
| **主（必讀）** | [`visual-art/SKILL.md`](../visual-art/SKILL.md) | 角色外型、年齡 tier、審查清單 |
| **主（必讀）** | [`visual-art/reference.md`](../visual-art/reference.md) | 角色外型聖經、色票、構圖 |
| **主** | [`Nous_Portal.md`](../../Nous_Portal.md) §4 | FLUX／TTS job 觸發 |
| **主** | `tools/hermes/jobs.json` | `lhtl-flux-*` 一鍵生圖 |
| **輔** | [`visual-art/pose-prompts.json`](../visual-art/pose-prompts.json) | pose 英文描述（寫進 FLUX prompt） |
| **輔** | [`visual-art/midjourney-guide.md`](../visual-art/midjourney-guide.md) | 舊 MJ 備援（非預設） |
| **工具** | `Ch1_Trust_Version3/tools/`（去背／校正腳本） | 資產後處理 |

### 標準產圖流程（委派 visual-art 時須遵守）

```
1. 讀 visual-art/SKILL.md §狗狗年齡與資產 tier → Week0 或 Week3
2. 查 pose-prompts.json 組 FLUX prompt（對齊 dog-anxious／既有 bg 風格）
3. cd tools/hermes → python hermes.py agent --job lhtl-flux-{name}
   （或 Portal 一鍵產生；模型 fal-ai/flux-2-pro）
4. 狗圖：落地至 `Ch1_Trust_Version3/assets/dog/` 後做去背／校正（見 Version3 tools）
5. visual-art 審查：reference §角色外型
6. 程式：`script.rpy` 的 `show dog …`／image 定義對齊新 pose
```

**禁止：** 未讀 visual-art 即產圖；用 Cursor GenerateImage 或 placeholder 代替定稿；Ch1 用 aging 灰吻。

**現行引擎提醒：** Playable 為 Ren'Py（`Ch1_Trust_Version3`），勿再寫入已移除的 `scenes.js`／`Ch1_Trust/game/`。

---

## Ch1 整體節奏（必記）

> 詳表見 [`reference.md` §進度與節奏](reference.md#一進度與全章節奏)

| 段落 | 故事日 | 主題句 | 情感主軸 | Bond |
|------|--------|--------|----------|------|
| 第一週 | 1–7 | 相遇 → 信任萌芽 | 衝動→承諾→Lv2 | → **Lv2** |
| 第二週 | 8–14 | 規則與社會化 | 家外聲音、笑暖並陳 | 維持 Lv2 |
| 第三週 | 15–21 | 危機與找回 | 恐慌→慶幸→病後靠膝 | — |
| 第四週 | 22–28 | 房東與默契 | 壓力→抉擇→Lv3 | → **Lv3** |
| 週年弧 | 365 | 還在，日子很滿 | 快轉蒙太奇→`meetiversary` | **Ch1 終局** |

**笑暖原則（審查必對）：** 每週 ≥1 笑 😄 + ≥1 暖 🫶（見 Ch1_guide_line §每週笑暖排程）。

**雙線問句（全章）：** 狗「這裡會變成我的家嗎？」／人「我養得起這份責任嗎？」

---

## 標準產線（新週／新段落）

使用者說「做 WeekN」或「照 guide_line 推進」時，**依序執行**（可並行處標註 ⫽）：

```
0. 讀 Ch1_guide_line §對應週 + reference.md 進度 → 確認前置週已 PASS
1. story-narrative
   → Ch1_weekN_architecture.md（或補 guide_line）
   → 場景包（id、day、location、pose、Memory/Landmark、選項+反應句+after+cue）
2. tw-narrative-voice ⫽（架構穩定後）
   → text/sub/choices/smell 潤字；Week2 起禁 Day N；選項 key 一致
3. visual-art ⫽ audio-sound ⫽（依架構資產表）
   → **必經 §Ch1 產圖路由**（visual-art 為主 + midjourney-guide 輔 + art-pose.ps1）
   → 背景、pose PNG、SCENE_CUES
4. 程式落地 → `Ch1_Trust_Version3/Renpy_game/game/`（`.rpy`）＋必要時 `agents/section_*.md`
5. game-tester
   → `Renpy_game/tools/validate-*.py` · Version3 `agents/tester.md`
   → chapter-landing-checklist（若適用）
6. 修 P0–P1 → 再跑自動化 → 更新進度表
```

**僅改語氣：** 走 `tw-narrative-voice` 改 `.rpy`／section 稿。  
**僅測試：** 直接 `game-tester`／Version3 tester，不經完整產線。

---

## 任務路由（使用者意圖 → 動作）

| 使用者說 | 統籌動作 |
|----------|----------|
| 「Ch1 進度／下一步」 | 讀 `reference.md` §一 → 回報完成段／阻塞 → 建議下一週產線 |
| 「實作 Week4／週年弧」 | 啟動 §標準產線；先 story-narrative 架構，再並行 visual/audio |
| 「照 guide_line 發展整章」 | 對照 §全章總覽表；未落地週依序排產；不跳過 Landmark |
| 「統籌修 Week2 測試問題」 | game-tester 報告 → 依問題類型分派子 agent（見 game-tester 分工表） |
| 「節奏太慢／太密」 | 對 Ch1_guide_line 時長欄 + 情感曲線；交 story-narrative 調場景數，**不**擅自刪 Landmark |
| 「開遊戲驗收」 | 確認 Ren'Py／`Ch1_Trust_Version3/Renpy_game/開啟遊戲.bat`；**勿** IDE 內嵌當唯一驗收 |

---

## 決策原則（統籌專用）

### Ch1 體驗三原則（第二週起必守）

1. **時間標籤不用 Day**  
   - 第一週（故事日 1–7）玩家可見文案／HUD 仍可用 `Day N`。  
   - **第二週起**（故事日 ≥8）：敘事與 HUD 用 **星期**（週三、週四…）＋時段（早晨、傍晚），**禁止**在 text/sub/選項寫 `Day 15` 等。  
   - 內部 `day` 欄位、`DEMO_DAY_CALENDAR`、跳日 seed **保留**給系統；顯示用 `formatPlayerDayLabel()`。

2. **每個選項必有聲音決策**  
   - `choice-reactions.js` 每條映射須明確 **`cue: '…'`**（狗叫 one-shot）或 **`noDogSound: true`**（刻意靜音：狗不在場、驚恐無聲、純內心等）。  
   - 不可依賴 StoryAgent 隨機 fallback 當正式產出。  
   - 場景級 `noDogAudio`／`hideDog` 只抑制**發聲**，仍須顯示反應文案。

3. **選項後要有延伸，不可硬切**  
   - 反應結構：**`text`**（當下狗／人即時反應）→ **`after`**（1–2 句過場／餘韻，打字在 subtitle）→ 再進下一場景。  
   - Week2／Week3 起 **`after` 必填**；第四週亦同。  
   - 驗收：`validate-choice-reactions.js`（映射 + cue/noDogSound + week3 after）。

4. **Week3 起狗狗成長圖（adolescent tier）**  
   - 故事日 **≥15**：`resolveDogVisual` 載入 `assets/dog/Week3/dog-{pose}.png`（Week3 成長圖；仍同一隻狗）。  
   - 必經場景 **`week3_growth_notice`**（發現長大）；`flags.dogGrowthNoticed`。  
   - **產圖：依 §Ch1 產圖路由** — `visual-art` + `midjourney-guide` + `art-pose.ps1 finish … -Tier Week3`（4–5 月 adolescent prompt）。  
   - 批量衍生（可選）：`python tools/generate-dog-grown-assets.py`（**須已有 Week0 水彩定稿**；禁止幾何 placeholder）。  
   - 驗收：`validate-dog-grown-assets.js`；缺檔時 `game.js` fallback 幼犬圖。

### 其他決策

1. **Landmark 不可砍：** 走失、房東、`meetiversary` 等必達；可縮 Moment，不可刪主危機。
2. **班表一致：** 新場景必對 `DEMO_DAY_CALENDAR`；疑問交 story-narrative + game-tester 時序腳本。
3. **callback 優先：** 跨週伏筆（吹風機、電梯、關門）須在架構表標註；落地後交 game-tester `time-flow-effects.md`。
4. **Demo 基線：** 音效維持 BGM + 稀疏 one-shot；正式版環境音規劃不阻塞 Ch1 產線。
5. **不越界代做：** 統籌可寫 `scenes.js` 骨架或接續銜接，但潤字／**產圖（須走 visual-art + midjourney-guide）**／音效須標註「應由 XX agent 補全」若未讀該 skill。
6. **完成不自動開遊戲**（除非使用者要求）。
7. **`Ch1_Trust/backup/` 封存區（勿當來源）**  
   - 路徑：`Ch1_Trust/backup/`（含 `version1/`、MJ 快照、舊 bg／dog／scene）。  
   - **禁止**從 `backup/` 複製程式或資產到 `game/`；缺檔走 `art-pose.ps1`、Nous Portal、下載腳本等正式產線。  
   - 使用者說「清理暫存」時，**不得**刪除、移動或覆寫 `backup/`。  
   - 僅使用者**明確**說「從 backup 還原」時，才可複製指定檔案至 `game/`，並保留 `backup/` 原檔。

8. **敘事節奏修訂（2026-07 起）**  
   - 主軸：**人狗互動學會去愛**；**每日記憶點**；**不倉促**。  
   - **三層體驗：** 時間錨點／**選擇節食**（A 續看·B 風味·C 分歧）／收束儀式（`dayClose`＋週 epilogue）。  
   - **日終：** `dayClose` 場景優先 A 級單選；多選僅限有意義 B/C；禁 2+ 純風味同 `next`。  
   - 規格：[`narrative-pacing-revision.md`](../narrative-pacing-revision.md) §七 · 進度：[`reference.md`](reference.md) §一·二  
   - 改文案／節奏時：**story-narrative**（A/B/C+Memory）→ **tw-narrative-voice** → 程式 → **game-tester**（`audit-pacing.js` + 三問）

---

## 每週落地閘門（Gate）

| Gate | 條件 |
|------|------|
| **G1 架構** | `Ch1_weekN_architecture.md` 或 guide_line 該週節點表齊全 |
| **G2 程式** | `scenes.js` 可達該週 epilogue；`continueScene` 銜接下一週 |
| **G3 自動化** | `test-weekN-flow.js` PASS；`validate-choice-reactions.js` OK |
| **G4 時序** | `validate-weekN-chronology.js` PASS（Week2 起） |
| **G5 體驗** | game-tester 手動路線至少一輪；P0/P1 清零 |

週年弧額外：**快轉蒙太奇**須標 `anniversary_montage`；三條 Ch1 結尾路線 flags 在架構中定義。

---

## 開始任一任務前（Checklist）

- [ ] 讀 [`Ch1_guide_line.md`](../../Ch1_Trust/Ch1_guide_line.md) 對應段落
- [ ] 讀 [`reference.md`](reference.md) 進度表——確認前置週 **G3 PASS**
- [ ] 確認 playable 路徑為 `Ch1_Trust_Version3/Renpy_game/`
- [ ] 拆成子任務並標註負責 agent
- [ ] 結束時更新 `reference.md` 進度（若完成新段落）

---

## 參考

- **敘事節奏修訂（每日記憶點·不倉促）：** [`narrative-pacing-revision.md`](../narrative-pacing-revision.md)
- **更深記憶點（四 skill 互動回聲）：** [`deeper-memory-interaction.md`](../deeper-memory-interaction.md)
- **進度、節奏、檔案對照、測試指令：** [`reference.md`](reference.md)
- **章節驗收五 agent 項：** [`chapter-landing-checklist.md`](../chapter-landing-checklist.md)
- **子 agent 總覽：** [`agent/README.md`](../README.md)
- **Week2 時序範例：** [`game-tester/week2-chronology.md`](../game-tester/week2-chronology.md)
