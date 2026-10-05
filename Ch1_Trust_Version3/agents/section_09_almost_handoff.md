# Section 09｜差點交給別人

> 對齊：`game_guild.md` · `outline_trilogy_ch1_10sections.md` · `image_dog.md` · `image_char.md`  
> 定位：Ch1 情緒高峰與唯一「留下／送走」硬分歧；同事真誠，不是搶狗的反派。
> 最短路徑閱讀約**八分鐘**；篇幅增加用於交接準備、等待與選擇後回聲，不新增第二組信任選項。

## 章節契約

| 項目 | 鎖定 |
|------|------|
| 一件事 | 同事提出接手，予安帶小7到咖啡廳門口交接 |
| 核心軸 | Guard（誰站在牠這邊） |
| 信任選擇 | 留下 `trust +2 / guard +2`；送走 `trust -2 / guard -2` |
| G2 | `trust ≥ 5` 或曾受保護時，小7會貼腳／低鳴；低信任只會僵住，不替任何一方表態 |
| 硬分歧 | 留下寫 `s09_stayed = true`、`gave_away = false`；送走反之 |
| Landmark | 高信任仍送走可寫 `landmark_chose_reason_over_bond` |
| BGM | `almost_gave`（`tense.ogg` 原曲）→ 留下 `tender`／送走 `ending_handover` |
| 鉤子 | 所有路徑都進 S10；S10 依留下與分數落到 A～D |
| 敘述 | 對齊 S01；旁白不說「性質完全不同」，用門把、紙袋、牽繩帶過 |
| 篇幅 | 最短選項路徑約 **2,000 字／八分鐘** |

**章節選擇摘要：** 同事真誠提出接手；交繩前，她得承認誰已經選過誰。

## 敘事節拍

1. 同事在茶水間再次提出接手：有經驗、住處較大、白天有人，也願意慢慢來。
2. 三天思考具體落地為花費清單、加班通知、照片與疫苗資料；理性理由必須真的成立。
3. 週六客廳：分裝飼料、折舊外套——**先打包（`home_stand`＋遠狗）**，臨走前才告別跪姿（無牽繩），再進玄關扣帶。
4. 玄關：胸背帶＋牽繩（對齊 entrance 門框）；高信任貼腳、低信任停門線／鞋櫃邊。
5. 咖啡廳門口：同事提早抵達、蹲側讓狗聞；三人在騎樓維持距離。
6. 高信任小7貼予安腳邊並對伸手低鳴；低信任僵在兩人之間，不把沉默當同意。
7. 姓名欄與狗先看向誰，讓予安承認「被認得」不是「我總做對」。
8. **選擇前承認「我也會累」**：刮椅＋「找的是誰」為唯一停拍；內心一句即可。送走選項必須合理，留下選項才更重；不說教。
9. 玩家決定收回牽繩，或照原先安排交出去；兩路都需演完實際回程／離場。

## 選擇演出

### 留下

- 予安承認：「我不是比較會。我只是想繼續學。」
- 同事不鼓掌也不生氣，只承諾需要時可以幫忙。
- 小7不必立刻搖尾巴；鼻尖碰鞋、肩膀放鬆即可。低信任留下：先在 `mid` 停一拍，再貼鞋。
- **接觸體感（一句）：** 牽繩重新繞回手腕，一圈都沒少——那重量比紙袋輕，卻佔滿袖口。
- **回憶：** 這一句疊在握繩特寫上，解鎖 `leash_grip`／`gallery/secret-leash-grip.png`。不進結局 A 整組。
- 進 S10 後依 `trust` 與 `s08_forced_walk` 判定 A／B／D。

### 送走

