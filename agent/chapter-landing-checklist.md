# 章節落地驗收清單

> **來源：** Ch1 Week2 playtest（game-tester）後的 P2 教訓，供 story／tw-narrative-voice／visual-art／audio-sound 落地時對照，**game-tester 回歸時必查**。  
> playable 路徑：**`Ch1_Trust/game/`**（優先於 `Demo/`）。

---

## 一、story-narrative

| # | 項目 | 通過條件 |
|---|------|----------|
| 1 | 架構文件 | 新週有 `Ch1_weekN_architecture.md`（或 guide_line §）：場景 id、Day、location、dogPose、Memory／Landmark |
| 2 | 場景包 | 每個有 `choices` 的場景，表格含 **選項原文 + 分級 A/B/C + 狗狗反應一句**（供 branch-engine／`choice-reactions.js`） |
| 3 | 跨週 callback | 文案用「第一天／第三週」等中文錨，**不寫 Day1／Week2**（交 tw-narrative-voice 潤） |
| 4 | 資產表 | 架構末尾列 **新 location、新 dogPose、新 minigame** → 交 visual-art／audio-sound |
| 5 | **敘事節奏** | 對照 [`narrative-pacing-revision.md`](narrative-pacing-revision.md)：每日 D1 記憶點、D2 人狗對白、D3 日終 `dayClose`／`breathMs`；場景包含互動課題欄 |

---

## 二、tw-narrative-voice

| # | 項目 | 通過條件 |
|---|------|----------|
| 1 | 英文殘留 | 無 `Day1`～`Day7`、`Week1`～`Week4` 出現在玩家可見字幕 |
| 2 | 時間 callback | 用「第一夜／第一天／第一週／第三天的拖鞋」等台灣口語 |
| 3 | 選項 key | `choices[].text` 與 `choice-reactions.js` key **逐字一致** |
| 4 | 掃描 | `node tools/tw-locale-pass.js` 通過 |
| 5 | **text／sub 分層** | `text`＝現場動作；`sub`＝內心一句；禁主題總結、禁 text/sub 情緒重複（§ [`narrative-pacing-revision.md`](narrative-pacing-revision.md) §二） |
| 6 | **人對狗對話** | 每天至少 1 句短對白（「」）；相簿 desc 寫互動句，非「這是成長」 |

---

## 二b、branch-engine

| # | 項目 | 通過條件 |
|---|------|----------|
| 1 | choice-reactions | 每個 `choices` 有 `` scene_id::選項原文 `` 映射 |
| 2 | 分級 | A/B/C 標註；日終無 2+ 純風味同 `next` |
| 3 | flags | 新 C 級有寫入與 callback 讀取 |
| 4 | 驗證 | `node tools/validate-choice-reactions.js` OK |

---

## 二c、character-bible

| # | 項目 | 通過條件 |
|---|------|----------|
| 1 | 取名時間線 | 取名前僅「牠」；取名後 `dogLabel` |
| 2 | 代詞 | female→她、male→他；無硬編碼狗名 |
| 3 | 年齡行為 | 對照 reference 狗年齡表 |
| 4 | 班表 | 上班日無无理由全天在家 |

---

## 三、visual-art

