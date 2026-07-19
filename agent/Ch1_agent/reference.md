# Ch1 統籌參考（進度 · 節奏 · 調度）

> 權威敘事：[`Ch1_Trust/Ch1_guide_line.md`](../../Ch1_Trust/Ch1_guide_line.md)  
> playable：**`Ch1_Trust/Renpy_game/`**（`game/week1.rpy`）· 內文編輯器：`啟動編輯器.bat`  
> **本檔進度表由統籌 agent 維護**——完成新段落後更新 §一。

---

## 一、進度與全章節奏

### 1.1 落地狀態（程式）

| 段落 | 故事日 | 目標場景數 | 程式狀態 | 架構文件 | 自動化 | 備註 |
|------|--------|------------|----------|----------|--------|------|
| 第一週 | 1–7 | ~57–58 | ✅ Ren'Py（**2026-07-11**：責任書改回 **Day4 醫院** `day4_responsibility_sign`；寵物店只取名） | `Ch1_week1_architecture.md` | 編輯器 parse | Bond→Lv2；含 `day2_bath` |
| 第二週 | 8–14 | ~16 | ⬜ Ren'Py 待落地（HTML 舊版曾完成） | `Ch1_week2_architecture.md` | — | 銜接 Week3 |
| 第三週 | 15–21 | 20 | ⬜ Ren'Py 待落地 | [`Ch1_week3_architecture.md`](../../Ch1_Trust/Ch1_week3_architecture.md) | — | Landmark 走失 |
| 第四週 | 22–28 | **11** | 📝 架構完成 | [`Ch1_week4_architecture.md`](../../Ch1_Trust/Ch1_week4_architecture.md) | — | 房東、Lv3 |
| 週年弧 | 365 | ~6–8 | ⬜ 未落地 | guide_line §週年弧 | — | `meetiversary` 終局 |

**下一個統籌建議：** Week2 架構對齊 → Ren'Py `week2.rpy` 落地；或先用內文編輯器潤 Week1。

### 1.2 情感與數值節奏

| 檢查點 | 故事日 | Trust／Bond 預期 | 必達事件 |
|--------|--------|------------------|----------|
| 第一週末 | 7 | Bond **Lv2** | 雷雨或靜日、`sad_day` |
| 第二週末 | 14 | 維持 Lv2；可 `landmark_gentle_rules` | 電梯、公園樹、防咬 |
| 第三週末 | 21 | Trust 回升弧 | **`landmark_lost_found`**、病後靠膝 |
| 第四週末 | 28 | Bond **Lv3** | 房東 Landmark、默契終章 |
| 週年 | 365 | Ch1 終局存檔 | **`meetiversary`** |

### 1.3 笑暖排程（審查用）

| 週 | 😄 笑 | 🫶 暖 |
|----|-------|-------|
| W1 | `day3_slipper` 等 | `knee`、`day7_moment` |
| W2 | `week2_sock_snatch` | `week2_camera_roll`、`week2_dryer_truce` |
| W3 | `week3_delivery_bark` → `rainy_home` → … → `leash_tangle` | 7 過場（雨夜、週四晨、門後平靜、走失夜、週五陪、週六晨、獸醫夜） |
| W4 | `week4_toy_three_min`、`week4_bag_pounce` | `week4_goodnight_ritual`、`week4_dog_walk_group` |
| 週年 | 蛋糕玩鬧 | `anniversary_old_umbrella`、`meetiversary` |

---

## 一·二、2026-07 敘事節奏修訂（統籌紀錄）

**主軸：** 人狗互動學會去愛 · 每日記憶點 · 不倉促  
**已完成（P0）：**

| 類別 | 內容 |
|------|------|
| Ren'Py Week1 | **2026-07-11** 責任書改回醫院：`day4_responsibility_sign`（reception→責任書→intake）；Day2 寵物店只取名；explore／slipper／chew／D5–D7 情緒仍保留 |
| 引擎（舊 HTML） | `SCENE_BREATH_MS` 等——HTML `Ch1_Trust/game/` 已移除，以 Ren'Py 為準 |
| Memory | `day2_responsibility_sign`、`day2_explore_hallway`、`day3_slipper`、`day6_quiet_day` 等 |
| 驗收 | 編輯器 parse 58 labels；鏈：`petshop_after`→`responsibility_sign`→`naming` |