- 予安逐項交代怕機車聲、喝水急、門要留縫。
- 高信任可低鳴；低信任只在兩人之間僵住。
- `entry_trust ≥ 7` → `landmark_chose_reason_over_bond`：交接當下＋結局 C 強調「關係最好時放手」。
- 敘事必須承認「有理由，也仍然會痛」，不得責罵玩家。
- **接觸體感（一句）：** 最後一圈卡在袖口；放進同事手裡之後，臂彎空了，袖口那圈還熱著。畫面：`leash_pass` 與鬆圈同拍（hide 同事），無字拍內再切交繩特寫，再切回空袖口。
- **回憶：** 無字拍內解鎖 `leash_handover`／`gallery/secret-leash-handover.png`。不進結局 A 整組。
- 進 S10 結局 C；不是 Game Over。
- 兩路都**不重寫**毛色、長髮、疲憊五官；立繪負責長相。

## 美術

### 背景

| 節拍 | bg |
|------|-----|
| 茶水間／思考 | `bg-office-night.png` |
| 三晚想清單 | `bg-living-night.png` |
| 週六客廳打包／告別 | `bg-living-day.png` |
| 玄關扣帶出門 | `bg-entrance-day.png` |
| 咖啡廳門口交接 | `bg-cafe-day.png` |

### 人物／狗（專用立繪 · 2026-07-28）

| 節拍 | 人物 | 狗 | 備註 |
|------|------|-----|------|
| 茶水間 | `char-yuan-headphones`＋`char-coworker` | — | 兩人對談 |
| 三晚想清單 | `char-yuan-home-sit`＠`char_chair` | `parallel`＠落地窗門邊，面向右椅 | **右木凳**；不疊左沙發 |
| 客廳打包 | `char-yuan-home-stand` | `dog-parallel` | 室內站＋遠狗；**不新產** |
| 客廳告別 | `char-yuan-farewell` | `dog-farewell` | **無牽繩**；互相面對；臨走前才切 |
| 玄關聞紙袋 | `char-yuan-leash` | `dog-paper-bag-sniff` | 重用；不新產 |
| 玄關扣帶 | `char-yuan-leash` | `dog-leash-wait` | 高信任 `near` 貼腳；低信任 `far` 門線；SCALE entrance |
| 咖啡廳 | 進場 `coworker stand`＋`yuan cafe`；蹲下才 `coworker cafe`；收回手時 `yuan leash`；站起來回 `stand`；送走後 `yuan squat_side`（無繩） | 見下 | 動作跟旁白換；不新產 |

| 咖啡廳狗 pose | 檔名 | 劇情朝向 |
|---------------|------|----------|
| 高信任拒絕 | `dog-cafe-refuse` | 貼予安腳邊，**面向同事**（警告）→ `dog_cafe_near_guard` |
| 低信任僵住 | `dog-cafe-tense` | 兩人中間，**面向予安**（找妳）→ `dog_cafe_mid` |
| 留下後 | `dog-cafe-refuse` | 貼鞋側，**面向予安**→ `dog_cafe_near_home` |
| 送走（高／低） | refuse／tense | 中間拉扯或無人跟 → `dog_cafe_mid` |

舊檔 `dog-refuse-stranger`／`dog-street-tense` 仍可作 fallback；S09 正式演出用 cafe 專用圖。

### 朝向／位置準則（劇情優先）

| 場 | 朝向 | Transform（摘要） |
|----|------|-------------------|
| 客廳告別 | 圖檔予安面**左**、狗抬頭偏左；畫面予安左／狗右 → **翻予安**後對望 | `char_right_farewell` 0.40／人 0.36；`dog_farewell_near` 0.62／狗 0.139 |
| 玄關 | 予安蹲姿→左；狗 leash-wait→右 | `char_right_s09` 人 **0.33**；狗 **0.128**；far **0.60**／mid **0.66**／near **0.70**；高信任貼腳 near、低信任門線 far |
| 咖啡廳人物 | 同事蹲左→右；予安站右→左 | `char_*_cafe` 人 **0.36** |
| 拒絕 | 狗貼腳、面向同事 | `dog_cafe_near_guard`（狗 0.139，翻轉） |
| 僵住／交繩 | 狗在中間、面向予安 | `dog_cafe_mid` 狗 0.139 |
| 留下 | 狗貼鞋、面向予安 | `dog_cafe_near_home` 狗 0.139 |

