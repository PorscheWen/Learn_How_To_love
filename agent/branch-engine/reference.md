# LHTL 分支引擎參考表

> playable：`Ch1_Trust/game/js/` · 驗證：`tools/validate-choice-reactions.js`

## CHOICE_REACTIONS 欄位

| 欄位 | 必填 | 說明 |
|------|------|------|
| `text` | ✅ | `(s) =>` 函式；用 `dogLabel(s)`／`dogPronoun(s)` |
| `feeling` | ✅ | 對應 `FEELINGS` key |
| `cue` | 建議 | 狗聲 one-shot；交 audio-sound 確認池 |
| `dogPose` | 可選 | 覆蓋當場 pose |
| `holdMs` | 可選 | 反應展示延長 |
| `after` | 可選 | 反應後跳場（少用，優先 scenes next） |

## Ch1 常用 flags（節選）

| flag | 寫入時機 | 讀取／callback |
|------|----------|----------------|
| `dogNamed` / `dogGender` | `day2_naming`／`day2_gender` | 全章 `dogLabel` |
| `dryGentle` | 吹風機溫和選項 | Week2 吹風機 |
| `followVariant` | `close`／`far` | 跟隨 pose |
| `socialTier` | `neutral`／`close`／`wide` | 社交敘事變體 |
| `neighborMet` | Week2 鄰居 | Week3 走失 |
| `neighborComfortFirst` | 鄰居安撫選項 | 走失協助線 |
| `biteTier` | 防咬 minigame | 教導敘事 |
| `vetTier` / `shopTier` | 小遊戲 | 後續 sub 變體 |
| `afraidOfThunder` | Day6 雷雨 | 跨週 callback |
| `dogGrowthNoticed` | Week3 成長 | 相簿、敘事 |

完整清單見 `systems.js` `createInitialState().flags` 與 Week2+ 動態寫入。

## callback 鏈範例（Ch1）

```
Day1 吹風機 dryGentle
  → Week2 week2_dryer_truce

Day1–2 取名／性別
  → 全章 dogLabel／dogPronoun

Week2 電梯阿黃
  → week2_park_play → week3_leash_tangle

Week2 neighborMet + neighborComfortFirst
  → Week3 走失結局變體
```

## minigame tier → flags

| minigame | tier 欄位 | 典型值 |
|----------|-----------|--------|
| shop | `shopTier` | good / ok / rush |
| vet | `vetTier` | good / anxious |
| home | `homeExploreTier` | good / cautious |
| thunder | `thunderHandled` | boolean |
| walk | `walkGuideTier` | calm / pull |
| bite | `biteTier` | gentle / harsh |

結果反應：`minigame-reactions.js` + 對應 flags 寫入 `systems.js` handler。

## 驗證指令

```powershell
cd Ch1_Trust\game
node tools\validate-choice-reactions.js   # 須 OK: all choices mapped
node tools\audit-pacing.js                # 日終多選、dayClose
node tools\test-week1-flow.js             # 分支鏈不斷
```

## 假選擇檢查

| 徵兆 | 處理 |
|------|------|
| 3 選項同 `next`、同 flags、反應可互換 | 合併為 1 A 或保留 1 B 風味組 |
| 日終 2+ 選項僅用語不同 | 合併 A 單選 |
| C 級寫 flag 但全章無讀取 | 刪 flag 或補 callback 場景 |
| choice-reactions 寫死「豆花」 | 改 `dogLabel(s)` |
