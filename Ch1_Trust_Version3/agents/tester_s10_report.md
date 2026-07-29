# Tester 報告｜Section 10／四結局

> 日期：2026-07-28  
> 範圍：`section_10_share_the_key`＋結局 A～D＋`endings.rpy` 節拍／解鎖  
> 方法：自動化腳本＋靜態對照 `tester.md` §3 · `game_guild.md` §3 · `section_10_share_the_key.md`（未開實機）

---

## 自動化結果

| 腳本 | 結果 |
|------|------|
| `python Renpy_game/tools/validate-s01.py` | **OK**（結構／flags／trust／結局解鎖） |
| `python Renpy_game/tools/validate-reading-time.py` | **OK**（S10-A～D 皆 ≥5；注意：此腳本會把 if/else 雙分支字數加總，偏鬆） |
| `python Renpy_game/tools/validate-s10.py` | **OK**（單一路徑閱讀時間＋路由真值表＋coda） |
| `python Renpy_game/tools/validate-menus.py` | **OK**（結局後 aftercare／一覽出口） |

### 單一路徑閱讀時間（`validate-s10.py`）

| 路線 | 估算 | 門檻 | 判定 |
|------|------|------|------|
| S10-A | 5.00 分 | ≥5 | **通過**（貼門檻） |
| S10-B | 5.39 分 | ≥5 | **通過** |
| S10-C | 5.14 分 | ≥5 | **通過**（本次補兩段空屋敘事後達標） |
| S10-D | 5.37 分 | ≥5 | **通過** |

---

## 契約對照（程式面）

| 項目 | 預期 | 程式狀態 | 判定 |
|------|------|----------|------|
| S10 不改 trust／三軸 | 只讀既有結果 | 無 `trust +=`／`-=` | **通過** |
| C 優先 | `gave_away` → C，不受 trust | if 最前＋`jump ending_ch1_handed_over` | **通過** |
| A | trust≥10、留下、非硬拖 | `trust >= 10 and not s08_forced_walk` | **通過** |
| B | 4～9；或高信任硬拖 | `elif trust >= 4`（含硬拖回落） | **通過** |
| D | ≤3 留下 | else → thin_ice | **通過** |
| 硬拖回聲 | S10 掛勾＋結局 B 睡姿 | 兩處皆有 `s08_forced_walk` | **通過** |
| 睡姿 | A near／B mid／D far；C 無狗 | pose 對齊；C 敘事無 `show dog` | **通過** |
| 共通句 | 「晚上見」；A／B／D「再試一年」 | 齊 | **通過** |
| 禁止 | 無衰老／安樂／Game Over／親密％ | 掃描無命中 | **通過** |
| 解鎖／軌跡 | process_ending_unlock＋record_trust_trajectory | 四結局皆有；`time.time()`／`or []` 防呆 | **通過** |
| 節拍收束 | coda → 標題 → 解鎖 → aftercare | `ending_coda_finish` 四路接入 | **通過** |
| landmark | 高信任送走酸感 | S09 寫入＋結局 C 變體 | **通過** |

### 路由真值表（10 案）

| trust | gave_away | s08_forced_walk | 預期 |
|------:|:---------:|:---------------:|:----:|
| 12 | N | N | A |
| 10 | N | N | A |
| 12 | N | Y | B |
| 9／4 | N | N | B |
| 3／0 | N | N | D |
| 12／0／7 | Y | * | C |

全部 **通過**。

---

## 本次測試中已修

| 級 | 問題 | 處理 |
|----|------|------|
| **P1** | 單一路徑估算 S10-C 僅 4.81 分（&lt;5） | 於送走空屋段補兩句有事件的敘事（玄關空弧、外套抓痕朝外），達 5.14 分 |
| **P2** | `validate-reading-time.py` 對 S10 if/else 雙計 | 新增 `validate-s10.py` 做單一路徑估算；舊腳本仍可用但偏鬆 |

---

## 待實機確認（非自動可關）

| 級 | 場景 | 現象／風險 | 預期 | 建議 |
|----|------|------------|------|------|
| **P2** | 結局節拍 | ATL 距離動畫缺圖時 fallback 色塊是否突兀 | 安靜、可略過、不搶敘事 | 實機 Ctrl／點擊略過四結局各一次 |
| **P2** | 結局 C 節拍 | `ending_c_photo_card` 純文字卡 | 有「照片感」、畫面無狗 | 實機看 2～3 秒停留 |
| **P2** | 解鎖提示 | `ending_unlock_notice` 與 aftercare 銜接 | 不蓋住情緒、可點繼續 | 打完任一結局看流程 |
| **P2** | S10-A | 文字時間貼 5.00 分 | 實機一般閱讀仍 ≥5 | 慢讀一輪 A；若偏短再補物證句 |
| — | 資產 | `images/` 可能未進此工作複本 | pose／bg 正常顯示 | 有資產的建置再跑視覺 |

**本次靜態審查：無 P0；P1 閱讀時間已修；剩餘為實機視覺／節奏 P2。**

---

## 建議手動路線（最短驗收）

1. **A**：高信任＋S08 不停等硬拖＋S09 留下 → 背靠睡＋紀念照解鎖  
2. **B（硬拖）**：高信任但 S08 硬拖＋留下 → 不得進 A；B 有「走太快」回聲  
3. **C**：任意信任 S09 送走 → 空屋、無狗 SFX、不羞辱；高信任另看 landmark 酸感  
4. **D**：trust≤3 仍留下 → 門邊睡、薄冰誠實  

每條：節拍可略過 → 標題卡 → 解鎖提示 → aftercare 選單。

---

## 結論

S10／四結局在**路由、契約、解鎖、節拍接入、單一路徑 ≥5 分**上自動化皆通過。實機請抽測四條結局的節拍與解鎖 UI；若要代開遊戲點路線，說一聲即可。

### 驗證指令

```powershell
cd Ch1_Trust_Version3\Renpy_game
python tools\validate-s01.py
python tools\validate-reading-time.py
python tools\validate-s10.py
```