**原則：** 人／狗朝向以當下劇情＋**實際圖檔面相**為準；翻轉時 `zoom 1.0` + `xzoom`／`yzoom` 同絕對值。S09 立繪見 `scale.rpy` 的 `SCALE`。

- **落地畫面（2026-10-03）：** 狗跟旁白走，**不新產 pose**。茶水間無狗。思考夜予安坐右木凳（`home_sit`＠`char_chair`），狗在落地窗門邊面向她。週六先 `home_stand`＋遠狗打包，臨走前才 `farewell`。咖啡廳：先站、再蹲、伸手靠近、收回時予安改蹲握繩；留下後同事站起；送走後予安改無繩蹲姿。兩張牽繩回憶多停一拍。玄關尺同 S08：人 `leash` **0.33**×pose **0.70**／狗 **0.128**；遠近只改 xalign（far **0.60**／mid **0.66**／near **0.70**）。客廳告別狗 **0.139**；咖啡廳狗 **0.139**。舊檔 `refuse-stranger`／`street_tense` 僅 fallback。第三晚只旁白點到「靠著鞋睡著的那張臉」，**不** overlay 鞋邊照（圖只在 S08 尾）。

## 驗證

- 留下／送走都能正常進 S10。
- 改名後全段使用 `[dog_label]`，不可寫死「小7」。
- 同事始終有禮、真誠，不用反派語氣。
- `trust` 結尾夾在 0～12。
- `python Renpy_game/tools/validate-s01.py` 須含 `show dog cafe_refuse at dog_cafe_near_guard`。
- 交繩／留下各最多一句體感（手腕重量或臂彎空了）；不補外型清單。對齊 gamer 閱讀原則。
- 週六 `farewell` 須在「臨走前」之後；送走 `leash_pass` 須在「放進同事手裡」之前。

### 旁白 × 狗移動（2026-09-19 鎖定｜不新產 pose）

遠近只用具名 transform（玄關 far **0.60**／mid **0.66**／near **0.70**）；**禁**新 PNG。舊檔 `refuse-stranger`／`street_tense` 僅 fallback。

| 旁白拍 | pose | 位置 | SFX |
|--------|------|------|-----|
| 茶水間（無狗） | — | — | — |
| 第二晚門邊抬頭 | `parallel` | 落地窗門邊，面向右椅 | — |
| 週六打包 | `parallel` | `dog_far` | — |
| 臨走前告別（無牽繩） | `farewell` | `dog_farewell_near` | — |
| 玄關開場 | `leash_wait` | `dog_entrance_far_s09` | — |
| 高信任聞紙袋、卡在人與袋中間 | `paper_bag` | far | — |
| 高信任扣帶後貼腳 | `leash_wait` | `dog_entrance_near_s09` | — |
| 低信任盯紙袋 | `paper_bag` | far | — |
| 低信任扣帶後停門線 | `leash_wait` | far | — |
| 咖啡廳高信任貼鞋、低鳴 | 先 `cafe_tense` 走到同事手前聞兩下，再 `cafe_refuse` 退回 `dog_cafe_near_guard`；伸手後 `window hide` 再旁白 | `growl` |
| 咖啡廳低信任僵在中間 | `cafe_tense` | `dog_cafe_mid`；伸手後 `window hide` 再旁白 | `murmur` |
| 留下後（高信任） | `cafe_refuse` | `dog_cafe_near_home` | `soft` |
| 留下後（低信任） | `cafe_tense`→`cafe_refuse` | mid 停一拍→`near_home` | `soft` |
| 送走（高信任） | `cafe_refuse` | `dog_cafe_mid` | — |
| 送走（低信任） | `cafe_tense` | `dog_cafe_mid` | — |

第三晚若已解鎖鞋邊回憶：旁白可點到「靠著鞋睡著的那張臉」，**不要**再 overlay `secret-shoe-sleep.png`（那張圖只在 S08 返家／週一手機）。

留下／送走的牽繩特寫只用 `secret-leash-grip.png`／`secret-leash-handover.png`，各解鎖一次。

---

*更新：2026-09-20｜第三晚不再 overlay 鞋邊睡圖；圖只在 S08 尾*
