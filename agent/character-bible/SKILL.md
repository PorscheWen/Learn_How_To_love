---
name: lhtl-character-bible
description: >-
  審查與維護《Learn How to Love／學會去愛》角色設定聖經：主人「你」、狗狗、NPC、取名／代詞時間線、
  狗年齡行為、跨場景／相簿／存檔一致性。
  當使用者提到角色一致性、取名、代詞、他她牠、狗年齡、主人設定、第一次養寵、
  阿黃、角色外型、硬編碼狗名、dogLabel、班表違規時，務必使用此 skill——
  即使未明說 skill 名稱也應觸發。場景架構交 story-narrative；潤字交 tw-narrative-voice；視覺 PNG 交 visual-art。
---

# LHTL 角色聖經 Agent

## 角色

你是《Learn How to Love》系列的**角色設定守門人**。須符合 [`guide_line.md`](../../guide_line.md) 與 [`reference.md`](reference.md)。

**你負責：** 主人／狗／NPC 設定鎖定、取名時間線、代詞契約、年齡行為合理性、跨 surface 一致審查。  
**你不負責：** 寫新場景包（story-narrative）、分支 flags（branch-engine）、畫 PNG（visual-art）。

## 開始前必讀

1. [`reference.md`](reference.md) — 角色表、時間線、NPC 登記
2. [`game-tester/character-consistency.md`](../game-tester/character-consistency.md) — 測試路線
3. [`deeper-memory-interaction.md`](../deeper-memory-interaction.md) — 人狗彼此回應與記憶點加深
4. `Ch1_Trust/game/js/systems.js` — `dogLabel`、`dogPronoun`、`applyDogPronouns`、`setDogProfile`
5. [`visual-art/reference.md`](../visual-art/reference.md#角色外型聖經) — 視覺外型（敘事須對齊）

## 主人「你」（全系列鎖定）

| 項目 | 規格 |
|------|------|
| 年齡 | **25 歲** |
| 性別 | **年輕長髮女性** |
| 職業 | **上班族**（週一～五 08:00–17:00） |
| 寵物經驗 | **第一次養寵物** — 會慌、查手機、問店員 |
| 性格 | **感情豐富** — 易共感、內疚、溫柔 |
| 敘事 | 第二人稱「你」；固定女主視角 |
| Demo 視覺 | **不露全臉**；局部見 visual-art |

**禁止：** Day1–2 像資深飼主；上班日無理由全天在家（除非 `flags` 請假明示）。

## 狗狗（全三部曲同一隻）

| 項目 | 規格 |
|------|------|
| 身份 | **混種幼犬** scruffy mixed breed；非可辨識純種 |
| 毛色 | golden-tan / honey ochre |
| Ch1 年齡 | 相遇 **~3 月** → Week3 **4–5 月** → 週年 **~1 歲** |
| 敘事 | 感官視角（嗅、聽、身體）；禁 stat 面板語言 |
| 禁止 | Ch1 寫成犬／老犬；換品種；多狗同框（主角） |

行為合齡表見 [`reference.md`](reference.md) §狗年齡行為。

## 取名／代詞時間線（程式契約）

| 階段 | 場景 | 字幕規則 |
|------|------|----------|
| **取名前** | `prologue_*`～`day2_petshop` | 指狗用 **「牠」**；禁玩家自訂名 |
| **取名中** | `day2_naming` | UI 輸入；空則預設「豆花」 |
| **性別** | `day2_gender` | 「{名字} 是弟弟還是妹妹？」 |
| **取名後** | `day2_return` 起 | `dogLabel(s)` + `dogPronoun(s)` |

```javascript
dogLabel(s)   // 有名字→名字；無→「牠」
dogPronoun(s) // female→她、male→他、未設→牠
// choice-reactions 必須 text: (s) => `${dogLabel(s)}…`
```

## NPC 登記

| ID | 角色 | 首次場景 | 備註 |
|----|------|----------|------|
| `ah_huang` | 阿黃（狗友） | `week2_elevator_dog` | companion 資產；非主角狗 |
| 店員 | 寵物店大姐 | `day2_petshop` | `scene-petshop-clerk.png` |
| 獸醫 | 專業穩重 | `day4_vet` | 白袍／制服 |

新 NPC 須登記 [`reference.md`](reference.md) 並對齊 visual-art scene-art。

## 審查工作流程

### 1. 文案掃描（新週／大改後）

- [ ] 取名前無自訂名／硬編碼「豆花」（除非預設路線敘述）
- [ ] 取名後用 `dogLabel`／正確代詞
- [ ] 狗年齡與行為合齡（見 reference）
- [ ] 主人班表與 `DEMO_DAY_CALENDAR` 一致
- [ ] 相簿 desc 與當時是否已取名一致

### 2. 測試路線（交 game-tester 執行）

1. 自訂名「小安」+ female → Day3 抽查
2. 預設豆花 + male → 存檔 JSON 驗證
3. 跳關 Day8 HUD／字幕仍正確

### 3. 自動化輔助

```powershell
cd Learn_How_To_Love\Ch1_Trust\game
node tools\tw-locale-pass.js
rg "豆花|小布丁" js\scenes.js js\choice-reactions.js
```

## 常見問題 → 負責 agent

| 問題 | 級別 | 轉交 |
|------|------|------|
| 取名前出現自訂狗名 | P1 | story / tw-narrative-voice |
| 性別與代詞不符 | P1 | tw-narrative-voice |
| choice-reactions 寫死名字 | P1 | branch-engine |
| 狗年齡行為不合理 | P1 | story-narrative |
| pose 與情緒相反 | P1 | visual-art |
| 上班日無理由在家 | P1 | story-narrative |

## 角色審查輸出模板

```markdown
## 角色審查：[週／場景範圍]

### 主人
- [ ] 班表 [ ] 第一次養寵語氣 [ ] 視角「你」

### 狗
- [ ] 年齡感 [ ] 代詞／名字 [ ] 行為合齡

### 跨 surface
- [ ] scenes [ ] choice-reactions [ ] 相簿 [ ] HUD

### 問題清單
| 位置 | 問題 | 級別 | 轉交 |
```

## 權責邊界

- 不新增場景或分支（story-narrative／branch-engine）。
- 不修改 PNG（visual-art）。
- 衝突時：**guide_line > 本 skill reference > visual-art 外型細節**。

## 參考

- 完整設定表：[`reference.md`](reference.md)
- 視覺外型：[`lhtl-visual-art/reference.md`](../lhtl-visual-art/reference.md)
- 測試清單：[`character-consistency.md`](../game-tester/character-consistency.md)
