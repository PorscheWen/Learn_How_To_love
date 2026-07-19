# 角色與展現一致性審查

> game-tester 專用。審查**取名／代詞／性別**、**狗與主人設定**、**場景用途與 UI 展現**是否前後一致。  
> 設定權威：[`visual-art/reference.md`](../visual-art/reference.md#角色外型聖經)、[`story-narrative/reference.md`](../story-narrative/reference.md#主角你ch1-鎖定)、[`tw-narrative-voice`](../tw-narrative-voice/SKILL.md)。

---

## 一、取名與代詞（必測）

### 程式契約（`systems.js`）

| 函式 | 行為 |
|------|------|
| `dogLabel(s)` | 有名字 → 名字；無名字 → `dogPronoun(s)`（預設「牠」） |
| `dogPronoun(s)` | `female`→她、`male`→他、未設→牠 |
| `applyDogPronouns(text, s)` | 取名+性別後，文案內「牠／牠的」→ 他／她／他的／她的 |
| `hasDogName(s)` | `dogName` 非空 |
| `setDogProfile` | Day2 `day2_naming`／`day2_gender` 後寫入 `dogName`、`dogGender`、`flags.dogNamed` |

### 時間線錨點

| 階段 | scene 範例 | 字幕預期 |
|------|------------|----------|
| **取名前** | `prologue_*`～`day2_petshop` | 指狗用 **「牠」**；不出現玩家自訂名；`dogLabel` 顯示為「牠」 |
| **取名中** | `day2_naming`（`namePrompt`） | UI 輸入名；空則預設「豆花」 |
| **性別** | `day2_gender`（`genderPrompt`） | 店員問「{名字} 是弟弟還是妹妹？」 |
| **取名後** | `day2_return` 起 | 主文用 **`${dogLabel(s)}`**；敘事代詞用 **`${dogPronoun(s)}`** 或 `applyDogPronouns` |
| **全章** | Week2+ | 不再退回全「牠」指已命名的狗（除非 flashback 刻意） |

### 手動測試路線（至少 2 組）

1. **自訂名 + 妹妹**：取名「小安」→ 性別 female → 玩到 Day3，抽查 3 場字幕是否為「小安／她」
2. **預設名 + 弟弟**：取名留空（豆花）→ male → 存檔匯出 JSON，確認 `dogName`、`dogGender`
3. **跳關回歸**：開發選單跳 Day 8，HUD／字幕仍為存檔內名字與代詞

### 常見問題 → 嚴重度

| 問題 | 級別 | 負責 |
|------|------|------|
| `day2_return` 前字幕出現自訂狗名 | P1 | story / tw-narrative-voice |
| 取名後仍全文「牠」指這隻狗（未用名字） | P2 | tw-narrative-voice |
| 性別 female 卻寫「他」 | P1 | tw-narrative-voice |
| 硬編碼「豆花」而玩家取名為其他 | P1 | story（改為 `dogLabel(s)`） |
| `choice-reactions` 寫死名字 | P1 | story |
| 單引號 `text: '...${dogLabel(s)}...'` 未替換 | P0 | story |
| 相簿／Memory 標題與當時是否已取名不符 | P2 | story / tw-narrative-voice |

### 自動化輔助

```powershell
# 取名前場景不應含玩家才會輸入的名字（需人工確認自訂名測試）
node tools/test-week1-flow.js   # text 解析含 mockState 取名
rg "豆花|小布丁" Ch1_Trust/game/js/scenes.js   # 硬編碼名字掃描
rg "dogLabel|dogPronoun|applyDogPronouns" Ch1_Trust/game/js/choice-reactions.js
```

---

## 二、狗狗角色一致性

### 敘事＋視覺鎖定（Ch1）

| 項目 | 規格 | 測什麼 |
|------|------|--------|
| 身份 | **全系列同一隻**混種幼犬 | 文案不寫成不同品種；相簿不像換狗 |
| 年齡 | Ch1：**2–4 個月** | 不寫「成年犬」「老狗」（Ch3 前） |
| 毛色／體型 | golden-tan、honey ochre、小、腿短 | PNG 非柯基／柴犬感；pose 不突然變大 |
| 多狗 | 主角狗 + **狗友 companion** | 阿黃用 `companion-dog-img`；主角仍 `dog-img` 單獨 |
| 情緒 | `feeling` ↔ 文案 ↔ `dogPose` | Alert 場卻 content 圖；playful � hurt pose |

### NPC 狗（跨場一致）

| ID | 名字 | 首次 | 後續須一致 |
|----|------|------|------------|
| `ah_huang` | 阿黃 | `week2_elevator_dog` | `week2_park_play`、`week3_leash_tangle`、相簿、`dogFriends` |

**阿黃 companion 視覺：** `assets/dog/companions/ah-huang/`（sit、sniff-greet、play、leash）· 場景 `companionDog` · 驗證 `validate-companion-ah-huang.js`

### 常見問題

| 問題 | 級別 | 負責 |
|------|------|------|
| 狗 pose 與字幕情緒相反 | P1 | visual-art / story |
| 品種感突變（像換了一隻） | P1 | visual-art |
| `DOG_POSES` behavior 與 `.dog-behavior` 不同步 | P2 | story / visual-art |

---

## 三、主人（「你」）一致性

### 敘事鎖定

| 項目 | 規格 |
|------|------|
| 視角 | 第二人稱 **「你」** |
| 年齡／身份 | **25 歲**上班族；**第一次養寵物** |
| 性格 | 感情豐富、會慌、願意學；非訓練師口吻 |
| 班表 | 週一～五上班；請假／週末在家（`DEMO_DAY_CALENDAR`） |

### 視覺鎖定（含 pose 局部）

| 項目 | 規格 |
|------|------|
| 呈現 | **不露全臉**、無全立繪 |
| 服裝 | 米白、燕麦、灰褐、深棕；無 Logo |
| `knee`／靠腿 | **僅大腿／膝上**；無小腿、腳、鞋 |
| `held` | 臂彎＋袖口即可 |

### 常見問題

| 問題 | 級別 | 負責 |
|------|------|------|
| 上班日無理由全天在家敘事 | P1 | story-narrative |
| 文案像資深飼主（Day1–2 過度專業） | P2 | tw-narrative-voice |
| pose 圖露出主人全臉或錯誤性別暗示 | P1 | visual-art |
| `knee` 構圖露出腳踝／鞋 | P1 | visual-art |

---

## 四、場景用途與展現一致

### 場景欄位 ↔ 畫面 ↔ 音訊

| 欄位 | 一致規則 |
|------|----------|
| `location` | HUD 地點 label、`style.css` `.loc-*` 背景、氣味 `smell` 同空間 |
| `dogPose` | 與 `resolveDogVisual` 檔名一致；`hideDog` 時不顯示狗圖 |
| `sceneArt` | 店員／獸醫只在該 NPC 場；`noSceneArt` 不誤顯示 |
| `feeling` | `#app` cold／content 色溫大致合理 |
| `music` | BGM profile 不與基調衝突（例：鄰居警戒可用 `night`） |
| `noDogAudio`／`pet_shop` | 無狗在場不狗叫 |

### 跨 surface 對照

| Surface | 須與誰一致 |
|---------|------------|
| `ALBUM_ENTRIES` title／desc | 解鎖 Memory 當下劇情、取名前後語氣 |
| `choice-reactions` text | 同場選項、`dogLabel`／代詞 |
| `minigame-reactions` | tier 結果與 `flags`、後續 `text` 分支 |
| Epilogue 統計 | 「相簿／羈絆」文案；**無** Trust 數字 |
| 存檔 JSON | `dogName`、`dogGender`、`memories`、`flags` 與遊戲內一致 |

---

## 五、審查表（報告用）

每輪 playtest 至少勾一列 **取名路線** + 全章抽樣：

```markdown
## 角色與展現一致性

| 維度 | 結果 | 備註 |
|------|------|------|
| 取名前「牠」 | ✅／⚠️／❌ | |
| 取名後名字＋他／她 | ✅／⚠️／❌ | 測試名：＿＿ |
| 狗外型／pose 連貫 | ✅／⚠️／❌ | |
| 主人「你」＋新手飼主感 | ✅／⚠️／❌ | |
| 地點／HUD／背景 | ✅／⚠️／❌ | |
| 相簿／Memory 文案 | ✅／⚠️／❌ | |
| 存檔匯出再載入 | ✅／⚠️／❌ | |
| NPC（阿黃等）稱呼 | ✅／⚠️／❌ | |
```

**⚠️** = P2 建議；**❌** = P1 起，須標 scene_id 與負責 agent。

時間流動（Trust/Bond、callback、跨週基調）：見 [`time-flow-effects.md`](time-flow-effects.md)。

---

## 六、與其他 agent 分工

| 不一致類型 | 轉交 |
|------------|------|
| 取名時序、分支、Memory 邏輯 | story-narrative |
| 代詞、名字、台灣口吻 | tw-narrative-voice |
| 狗／主人 PNG、背景、pose | visual-art |
| 有狗卻無聲／無狗卻亂叫 | audio-sound |