**2026-07-05 節奏掃描（日子感／防疲憊）：**
- 規格：[`narrative-pacing-revision.md`](../narrative-pacing-revision.md) §七（三層框架、A/B/C 分級、日終規則）
- 工具：`node tools/audit-pacing.js`
- 已修：Week2–3 日終**純風味**多選合併為 A 級單選；meta／主題 sub 改具象（`week2_epilogue`、`week3_delivery_bark` 等）
- 保留多選：`week2_neighbor_after`（`neighborMet`）、`week2_elevator_after`（`socialTier`）、`week2_sock_snatch` 等 C/B 高峰

**待辦（P1）：** Week4 程式落地；週年蒙太奇架構。阿黃 companion MJ sref 可重跑 `art-companion.ps1 batch`。

**game-tester 修訂（2026-07-05）：** `week2_calendar`「週六」→「後天」；`day2_gender`／Day2 分支 sub；Week2–3 日終 `dayClose` + 缺 sub 場景；刪 `choice-reactions` 重複 key。**Week2/3 Day3 準則**（同日）：電梯／公園／吹風機／防咬／外送／門縫／走失／病後等場補對白；`week2_epilogue`／`week3_epilogue` 改具象夜場收束。**P1 補齊**：`week2_no_bite_after` ok／harsh 分支對白；`week3_leash_tangle`「好了，沒纏了。」**台灣口語句長**（2026-07-05）：全章 Ch1 禁單字「在」「好」；宜「我在這」「好喔」——見 `lhtl-tw-narrative-voice` §人對狗對白句長。

---

```
Day 1–7    第一週   相遇、取名、獸醫、認家          → week1_epilogue
Day 8–14   第二週   鄰居、電梯、公園、防咬          → week2_epilogue → week3_intro
Day 15–21  第三週   走失、發燒、病後靠膝            → week3_epilogue
Day 22–28  第四週   房東、加班、默契終章            → week4_ch1_finale（待實作）
Day 365    週年弧   蒙太奇、慶祝、Ch1 落幕          → ch1_anniversary_epilogue（待實作）
```

**日曆權威：** `Ch1_Trust/game/js/systems.js` → `DEMO_DAY_CALENDAR`（Day 1＝週三傍晚）。

---

## 三、調度矩陣（產出物 → 檔案）

| 子 agent | 主要產出 | 落地檔案 |
|----------|----------|----------|
| story-narrative | 架構 md、場景包、flags | `Ch1_weekN_architecture.md`、`scenes.js`、`systems.js` |
| tw-narrative-voice | 潤色後四層文案 | `scenes.js`；key 對 `choice-reactions.js` |
| visual-art | PNG、CSS location | `assets/bg/`、`assets/dog/`、`css/style.css`、`locations.js` |

#### visual-art 產圖（Ch1 鎖定）

