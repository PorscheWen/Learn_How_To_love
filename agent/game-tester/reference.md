# 遊戲測試參考（台灣玩家）

> **Playable：`Ch1_Trust/Renpy_game/`**（主）。舊 HTML `Ch1_Trust/game/tools/` 僅對照。  
> **Steam 電子小說玩家視角：** [`steam-vn-players.md`](steam-vn-players.md)  
> **取名／狗與主人／展現一致：** [`character-consistency.md`](character-consistency.md)  
> **時間流動／身心變化：** [`time-flow-effects.md`](time-flow-effects.md)

## Ren'Py 視覺與字幕鎖定

> 對應 `game/definitions.rpy`、`game/week1.rpy`、`game/gui.rpy`（CJK = SourceHanSansLite）  
> 審計：`python tools/audit-font-glyphs.py`、`python tools/game-tester-visual-audit.py`

### Transform（1280×720）

| Transform | 用途 | 規格（鎖定） |
|-----------|------|----------------|
| `dog_bottom` | 僅狗在場 | `xalign 0.5`、`ypos 0.93`、`yanchor 1.0`、**zoom 0.24** |
| `dog_with_npc` | 狗＋店員／醫師同場 | `xalign 0.10`（左下）、**zoom 0.20** |
| `scene_art_fit` | NPC／帳單插圖 | `xalign 0.62`、`yalign 0.28`、**zoom 0.38** |

原圖多為 1536×1024；zoom 過大會蓋字幕、與 scene_art 中段重疊（曾測：scene 底≈495、dog 頂≈341 → **P1**）。

### show／hide 規則

| 場景類型 | 必做 |
|----------|------|
| 寵物店／結帳／診間／帳單（僅 NPC 圖） | **`hide dog`** + `show scene_art …` |
| 獸醫櫃檯／責任書（懷裡有狗＋櫃檯圖） | `show dog … at dog_with_npc` + `show scene_art …` |
| 一般居家／街道僅狗 | `show dog … at dog_bottom` + **`hide scene_art`** |
| 從有狗場切到無狗場 | 必須 `hide dog`，否則上一場狗殘留疊圖 |

### 字型缺字（會顯示成 X／方框）

SourceHanSansLite **沒有**：

| Codepoint | 勿用 | 改用 |
|-----------|------|------|
| U+00B7 | 間隔點（中點） | `｜`（U+FF5C）或 `・`（U+30FB） |
| U+25B8 | 小三角前綴 | `▶`（U+25B6） |
| U+2726 | 四角星裝飾 | `＊`（U+FF0A）或拿掉 |

**有字可用：** `……` `—` `「」` `，。` `→` `▶` `｜` `・`

### 字幕怪字紅旗（P1）

- `牠 `／` 牠` 異常空格（像缺字）
- 對白混用 ASCII `...` 與 `……`（統一全形省略）
- 大陸用字殘留：柜台→**櫃檯**、里／面／发 等（見 tw-narrative-voice）

### Ren'Py 手動必測（視覺）

| 跳關 | 預期畫面 |
|------|----------|
| Day2 寵物店 | 僅店員／結帳圖，**無狗疊圖** |
| Day4 櫃檯／責任書 | 狗在**左下**，人物插圖在右上，不互蓋 |
| Day1 對白 | 無 X 方框、無「牠 」空格、省略號為 …… |

## 自動化腳本

| 腳本 | 指令 | 通過條件 |
|------|------|----------|
| **字型缺字** | `cd Ch1_Trust/Renpy_game` → `python tools/audit-font-glyphs.py` | quoted 字串無缺字（BOM 可忽略） |
| **視覺估算** | `python tools/game-tester-visual-audit.py` | Missing glyphs PASS；尺寸與 definitions 一致 |
| Week1 流程（HTML） | `node tools/test-week1-flow.js` | 舊 HTML 對照用 |
| 選項反應（HTML） | `node tools/validate-choice-reactions.js` | OK: all choices mapped |
| 繁體掃描（HTML） | `node tools/tw-locale-pass.js` | 無簡化殘留 |

`test-week1-flow.js`（HTML）另驗證：Day 2 寵物店 → naming；Day 4 掛號 → responsibility_sign → 診間。Ren'Py 對應用章節跳關手動驗。

## Ch1 第一週手動路線（主線）

| Day | 必測場景 | 玩家在意 |
|-----|----------|----------|
| 1 | `prologue_rain`～`prologue_dawn` | 語調金標、雨夜圖、不卡住 |
| 2 | `day2_petshop`、取名、探索 | 店內無狗圖、小遊戲、責任書**不在**此日；**取名→性別→回家**代詞一致 |
| 3 | `day3_homecoming`、`day3_slipper`、尿墊 | 提早回家動機、靠膝 Memory |
| 4 | `day4_responsibility_sign`、獸醫 | 責任書在醫院、帳單文案 |
| 5 | `day5_home_intro` 小遊戲 | 認家 tier 與相簿 |
| 6 | 雷雨／靜日分支 | 條件合理、不強迫雷雨 |
| 7 | `day7_moment`、`week1_epilogue` | 結語字幕、Bond Lv2 |

