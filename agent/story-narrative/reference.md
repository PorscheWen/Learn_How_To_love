# 故事架構參考

## 主角（「你」）— Ch1 鎖定

| 項目 | 規格 |
|------|------|
| 年齡 | **25 歲** |
| 性別／外型 | **年輕長髮女性** |
| 職業 | **上班族**（Demo：可請假、需打卡） |
| 寵物經驗 | **第一次養寵物**——會慌、會查手機、會問店員／獸醫，但不代表不愛 |
| 性格 | **感情豐富**——易共感、內心戲多、做錯會內疚、對小動作很敏感 |
| 敘事 | 第二人稱「你」；**固定女主**，勿寫成中性或男性視角 |
| 視覺 | Demo 不露全臉；細規見 [`visual-art/reference.md`](../visual-art/reference.md#角色外型聖經) |

**寫作提示：** 她的軟弱（著急、自責）與溫柔（願意等、願意學）並存；催淚來自「第一次」而非狗血。

## 主人作息（Ch1 鎖定 — 審查必對）

| 項目 | 規格 |
|------|------|
| 上班日 | **週一～週五** |
| 上班時間 | **08:00–17:00**（八點前出門、五點下班為基準） |
| 休息日 | **週六、週日**（不用上班、不用打卡） |
| 例外 | **僅限刻意請假／提早離開**（需劇情或 `flags` 明示，不可無故白天在家） |

### Demo Ch1 故事天 ↔ 星期

| 故事天 | 星期 | 班表 | 備註 |
|--------|------|------|------|
| Day 1 | 週三 | 下班後 | 傍晚上班後帶回家 |
| Day 2 | 週四 | **請假** | 寵物店、取名 |
| Day 3 | 週五 | 上班 | 08:00–17:00；可提早離開（`day3LeftEarly`） |
| Day 4 | 週六 | 放假 | 寵物醫院 |
| Day 5 | 週日 | 放假 | 懷裡認家 |
| Day 6 | 週一 | 上班 | 早晨出門；**傍晚**回家後雷雨 |
| Day 7 | 週二 | 上班 | 可寫「比平常晚回家」（仍屬下班後） |

### 審查：行為 vs 班表

撰寫或修改場景前，對照 `Demo/js/systems.js` 的 `DEMO_DAY_CALENDAR`、`ownerShouldBeHome()`：

- **上班日 08:00–17:00**：主人應在**公司**（`location: office`）或通勤途中——**不可**寫在家泡茶、週末慢活，除非 `onLeave`／`day3LeftEarly` 等請假旗標。
- **上班日早晨**：可寫出門前、鬧鐘、八點前要出門。
- **上班日傍晚**：五點後可寫回家、門口、陪狗（Day 6 雷雨、Day 7 難過）。
- **週六日**：不可寫「得上班」「打卡」；可寫鬧鐘沒響、週末、不用出門（除約好的外出如醫院）。
- **請假**：Day 2 整日請假；Day 3 需選項或 flag 明示提早離開。

程式對照：`OWNER_WORK_START_HOUR`、`OWNER_WORK_END_HOUR`、`isOwnerOnLeave(state, day)`。

## 三部曲速查

| 篇章 | 主題 | 基調 | 玩法重心 |
|------|------|------|----------|
| Ch1 First Steps | 信任 | 暖、有笑 | 教、防禍、如廁／社會化 |
| Ch2 Still Here | 日常 | 靜、小確幸 | 默契、家庭變化、被忽略後再看見 |
| Ch3 Goodbye | 告別 | 克制、尊嚴 | 照護、氣味記憶、三條終局主線 |

## Feelings（12）— 敘事觸發用

Anxious、Excited、Content、Curious、Hurt、Attached、Sleepy、Playful、Alert、Shy、Hungry、Angry

敘事寫作時用**行為描述**（夾尾、踱步、靠膝），不用數字面板。

## Bond 五階

1. Stranger → 2. Familiar → 3. Rhythm → 4. Anchor → 5. One Life

Demo 結束目標：Lv2 Familiar。

## 各章 Landmark / Memory 範例（guide_line §6.4）

### First Steps

| 事件 | 觸發 | 跨作 |
|------|------|------|
| 第一次跟回家 | Bond Lv2 + 連續安撫 Anxious | 第三部同路走很慢 |
| 尿墊之夜 | 選不罵、清理、陪坐 | 解鎖靠膝 |
| 雷雨 | Anxious 高 + Bond ≥ Lv2 | afraidOfThunder |
| 走失與找回 | 主線 + Bond 高/低分支 | 第二部信任支線 |

### Still Here

| 事件 | 觸發 | 跨作 |
|------|------|------|
| 被忽略的一週 | 連續忽略 Attached | 修復線 or 缺席版 |
| 寶寶來了 | 主線 + Curious/Anxious | 守嬰兒房 |
| 老媽的散步 | Bond Lv4 + Content | 第三部樹下駐足 |
| 吵架之後 | Attached 高 | Landmark：叼拖鞋 |

### Goodbye

| 事件 | 觸發 | 跨作 |
|------|------|------|
| 氣味博物館 | Bond Lv5 + Landmark ≥2 | 個人化閃回 |
| 最後一次最愛的事 | Comfort 中 + Attached | epilogue |
| 還在的早晨 | 終局前 + Bond Lv5 | 告別平靜度 |
| 你學會了 | 通關 | 全系列徽章 |

## Demo 場景 ID 對照（scenes.js）

Day 1 閃回 → Day 3–7 室內／戶外 → Epilogue。改動時保持 `scene_id` 穩定，供 audio `SCENE_CUES` 引用。

## 開場／結尾文案（草案）

**Ch1 開場：**
> 你還不知道怎麼愛一個生命。牠也不知道怎麼相信一個人。這沒關係。你們可以一起學。

**Ch3 結尾：**
> 你終於學會了。不是學會失去——是學會，愛過之後還在。

## 參考基調作品

Spiritfarer（告別尊嚴）、A Short Hike（日常）、To the Moon（記憶）、Farewell North（克制）、My Little Puppy（老犬溫度，避死後大冒險）
