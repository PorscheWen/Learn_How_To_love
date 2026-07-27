# tester｜插圖重疊檢查報告

- **範圍：** Ch1 Trust Version3 Ren'Py（S01～S10 全段立繪位置／大小）
- **依據：** `agents/tester.md` §6.3
- **方法：** 重產後 content bbox 重算 `DOG_POSE_SCALE`＋transform 對齊＋1280×720 合成預覽
- **日期：** 2026-07-25（狗／人物全量重產後全段重調）

---

## 總評

| 級 | 場景 | 現象 | 狀態 |
|----|------|------|------|
| **P1** | 全段狗圖 | 重產後 h_fill 大變，舊 scale 使站姿過小／臥姿失控 | **已修** 依 bbox 重算 18 個 `DOG_POSE_SCALE` |
| **P1** | S06 頂額 | `forehead_nudge` 自帶小腿＋予安立繪 → 雙腿 | **已修** 隱藏 yuan，改用 `dog_nudge` |
| **P1** | S06／S09 人狗同框 | 左右間距需重對齊新畫幅 | **已修** pair／walk／entrance／char 全套 |
| **P2** | 字幕切爪 | ypos 0.85 部分 pose 貼框 | **已修** 統一 ypos 0.86～0.87；solo cover≈0% |
| — | 兩人同框（店員／鄰居／同事） | 左右分開 | OK（overlap 0%） |

---

## 已改檔

| 檔案 | 變更 |
|------|------|
| `Renpy_game/game/script.rpy` | `DOG_POSE_SCALE` 全表；char／dog transforms；新增 `dog_nudge`；S06 頂額 hide yuan |
| `tools/recalibrate_sprites.py` | 新增：目標高度→scale＋pair 預覽 |
| `tools/check_overlap.py` | 與 script 同步；xalign 改中心對齊模型 |
| `Renpy_game/tools/overlap-previews/*.jpg` | 重產預覽 |

### Transform 摘要（1280×720）

| Transform | xalign | ypos | zoom | 用途 |
|-----------|--------|------|------|------|
| `char_left`／`char_right` | 0.26／0.74 | 0.86 | 0.45 | 兩人同框 |
| `dog_far`／`mid`／`near` | 0.58／0.50／0.42 | 0.86 | 0.26／0.30／0.34 | 單狗距離 |
| `dog_*_pair` | 0.50／0.56／0.60 | 0.86 | 0.22～0.24 | 人右狗左 |
| `dog_nudge` | 0.68 | 0.86 | 0.28 | 頂額單圖 |
| `dog_entrance_*` | 0.50／0.54 | 0.87 | 0.24／0.27 | 玄關地墊 |
| `*_walk` | 人 0.74／狗 0.30～0.50 | 0.86 | — | S08 巷口 |

站姿 near≈200px、臥姿 near≈150px（內容高度）。

---

## 靜態檢查結果（2026-07-25）

```text
S02 相遇／靠近、S01 店員、S05 耳機、S06 兩人／躲腿／擋人、S08 散步、S09 兩人／拒絕／玄關 → OK
字幕 cover：抽樣 dog solo 皆 ≤1%
```

重跑：

```powershell
cd Ch1_Trust_Version3
python tools/recalibrate_sprites.py
python tools/check_overlap.py
```

## 實機再確認

1. S02：人右狗左／中，不糊臉、不切字幕  
2. S06：躲腿在予安左側小腿；頂額只見單圖小腿＋狗  
3. S08：牽繩人右、狗在左～中隨信任靠近  
4. S09：同事左、予安右；拒絕時狗貼予安腳邊、不蓋同事臉  
5. S03／S08 玄關：狗在地墊，不進門板  

預覽：`Renpy_game/tools/overlap-previews/S0*.jpg`

---

*對齊：`agents/tester.md` §6.3｜`image_dog.md`／`image_char.md` 重產後*
