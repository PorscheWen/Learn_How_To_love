# 故事架構參考

> **Steam 上架（敘事門檻）：** [`steam-release.md`](steam-release.md)（對照 `guide_line.md` §十）  
> **Ch1 正式版全章總覽：** [`Ch1_Trust/Ch1_guide_line.md`](../../Ch1_Trust/Ch1_guide_line.md)  
> **Ch1 第一週場景架構（57 節點）：** [`Ch1_Trust/Ch1_week1_architecture.md`](../../Ch1_Trust/Ch1_week1_architecture.md)  
> **Ch1 第二週場景架構（16 節點）：** [`Ch1_Trust/Ch1_week2_architecture.md`](../../Ch1_Trust/Ch1_week2_architecture.md)  
> **章節落地驗收（game-tester 反饋）：** [`chapter-landing-checklist.md`](../chapter-landing-checklist.md)  
> **Ch1 敘事節奏修訂（2026-07）：** [`narrative-pacing-revision.md`](../narrative-pacing-revision.md)

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

## 狗狗年齡（全系列 · 時間線鎖定 — 審查必對）

> 權威：`guide_line.md` §四–§六、[`Ch1_guide_line.md`](../../Ch1_Trust/Ch1_guide_line.md) §七時間線、[`time-flow-effects.md`](../game-tester/time-flow-effects.md) §二。  
> 美術 prompt／PNG tier 細節交 [`visual-art/reference.md`](../visual-art/reference.md#角色外型聖經)；本節管**敘事合理性、文案暗示、行為可否**。

### 三部曲生命階段

| 篇章 | 生命階段 | 狗年齡（敘事） |
|------|----------|----------------|
| **Ch1 First Steps** | 幼犬（0–2 歲段） | 相遇 **2–4 個月** → 週年 **約 1 歲** |
| **Ch2 Still Here** | 中年 | 穩重成犬（具體歲數 Ch2 大綱鎖定） |
| **Ch3 Goodbye** | 老犬 | **9 歲+**；灰吻、動作慢、感官敘事 |

**全系列同一隻混種狗**；Ch1 不得換品種、不得突然老犬化（灰吻等留 Ch3）。

### Ch1 細時間軸（故事日 ↔ 狗年齡）

| 故事日 | 狗年齡 | 敘事／行為合理範圍 | 視覺 tier |
|--------|--------|-------------------|-----------|
| **Day 1** 雨天相遇（`prologue_rain`） | **約 3 個月**（官方 2–4 月；**相遇宜偏 3 月**） | 紙箱裡細小發抖、眼神無助、控 bladder 差、易驚、不能獨太久 | Week0 |
| **Day 1–14**（第 1–2 週） | 仍 **~3 月** | 如廁仍在學、分離焦慮、社會化皆「第一次」 | Week0 |
| **Day 15+**（第 3 週起） | **4–5 月**（敘事「悄悄長大」） | `week3_growth_notice`：項圈多一格、膝邊略高；仍幼犬、仍衝動 | Week3 adolescent PNG |
| **Day 16–28**（走失、房東） | 4–5 月 | 已認家、會開門縫，但非成犬穩定 | Week3 |
| **Day 365** 相遇週年 | **~12 個月（1 歲）** | 比相遇大一圈、仍活潑；**仍屬 Ch1 幼犬段**，非 Ch2 中年 | 週年場景（若有專用 pose） |

**時間壓縮備註：** Ch1 前 28 天僅曆 **4 週**，生理上狗不會長大很多；Week3「長大」以**感受＋略長高**演出，週年弧才快轉至 1 歲。撰寫時勿讓 Day 3 文案像 6 個月幼犬，亦勿讓 Day 28 像成犬。

### 製作基準（與 visual-art 對齊）

| 用途 | 建議鎖定 |
|------|----------|
| 情緒基準 `dog-anxious.png`、Week0 多數 pose | **3 個月** |
| Day 1 序章無助／被遺棄（`box`、`anxious`） | **2.5–3 個月**（宜小、腿短、肚圓） |
| Week3+ 成長圖（`assets/dog/Week3/`） | **4–5 個月** adolescent |
| Day 365 週年 | **12 個月** |

### 敘事審查：合理 vs 要報

| 時段 | 合理 | 不合理（違規） |
|------|------|----------------|
| Day 1–3 | 小、易累、尿墊、蜷縮、不敢靠近 | 像成犬穩定、長時間獨處無焦慮 |
| Week2 | 電梯／公園／鄰居是「第一次」試探 | 像社會化老手、無鋪墊就淡定 |
| Week3 走失 | 認家、會開門縫，仍幼犬衝動 | 完全不懂家界線（若已有認家 Memory） |
| Day 365 | 大一圈、仍 golden-tan 同一隻 | 突然灰吻、老犬步態、換品種感 |
| Ch1 全章 | 文案用「小傢伙」「還在學」 | 寫「成年犬」「老狗」「很大隻了」（週年前） |

### 場景包必填

撰寫或審查場景時，在場景包標註：

- **狗年齡感：** 對照上表（例：Day 1 → ~3 月；Week3 intro → 4–5 月）
- **身體語言是否合齡：** 控尿、體力、社會化經驗
- **dogPose tier：** Week0 或 Week3（Day 15+ 預設 Week3 成長圖）

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

## Ch1 第一週場景一覽

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
| 7 | `week1_epilogue` | 第一週總結 |

完整 id 列表見 `Demo/js/scenes.js` 的 `SCENES` 物件。  
**Ch1 全章**（含 W2–週年弧）見 [`Ch1_guide_line.md`](../../Ch1_Trust/Ch1_guide_line.md) §全章總覽表。

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
| `shop` | `day2_petshop` | `shopTier`、`shopShampooOk` | `day2_petshop_after` 店員評價句；`day2_bath` 沐浴精來源 |
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

撰寫新章節大綱時：場景包標 `memory_id`，並提供相簿 `title`／`desc` 草稿。整章須維護全章總覽表，見 [`steam-release.md`](steam-release.md)。

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

Demo 第一週結束目標：Lv2 Familiar。Ch1 全章終局：週年弧後 Bond Lv3+、Landmark `meetiversary`。

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

**Ch1 第一週收束：**
> 不是一次做對，而是一次次，選擇留下來。

**Ch1 週年終局（範例）：**
> 你們還在學，但這一年已經很滿了。

## 參考基調作品

Spiritfarer、A Short Hike、To the Moon、Farewell North、My Little Puppy（避死後大冒險）