> 詳 [`SKILL.md` §Ch1 產圖路由](SKILL.md#ch1-產圖路由鎖定)

| 步驟 | 指令／檔案 |
|------|------------|
| 規格 | `agent/visual-art/SKILL.md` · `reference.md` · `pose-prompts.json` |
| MJ 輔助 | `agent/visual-art/midjourney-guide.md` |
| 一鍵 prompt | `Ch1_Trust/game/tools/art-pose.ps1 mj {pose}` · **狗友** `art-companion.ps1 mj sit` |
| Week0 重產 | `art-pose.ps1 regenerate Week0`（歸檔至 `_archive/`，**禁止 version1**） |
| **備份（勿刪、勿當來源）** | `Ch1_Trust/backup/` — 僅封存；Agent 不得複製至 `game/`（除非使用者明確要求還原） |
| 進度 | `art-pose.ps1 status Week0` · `mj-batch-week0/status.json` |
| 存檔去背 | `art-pose.ps1 finish {pose} 下載.png`（Week3：`-Tier Week3`） |
| 驗收 | visual-art 審查清單 · `validate-dog-grown-assets.js` |
| audio-sound | cue 表 | `js/dog-audio.js`、`choice-reactions.js`（cue 欄） |
| game-tester | 報告、腳本 | `tools/test-weekN-flow.js`、`tools/validate-*.js` |

### Week4 預定 scene_id（guide_line）

| scene_id | 事件等級 |
|----------|----------|
| `week4_landlord_call` | Landmark |
| `week4_toy_three_min` | Moment |
| `week4_landlord_choice` | 分支 → `landlordOutcome` |
| `week4_goodnight_ritual` | Memory |
| `week4_overtime_wait` | Memory |
| `week4_bag_pounce` | Moment |
| `week4_dog_walk_group` | Memory |
| `week4_ch1_finale` | Landmark |

### 週年弧預定 scene_id

`anniversary_montage` · `anniversary_morning` · `anniversary_old_umbrella` · `anniversary_party` · `anniversary_dog_friends` · `anniversary_wish` · `ch1_anniversary_epilogue`

---

## 三·五、Ch1 體驗三原則（第二週起）

| # | 原則 | 落地 |
|---|------|------|
| 1 | **不用 Day 標日子** | HUD／相簿／跳日選單用 `formatPlayerDayLabel()`；敘事用「週X＋時段」 |
| 2 | **選項必有聲音決策** | `choice-reactions` 每條：`cue` 或 `noDogSound: true` |
| 3 | **選後有延伸** | `text` + `after`（subtitle 過場）再 `next`；Week2／Week3+ `after` 必填 |
| 4 | **Week3+ 成長圖** | 故事日 ≥15 → `assets/dog/Week3/` adolescent PNG；**產圖走 visual-art + midjourney-guide + art-pose.ps1 -Tier Week3** |

詳見 [`SKILL.md` §Ch1 體驗三原則](SKILL.md#ch1-體驗三原則第二週起必守)。

---

## 四、驗收指令（依週）

```powershell
cd Learn_How_To_Love\Ch1_Trust\game

# 全章回歸
node tools/test-week1-flow.js
node tools/validate-choice-reactions.js
node tools/tw-locale-pass.js

# 各週（已落地）
node tools/test-week2-flow.js
node tools/validate-week2-chronology.js
node tools/test-week3-flow.js
node tools/validate-week3-chronology.js
node tools/validate-companion-ah-huang.js   # 阿黃狗友圖／場景／音效
node tools/validate-dog-grown-assets.js   # Week3+ 成長圖
node tools/audit-pacing.js                # 節奏：日終 dayClose、日終多選、主題句
```

**閘門定義：** 見 [`SKILL.md` §每週落地閘門](SKILL.md#每週落地閘門gate)。

---

## 五、跨週 callback 清單（統籌審查）

| 伏筆 | 種下 | 回收 |
|------|------|------|
| 吹風機 `dryGentle` | Day 1 `prologue_dry` | Week2 `week2_dryer_truce` |
| 關門／走廊 | Day 1 雨夜 | Week2 鄰居 → Week3 門沒關好／走失 |
| 拖鞋輕重 | Day 3 `day3_slipper` | Week2 防咬 |
| 電梯阿黃 | Week2 | Week2 公園、Week3 牽繩 |
| 獸醫簽名 | Day 4 | Week3 發燒複診 |
| 房東（預告） | Week3 epilogue | Week4 主線 |

詳審：[`game-tester/time-flow-effects.md`](../game-tester/time-flow-effects.md)

---

## 六、阻塞項模板（統籌記錄用）

| 阻塞 | 負責 agent | 解除條件 |
|------|------------|----------|
| （範例）Week4 無架構 | story-narrative | `Ch1_week4_architecture.md` 完成 ✅ |
| （範例）choice-reactions 缺漏 | tw-narrative-voice + story | `validate-choice-reactions.js` OK |

---

## 七、狗友 NPC｜阿黃（ah_huang）

> 劇情名 **阿黃**（金毛中型犬）；口語有時稱「大黃」。與主角幼犬分開繪製。

| 項目 | 路徑／欄位 |
|------|------------|
| 靜態 pose | `assets/dog/companions/ah-huang/sit.png` · `sniff-greet` · `play` · `leash` |
| 產圖 | `.\art-companion.ps1 batch` → Midjourney Relax → `finish-downloads`（prompt 含 `MJ_SREF`） |
| placeholder | `python tools/generate-ah-huang-assets.py`（僅開發用） |
| 程式 | `systems.js` → `COMPANION_DOGS`、`resolveCompanionVisual` |
| 場景 | `week2_elevator_dog`（sit）· `week2_park_play`（play）· `week3_leash_tangle`（leash） |
| 音效 | `dog-samples.js` → `friend` 池；`dog-audio.js` → `companionCue` |
| 驗證 | `node tools/validate-companion-ah-huang.js` |

---

*最後更新：2026-07-10 · Week1 依 architecture 責任書回 Day2＋情緒文案 · Week2–3 已落地 · Week4 架構待程式 · 阿黃 companion 已接*