| # | 項目 | 通過條件 |
|---|------|----------|
| 1 | 新 location | `bg-{slug}.png` + `style.css` 的 `.loc-{location_id}`；`locations.js` 有 label |
| 2 | 色溫 | 新背景若 AI 生成，須對齊 `#app.cold`／`#app.content`（必要時 `.loc-*` 覆寫 filter） |
| 3 | 新 dogPose | **`assets/dog/Week0/dog-{pose}.png` 專用圖**（Week3+ → `Week3/`）；**禁止**長期用 `DOG_POSE_ASSET` 別名代替故事 pose |
| 3b | **產圖流程** | **Ch1_agent 必經** [`visual-art/SKILL.md`](visual-art/SKILL.md) + [`midjourney-guide.md`](visual-art/midjourney-guide.md) 輔；`art-pose.ps1 mj/finish`；見 [`Ch1_agent/SKILL.md` §產圖路由](Ch1_agent/SKILL.md#ch1-產圖路由鎖定) |
| 4 | 去背 | `python Ch1_Trust/game/tools/remove_dog_bg.py`（新增 PNG 後；`art-pose.ps1 finish` 會自動跑） |
| 5 | 動畫 | 新 pose 交 **motion-animation** 在 `style.css` 補 `.dog-img[src*="…"]`（alert／play／sniff 等） |
| 6 | 禁止 | 多狗同框、狗畫進背景 PNG |

**Week2 參考 pose：** `alert-ears`、`leash`、`phone-pose`、`sock`、`park-tree`、`park-play`、`bite-teach`  
**Week2 參考背景：** `hallway_neighbor`、`elevator`

---

## 四、audio-sound

| # | 項目 | 通過條件 |
|---|------|----------|
| 1 | SCENE_CUES | **有狗在場的每個新 scene_id** 一筆 `{ delay, cue }`（非僅 Landmark） |
| 2 | 選項狗叫 | 分支／情緒 beat 的選項在 `choice-reactions.js` 含 `cue`（key 缺漏 → P2） |
| 3 | 小遊戲 | 新 minigame tier 在 `minigame-reactions.js` 有 `cue` |
| 4 | 基線 | 維持 Demo：僅 BGM + 稀疏 one-shot；`noDogAudio` 場景不發狗聲 |
| 5 | 驗證 | 不自動開遊戲；使用者要求時才 `開啟遊戲.bat` 聽音 |

**Week2 cue 範例：** 鄰居 `murmurLow`、電梯 `murmurAnxious`、公園 `sniffDeep`／`yipExcited`、結語 `sleepSnoreDeep`

**新 BGM：** 先 **music-composition** brief → **audio-sound** 整合 `audio-tracks.js` + CREDITS

---

## 四b、motion-animation

| # | 項目 | 通過條件 |
|---|------|----------|
| 1 | 新 pose 動畫 | `style.css` 有 `.dog-img[src*="pose-id"]`；複用 `dogBob`／`dogAlert` 等（見 motion-animation reference） |
| 2 | has-choices | 選項出現時呼吸動畫正確暫停 |
| 3 | breathMs | 重場 2600–3200；日終 `dayClose`；`node tools/audit-pacing.js` 通過 |
| 4 | 撫摸 | `.is-pettable`／`.is-petting` 視覺回饋符合 §6.9 |

---

## 四c、music-composition（新曲時）

| # | 項目 | 通過條件 |
|---|------|----------|
| 1 | brief | profile 名稱、情緒、樂器、禁止項 |
| 2 | 授權 | CREDITS.md 已登記；Steam 可署名 |
| 3 | 整合 | 交 audio-sound 更新 manifest + deploy |

---

## 五、game-tester（回歸）

### 自動化（遊戲根目錄）

```powershell
cd Ch1_Trust\game
node tools/test-week1-flow.js      # 全章場景鏈
node tools/test-week2-flow.js      # 依週增補（Week3 起同理）
node tools/validate-choice-reactions.js   # 須 OK: all choices mapped
node tools/tw-locale-pass.js
```

### 敘事節奏（Ch1 改文案後必查）

對照 [`narrative-pacing-revision.md`](narrative-pacing-revision.md) §六：

1. 今天讀者會記得哪個畫面或哪句對白？
2. 今天最後一場有沒有「停下來」的感覺（`dayClose`／足夠留白）？
3. 像「過完一天」還是「跳過幾張卡」？

### 手動（新週至少一次）

| Day 範圍 | 必測 beat |
|----------|-----------|
| Week2 8–14 | 鄰居／電梯阿黃／相簿／襪子／公園樹／bite minigame／`landmark_gentle_rules` |
| 分支 | 電梯硬拉、socialTier close／wide、dryGentle、bite tier |
| **角色一致** | 取名路線 ×2 + [`character-consistency.md`](game-tester/character-consistency.md) 審查表 |
| **時間流動** | callback 路線 + [`time-flow-effects.md`](game-tester/time-flow-effects.md) 審查表 |

### 報告必含

- P0–P2 分級 + **負責 agent**（見 [`game-tester/SKILL.md`](game-tester/SKILL.md) 分工表）
- **角色與展現一致性表**（取名、狗／主人、HUD／相簿／存檔）
- **時間流動與身心變化表**（callback、Bond 跨週、外部事件）
- Steam 敘事體驗表 + 模擬好／差評一句

---

## 六、建議落地順序

```
Ch1_agent（讀 guide_line + reference 進度、拆週任務）
    → story-narrative（架構 + 場景包）
    → character-bible（審設定）
    → tw-narrative-voice（四層文案）
    → branch-engine（flags + choice-reactions）
    → visual-art + motion-animation + music-composition（可並行）
    → audio-sound（BGM 整合 + SCENE_CUES）
    → scenes.js / choice-reactions.js / systems.js
    → game-tester（本清單 §五）
    → 各 agent 修 P0–P1 → 再跑自動化
```
