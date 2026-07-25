# tester｜插圖重疊檢查報告

- **範圍：** Ch1 Trust Version3 Ren'Py（重點 S03 玄關、S05～S09 人狗同框）
- **依據：** `agents/tester.md` §6.3
- **方法：** 資產 alpha 稽核＋1280×720 合成預覽＋劇本 show／transform 對照
- **日期：** 2026-07-24（同日已依報告修改落地）

---

## 總評

| 級 | 場景 | 現象 | 狀態 |
|----|------|------|------|
| **P1** | S06／S09 人狗同框 | `dog_*_pair` 舊值貼左側鄰居 | **已修** pair → 0.48／0.54／0.60 |
| **P1** | S06 `dog-behind-legs` | 懸空＋pose 不像躲腿 | **已修** 重產 peek／躲藏全身＋去背＋右下對齊 |
| **P1** | S09 refuse | 仍有一處 `dog_mid` 浮在兩人中間 | **已修** → `dog_mid_pair` |
| **P2** | S03 玄關 | 狗略貼門板 | **已修** `dog_entrance_*` |
| **P2** | stair-watch 等近黑邊 | 可選清邊 | 暫留；核心毛色勿誤刪 |
| — | 字幕切臉／雙狗／zorder | — | OK |

---

## 已改檔

- `Renpy_game/game/script.rpy`：pair／entrance transform；S03 玄關；S09 全數 `*_pair`
- `assets/dog/dog-behind-legs.png`：新 pose（備份 `dog-behind-legs.bak.png`）

## 實機再確認

1. S06：狗在予安右側小腿一帶，不蓋鄰居臉  
2. S03 玄關：狗在地墊  
3. S09：拒絕時狗靠予安側  

預覽：`Renpy_game/tools/overlap-previews/s06_behind_legs_FINAL.jpg`、`s03_entrance_FINAL.jpg`

---

*對齊：`agents/tester.md` §6.3*