## Ch1 第二週手動路線（Week2）

| Day | 必測場景 | 玩家在意 |
|-----|----------|----------|
| 8 | `week2_intro`、`week2_neighbor`、`week2_neighbor_after` | 晨→傍晚；鄰居腳步、三選 socialization |
| 9 | `week2_calendar` | **週四晚上**行事曆；刪聚會／固定遛狗 |
| 10 | `week2_friday_morning`、`week2_elevator_dog`、`week2_elevator_after` | **週五早晨**；阿黃、硬拉分支、`socialTier` |
| 11–12 | `week2_camera_roll`、`week2_sock_snatch` | 相簿、襪子玩鬧 |
| 13 | `week2_park_tree`、`week2_park_play`（需 close tier） | Landmark 樹、阿黃公園 |
| 13–14 | `week2_dryer_truce`、`week2_no_bite` | **Day1 吹風機 callback**、bite 與 Day3 拖鞋弧 |
| 14 | `week2_epilogue` | 第二週結語、Landmark  gentle_rules |

**Week2 視覺／音效必查：** `hallway_neighbor`、`elevator` 背景；專用 pose 非別名；16 場皆有 `SCENE_CUES`。

## Ch1 第三週手動路線（Week3）

| Day | 必測場景 | 玩家在意 |
|-----|----------|----------|
| 15 | `week3_rainy_commute`、`week3_delivery_bark` | 笑點（外賣）、雨天想回家 |
| 16 | `week3_door_ajar`、`week3_lost_panic`、`week3_lost_found` | **Landmark 走失**；親自找到 vs 鄰居協助 |
| 18 | `week3_tail_chase` | 豆豆、走失後第一笑 |
| 19 | `week3_fever_vet`、`week3_zoom_cameo` | 獸醫 callback、視訊入鏡 |
| 20–21 | `week3_leash_tangle`、`week3_recovery_knee` | 阿黃牽繩、病後靠膝 |
| 21 | `week3_epilogue` | 第三週結語、預告房東線 |

**Week3 分支必測：** 低 Trust 走鄰居協助找回；`neighborMet`＋敲鄰居門路線。

## 場景視覺對照表（審查用）

填寫時對照 `Ch1_Trust/game/js/scenes.js`：

| scene_id | location | dogPose | sceneArt | hideDog | 玩家預期畫面 | 結果 OK? |
|----------|----------|---------|----------|---------|--------------|----------|
| （範例）`day2_petshop` | pet_shop | — | petshop-clerk | 否 | 店員圖、無狗 | |

**常見錯誤：**

- `location: pet_shop` 卻顯示客廳狗 pose
- `hideDog: true` 仍顯示狗圖
- `sceneArt` PNG 缺失 → 破圖或空白
- 新週 **故事 pose** 仍用 `DOG_POSE_ASSET` 別名（P2 → visual-art 補專用 PNG）
- `location` 在 `locations.js` 有定義但 `style.css` 無 `.loc-*` → 背景 fallback 錯誤（P1）

資產路徑：`assets/dog/Week0/dog-{pose}.png`（Week3+ → `Week3/`）、`assets/scene/scene-{sceneArt}.png`、`assets/bg/`（見 `locations.js`）。

## 字幕繁體檢查

### 必查檔案

`scenes.js`、`choice-reactions.js`、`minigame-reactions.js`、`systems.js`（`ALBUM_ENTRIES`）、`game.js`（小遊戲 UI）、`index.html`

### 快速人工規則

| 通過 | 不通過 |
|------|--------|
| 繁體、全形標點為主 | 簡體字、大陆用语 |
| 台灣：影片、品質、軟體、資訊、第一天／第一週 | 视频、质量、软件、信息、Day1、Week2 |
| 寵物、牠／他／她一致 | 取名後仍全用「牠」指名後的狗 |
| 遊戲化數字不進字幕 | 「Trust +20」類文案 |

### 邏輯斷裂紅旗

- 上一場「深夜」，下一場無過場變「清晨上班」卻無 `day` 標籤更新
- 請假日（Day 2）出現「主管催報告進會議」
- 獸醫場景 `text` 內字面 `${dogLabel(s)}` 未替換（單引號字串 bug）
- `text: () =>` 使用 `dogPronoun(s)` 等但未接收 `s`

## 角色與展現一致性

完整清單見 [`character-consistency.md`](character-consistency.md)。每輪 playtest **必做**：

