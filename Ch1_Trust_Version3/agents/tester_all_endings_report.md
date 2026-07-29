# Tester 報告｜四結局完整驗收

> 日期：2026-07-28  
> 範圍：結局 A～D（路由／敘事／節拍／解鎖／aftercare／結局一覽）  
> 方法：自動化＋Ren'Py lint（**未開實機逐條點完**）

---

## 總評

**靜態／自動化：四結局皆正常，無 P0／P1。**  
剩餘為實機視覺與節奏 P2。

---

## 自動化結果

| 腳本 | 結果 |
|------|------|
| `python tools/validate-s01.py` | **OK** |
| `python tools/validate-reading-time.py` | **OK**（S10-A～D ≥5） |
| `python tools/validate-s10.py` | **OK**（單一路徑閱讀＋路由） |
| `python tools/validate-all-endings.py` | **OK**（解鎖對齊／coda／aftercare） |
| `python tools/validate-menus.py` | **OK**（結局一覽／隱藏／aftercare 出口） |
| `python tools/validate-menu-layout.py` | **OK**（結局／隱藏 side／viewport 不擠返回） |
| `renpy.exe . lint` | **OK**（無錯誤輸出；696 dialogue blocks） |

### 單一路徑閱讀時間

| 路線 | 分 | 判定 |
|------|-----|------|
| A | 5.00 | OK（貼門檻） |
| B | 5.39 | OK |
| C | 5.14 | OK |
| D | 5.37 | OK |

---

## 四結局檢查表

| 項目 | A 背靠 | B 選定 | C 送走 | D 薄冰 |
|------|:------:|:------:|:------:|:------:|
| 可達（路由條件） | ✓ | ✓ | ✓ | ✓ |
| `ch1_ending` 寫入 | ✓ | ✓ | ✓ | ✓ |
| `process_ending_unlock` | ✓ | ✓ | ✓ | ✓ |
| `record_trust_trajectory` | ✓ | ✓ | ✓ | ✓ |
| 節拍 `ending_beat_*` | ✓ | ✓ | ✓（無狗） | ✓ |
| 標題卡＋解鎖提示 | ✓ | ✓ | ✓ | ✓ |
| → `ending_aftercare` | ✓ | ✓ | ✓ | ✓ |
| 睡姿／距離 | near 背睡 | mid 確認 | 空屋 | far 門邊 |
| 硬拖不得進 A／進 B | — | ✓ | — | — |
| C 優先於 trust | — | — | ✓ | — |
| 隱藏三層（日記／心境／朋友） | ✓ | ✓ | ✓ | ✓ |
| 紀念照 | lap＋背靠 | — | — | — |
| 結局靜幀 gallery | ✓ | ✓ | ✓ | ✓ |
| 無 Game Over／羞辱／衰老 | ✓ | ✓ | ✓ | ✓ |

### 路由抽樣（真值表）

| 條件 | 結局 |
|------|------|
| trust 10～12、留下、非硬拖 | **A** |
| trust 4～9 留下；或高信任＋硬拖 | **B** |
| S09 送走（任意 trust） | **C** |
| trust ≤3 留下 | **D** |

---

## 解鎖對齊（提示 ≠ 空頭支票）

每結局 `process_ending_unlock` 實際寫入：

- 共通：`dog_diary_*`／`character_aftercare_*`／`friend_perspective_*`
- 僅 A：`lap_sleep`、`back_to_back` 照、`ch2_trust_foundation_hint`

與 `hidden_content.rpy` 目錄、`ending_unlock_notice` 文案、結局一覽靜幀 **一致**。

---

## 待實機（P2）

| 項目 | 說明 |
|------|------|
| 四結局節拍 | 點擊／Ctrl 略過、距離 ATL、缺圖 fallback |
| C 照片文字卡 | 空屋無狗、不播狗 SFX |
| 解鎖彈窗 → aftercare | 不蓋情緒、可回主選單看隱藏庫 |
| A 貼 5.00 分 | 慢讀一輪確認體感仍夠 |
| gallery 圖檔 | 若 `images/gallery/` 未齊，靜幀可能色塊 fallback |

### 建議手動四條

1. **A**：高信任＋S08 不硬拖＋留下  
2. **B 硬拖**：高信任＋S08 硬拖＋留下（不得進 A）  
3. **C**：任意路徑送走  
4. **D**：低信任仍留下  

每條確認：節拍 → 標題 → 解鎖清單 → aftercare → 主選單「結局一覽／隱藏內容」。

---

## 結論

**四結局在程式契約與自動化驗收下皆正常可達、可收束、可解鎖。**  
未代開遊戲實點；若要實機代測四條，說一聲即可。

```powershell
cd Ch1_Trust_Version3\Renpy_game
python tools\validate-all-endings.py
python tools\validate-s10.py
python tools\validate-menus.py
python tools\validate-menu-layout.py
.\tools\renpy-sdk\renpy.exe . lint
```

選單細節見 `tester_menus_report.md`。
