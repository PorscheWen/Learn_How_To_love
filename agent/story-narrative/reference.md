# 故事架構參考

## 主角（「你」）— Ch1 鎖定

| 項目 | 規格 |
|------|------|
| 年齡 | **25 歲** |
| 性別／外型 | **年輕長髮女性** |
| 職業 | **上班族**（Demo：可請假、需打卡） |
| 寵物經驗 | **第一次養寵物**——會慌、會查手機、會問店員／獸醫 |
| 性格 | **感情豐富**——易共感、內疚、對小動作敏感 |
| 敘事 | 第二人稱「你」；固定女主 |
| 視覺 | Demo 不露全臉；見 [`visual-art/reference.md`](../visual-art/reference.md#角色外型聖經) |

## 主人作息（Ch1 鎖定 — 審查必對）

| 項目 | 規格 |
|------|------|
| 上班日 | **週一～週五** |
| 上班時間 | **08:00–17:00** |
| 休息日 | **週六、週日** |
| 例外 | **請假／提早離開**（需劇情或 `flags` 明示） |

### Demo 故事天 ↔ 星期

| 故事天 | 星期 | 班表 | 敘事重點 |
|--------|------|------|----------|
| Day 1 | 週三 | 下班後 | 雨天相遇、第一夜 |
| Day 2 | 週四 | **請假** | 寵物店、取名、第一次進食 |
| Day 3 | 週五 | 上班 | 分離焦慮、提早回家、尿墊之夜 |
| Day 4 | 週六 | 放假 | 修復線（可選）、寵物醫院 |
| Day 5 | 週日 | 放假 | 懷裡認家 |
| Day 6 | 週一 | 上班 | 傍晚雷雨（條件觸發） |
| Day 7 | 週二 | 上班 | 難過的一天、Epilogue |

程式：`Demo/js/systems.js` → `DEMO_DAY_CALENDAR`、`isOwnerOnLeave()`、`ownerShouldBeHome()`。

審查：上班日 08:00–17:00 主人應在公司或通勤，除非 `onLeave`／`day3LeftEarly` 等 flag。

---

## Demo Ch1 敘事弧線（七天）

| 天 | 主題句 | 關鍵 Memory／事件 |
|----|--------|-------------------|
| 1 | 還不會，但願意帶回家 | `prologue_rain`、`first_night` |
| 2 | 養不只是浪漫，是每天 | `day2_petshop`、`dog_named`、`day2_first_meal` |
| 3 | 愛有時是提早回家 | `door_wait`、`potty_night`、`knee` |
| 4 | 責任也排進生活 | `vet_visit` |
| 5 | 家變成你們的 | `home_scent` |
| 6 | 普通的一天很難得 | `thunder`（條件） |
| 7 | 一次次選擇留下來 | `sad_day` → Epilogue |

語調潤飾以 Day 1（`prologue_rain`～`prologue_dawn`）為金標，見 [`tw-narrative-voice`](../tw-narrative-voice/SKILL.md)。

---

## Demo Ch1 場景一覽

| Day | scene_id | 摘要 |
|-----|----------|------|
| 1 | `prologue_rain` | 雨天紙箱相遇 |
| 1 | `prologue_home` | 帶回家、狼狽 |
| 1 | `prologue_dry` | 浴室吹乾 |
| 1 | `prologue_night` | 第一夜哀鳴 |
| 1 | `prologue_dawn` | 天亮 |
| 2 | `day2_empty`～`day2_evening` | 請假、店、取名、進食、午後聲音 |
| 3 | `day3_morning`～`day3_night_after` | 上班、離家、提早回、如廁、尿墊之夜 |
| 4 | `day4_repair`～`day4_evening` | 修復（可選）、週六獸醫 |
| 5 | `day5_sunday`～`day5_evening` | 週日認家 |
| 6 | `day6_morning`～`day6_thunder_after` | 週一上班、雷雨分支 |
| 7 | `day7_morning`～`day7_moment` | 加班、難過 |
| 7 | `epilogue` | 七天總結 |

完整 id 列表見 `Demo/js/scenes.js` 的 `SCENES` 物件。

---

## 條件分支 text 與編輯器

以下 8 場 `text` 依 `flags`／小遊戲結果組句；`game_editor.html` 拆成**多欄**編輯（非「僅預覽」）：

| scene_id | 分支依據 | editor 子欄（摘要） |
|----------|----------|---------------------|
| `day2_petshop_after` | `shopTier`、`dryGentle` | 開頭、溫柔句、店員三評、結尾 |
| `day2_return` | `dogGender` | 店員弟／妹回應、進門主文 |
| `day3_leave_early` | `day3AskedLeave` | 有請假／沒解釋開場、回家路 |
| `day4_vet_intake` | `vetFormDetail` | 詳填／簡填、診間頭尾 |
| `day4_vet` | `vetIntakeTier` | 三種醫師開場、檢查主文 |
| `day4_vet_bill` | `vetTier` | 結帳說明、頭尾 |
| `day5_home_after` | `homeExploreTier` | 認家佳績／部分／較少 |
| `day6_thunder_after` | `thunderComfortTier` | 雷雨後四種結語 |

其餘場景：`text` 為字串或 `(s) => \`模板\``，editor **單欄**可改。

**新增分支場景時：** 在場景包寫清各分支句；落地後於 `game_editor.html` 的 `COMPLEX_TEXT` 登記子欄（或暫用「進階函式」整段編輯）。

---

## 小遊戲 ↔ flags ↔ 敘事

| minigame | 觸發場景 | 結果 flag | 影響敘事 |
|----------|----------|-----------|----------|
| `shop` | `day2_petshop` | `shopTier` | `day2_petshop_after` 店員評價句 |
| `potty` | `day3_potty_intro` | `pottyGuideTier` | `resolvePottyAfternoonCopy`（systems 流程） |
| `vet` | `day4_vet` | `vetTier`、`vetIntakeTier` | `day4_vet_bill`、結帳文案 |
| `home` | `day5_home_intro` | `homeExploreTier` | `day5_home_after` 全文 |
| `thunder` | `day6_thunder` | `thunderComfortTier` | `day6_thunder_after` |
| `walk` | （支線預留） | `walkGuideTier` | 公園文案 |

結果文案檔：`Demo/js/minigame-reactions.js`（`resultLine`、`reactionLine`）。  
撰寫新小遊戲時：場景包須列 **tier 差異一句** + 對應 flag 名。

---

## game_editor 欄位對照

| UI 欄位 | 寫入檔案 | 備註 |
|---------|----------|------|
| 主敘事 text | `scenes.js` | 含條件分支子欄 |
| 副標 sub | `scenes.js` | |
| 氣味 smell | `scenes.js` | 字串 |
| 氣味追加 smellAdd | `scenes.js` | 字串或陣列（頓號分隔編輯） |
| 選項 | `scenes.js` | 變更時同步 reaction key |
| 選項反應 | `choice-reactions.js` | key = `sceneId::選項原文` |
| 小遊戲結果 | `minigame-reactions.js` | |
| 相簿 title／desc | `systems.js` `ALBUM_ENTRIES` | |

預覽預設：狗名豆花、妹妹；匯出時還原 `${dogLabel(s)}`、`${dogPronoun(s)}`。

啟動：`Demo/啟動編輯器.bat`（port 8765）；勿用 `file://` 開啟。

---

## 相簿 ALBUM_ENTRIES（Demo Ch1 主線）

| memory_id | 標題方向 |
|-----------|----------|
| `prologue_rain` | 雨天相遇 |
| `first_night` | 第一夜 |
| `day2_petshop` | 寵物店 |
| `dog_named` | 取名 |
| `day2_first_meal` | 第一次自己吃 |
| `door_wait` | 門口等待 |
| `potty_guide` / `potty_night` / `knee` | 如廁、尿墊之夜、靠膝 |
| `vet_visit` | 寵物醫院 |
| `home_scent` | 家的氣味 |
| `thunder` | 雷雨 |
| `sad_day` | 難過的那一天 |

新增 Memory 時：場景包標 `memory_id`，並提供相簿 `title`／`desc` 草稿。

---

## 三部曲速查

| 篇章 | 主題 | 基調 | 玩法重心 |
|------|------|------|----------|
| Ch1 First Steps | 信任 | 暖、有笑 | 教、防禍、如廁／社會化 |
| Ch2 Still Here | 日常 | 靜、小確幸 | 默契、家庭變化 |
| Ch3 Goodbye | 告別 | 克制、尊嚴 | 照護、三條終局主線 |

## Feelings（12）— 敘事觸發用

Anxious、Excited、Content、Curious、Hurt、Attached、Sleepy、Playful、Alert、Shy、Hungry、Angry

寫作時用**行為**（夾尾、踱步、靠膝），不用數字面板。

## Bond 五階

1. Stranger → 2. Familiar → 3. Rhythm → 4. Anchor → 5. One Life

Demo 結束目標：Lv2 Familiar。

## 各章 Landmark / Memory 範例（guide_line §6.4）

### First Steps

| 事件 | 觸發 | 跨作 |
|------|------|------|
| 第一次跟回家 | Bond Lv2 + 連續安撫 Anxious | 第三部同路走很慢 |
| 尿墊之夜 | 選不罵、清理、陪坐 | 解鎖靠膝 |
| 雷雨 | Anxious 高 + Bond ≥ Lv2 | `afraidOfThunder` |
| 走失與找回 | 主線 + Bond 高/低分支 | 第二部信任支線 |

### Still Here / Goodbye

見 `guide_line.md` §6.4。

## 開場／結尾文案（草案）

**Ch1 開場：**
> 你還不知道怎麼愛一個生命。牠也不知道怎麼相信一個人。這沒關係。你們可以一起學。

**Ch3 結尾：**
> 你終於學會了。不是學會失去——是學會，愛過之後還在。

**Demo Epilogue 方向：**
> 不是一次做對，而是一次次，選擇留下來。

## 參考基調作品

Spiritfarer、A Short Hike、To the Moon、Farewell North、My Little Puppy（避死後大冒險）