1. **取名路線 ×2**：自訂名＋female、預設名（豆花）＋male
2. **時間線**：`day2_return` 前無自訂名；之後字幕用 `dogLabel`／他或她
3. **狗／主人**：混種幼犬 PNG 連貫；「你」為新手飼主；上班班表合理
4. **展現**：HUD 地點 = `location`；相簿 title 與 Memory 劇情一致；存檔 JSON `dogName`／`dogGender` 正確
5. **NPC 狗**：阿黃等稱呼跨場一致

### 快速掃描（可選）

```powershell
rg "豆花|小布丁" js/scenes.js js/choice-reactions.js   # 硬編碼名字
rg "dogLabel|dogPronoun" js/choice-reactions.js          # 應用函式而非寫死
```

## 時間流動與身心變化

完整規格見 [`time-flow-effects.md`](time-flow-effects.md)。每輪 playtest **建議至少 1 條 callback 路線**：

| 路線 | 驗什麼 |
|------|--------|
| Day1 吹風機溫柔 → Week2 `week2_dryer_truce` | `dryGentle` 文案／心理差異 |
| Week2 電梯 socialTier → `week2_park_play` | 關係累積解鎖 |
| Week1 Bond Lv2 → Week2 intro | 基調從「帶回家」→「一起面對外界」 |
| 低 Trust 線（吼叫／硬拉）→ 後段 | 修復窗口或變體，非 reset |

**Ch1 幼犬段：** 全程 2–4 個月→週年約 1 歲；**勿**過早 aging 視覺。Ch2/3 見 time-flow §五。

## 玩家能力／可及性（輕量）

| 項目 | 預期 |
|------|------|
| 推進 | 空白鍵／點字幕加速；breath 空檔可快進 |
| 撫摸 | breath 階段、情緒允許時可拖曳狗圖 |
| 存檔 | 💾 匯出 JSON；重新整理可繼續（localStorage） |
| 音訊 | 🎵 可關；無素材時不應整頁崩潰 |
| 開發選單 | 跳 Day／結語不破壞 `state` |

## 測試報告模板

```markdown
# LHTL 測試報告 — [範圍，例 Ch1 Week1]

**日期：** YYYY-MM-DD  
**環境：** Ch1_Trust/Renpy_game  
**自動化：** audit-font-glyphs [PASS/FAIL] · game-tester-visual-audit [PASS/FAIL]

## 摘要
- 結論：PASS / FAIL（P0=n, P1=n, P2=n）
- 建議優先：[…]

## 問題清單

### P0 — 阻塞
| # | scene_id | 重現 | 預期 | 實際 | 負責 |
|---|----------|------|------|------|------|

### P1 — 嚴重
| # | scene_id | … |

**台灣口語對白（2026-07）：** 人對狗安撫句過短（「在。」「好。」）→ 交 tw-narrative-voice；宜 ≥4 字（「我在這」「好喔，再玩一下」）。詳 `.cursor/skills/lhtl-tw-narrative-voice/reference.md` §人對狗對白句長。

### P2 — 建議
| # | scene_id | … |

## 視覺抽樣（圖文相符）
- [ ] day2_petshop — …
- [ ] day4_responsibility_sign — …

## 已驗主線分支
- [ ] 尿墊溫柔線
- [ ] 尿墊吼叫 → day4_repair
- [ ] Day6 靜日 / 雷雨

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

## 時間流動與身心變化
| 維度 | 結果 | 備註 |
|------|------|------|
| 日／週過場合理 | ✅／⚠️／❌ | |
| 狗行為隨 Trust/Bond 演進 | ✅／⚠️／❌ | |
| 主人新手→默契弧 | ✅／⚠️／❌ | |
| 外部事件 callback | ✅／⚠️／❌ | |
| flags 影響後續 | ✅／⚠️／❌ | |
| 無「Day1 重播」感 | ✅／⚠️／❌ | |

## Steam 敘事體驗（玩家視角）
| 維度 | 評價 | 備註 |
|------|------|------|
| 開場 hook（前 15 min） | ✅／⚠️／❌ | |
| 選擇回聲感 | ✅／⚠️／❌ | |
| 節奏 | ✅／⚠️／❌ | |
| 基調誠實 | ✅／⚠️／❌ | |
| 台灣繁中／口語 | ✅／⚠️／❌ | |
| **時間弧／成長感** | ✅／⚠️／❌ | 玩得越久越像真的在一起過日子 |

**模擬 Steam 評論：** 好評一句／差評一句
```

（Steam 維度細項見 [`steam-vn-players.md`](steam-vn-players.md) §6。）

## 與製作流程的銜接

```
story / visual / audio 落地
       ↓
game-tester（本 skill）→ 報告
       ↓
各 agent 修復 → 再跑 test-week1-flow + 受影響路線
```

發布前 Ch1 第一週建議：**自動化全綠 + 至少 1 次完整手動主線 + 2 條主要分支**。
