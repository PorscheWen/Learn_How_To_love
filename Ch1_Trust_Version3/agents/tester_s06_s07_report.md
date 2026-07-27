# Tester 報告｜S06／S07 近期變更確認

> 日期：2026-07-27  
> 範圍：走廊靜音＋進門玄關、S07 單軌 BGM、S06 擋人／躲身後立繪  
> 方法：自動化腳本＋靜態對照 `tester.md`（未開實機）

---

## 自動化結果

| 腳本 | 結果 |
|------|------|
| `python Renpy_game/tools/validate-s01.py` | **OK**（結構／flags／trust／結局解鎖） |
| `python Renpy_game/tools/validate-reading-time.py` | **OK**（S06 5.09 分、S07 5.16 分；皆 ≥5） |
| `tools/check_overlap.py` | **缺檔**（無法自動重疊驗收） |

### 關鍵資產存在

corridor-day／entrance-day／living-night、char-yuan-block／neighbor、dog-behind-legs／forehead-nudge／guard-door、sick-guard.ogg／tender.ogg、gallery/secret-lap-sleep.png → **皆存在**

---

## 契約對照（程式面）

| 項目 | 預期 | 程式狀態 | 判定 |
|------|------|----------|------|
| S06 開場音樂 | 無 BGM | `music.stop`＋`_current_bgm = None` | **通過** |
| S06 進門背景 | 屋內玄關 | `scene bg entrance_day`（非 living_day） | **通過** |
| S06 進門後音樂 | `tender` | 進門後 `play_bgm("tender")` | **通過** |
| S06 擋人朝向 | 予安朝左對鄰居 | `char-yuan-block` 面向左；鄰居左／予安右 | **通過（待實機看疊圖）** |
| S06 狗躲身後 | `dog_behind_pair`＋先狗後人 | 有；xalign≈0.82 | **通過（待實機）** |
| S06 Guard ± | +2／−2／−1 | 三選項齊 | **通過** |
| S07 開場音樂 | `sick_guard` | 僅此一處 `play_bgm` | **通過** |
| S07 後段切曲 | 不要切換 | 已移除 tender／tense | **通過** |
| S07 Tone ± | +2／−2 | 仍在 | **通過** |
| S06→S07 jump | 不斷 | `jump section_07_sick_guard` | **通過** |

---

## 待實機確認（非自動可關）

| 級 | 場景 | 現象／風險 | 預期 | 建議 |
|----|------|------------|------|------|
| **P2** | S06 開場～選前 | `yuan commute` 多半朝右，鄰居在左，擋人前視線可能「背對威脅」 | 擋人前也可感對峙，或接受過渡姿 | 實機看；若違和交 visual-art 產朝左 commute／側身 |
| **P2** | S06 擋人 | `dog_behind_pair` 偏右緣，窄螢幕可能裁半隻狗 | 狗露頭在腿後、不貼鄰居 | 實機 1280×720／1920×1080；必要時調 xalign |
| **P2** | S06 頂額 | 進門改玄關後，`dog_nudge` 是否仍對齊鞋櫃／門線 | 單圖小腿、無雙腿疊影 | 護衛線重玩頂額一段 |
| **P2** | S06→S07 | 玄關 tender → 病守 sick_guard 淡入是否突兀 | 情緒可接、不跳針 | 聽感；必要時加長 fade |
| — | 重疊工具 | `check_overlap.py`／`recalibrate_sprites.py` 路徑未在 Renpy_game/tools | 重產後可跑 | 確認 tools 位置或補連結 |

**本次靜態審查：無 P0／P1 邏輯斷裂。**

---

## 建議手動路線（最短驗收）

1. 章節選單 → **S06**  
   - 走廊應無 BGM  
   - 選「往前半步擋住」→ 予安朝左擋、狗在身後  
   - 進門 → **玄關 day**＋`tender`  
   - 頂額：只見 nudge 圖、無雙腿  
2. 接 **S07**  
   - 開場 `sick_guard`  
   - 分別抽「我還在」「吵死了」→ **BGM 不應換曲**  
   - bark 只一次  
3. 回歸：S06「塞回屋」「讓摸」各一次，確認仍進得了 S07、trust 方向正確  

---

## 結論

近期 S06／S07 音景與進門背景契約，**自動化與靜態對照皆通過**。剩餘為**實機視覺／聽感 P2**（立繪朝向過渡、狗右緣裁切、頂額對齊、曲目銜接）。若要我開遊戲代點上述三條路線，說一聲即可。
