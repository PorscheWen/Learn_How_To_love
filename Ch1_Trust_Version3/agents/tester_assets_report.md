# Tester 報告｜全遊戲線圖片與音樂

> 日期：2026-08-02  
> 範圍：S01～S10 全線＋四結局＋選單／畫廊的 image、transform、BGM、SFX、實體檔案  
> 方法：`tools/validate-assets.py`（新增）＋全套既有驗證腳本（靜態，未開實機）

---

## 總評

**全部通過。** 劇本引用的 134 個實體檔案（bg／dog／char／audio／gallery／theme）全數存在於
`Ch1_Trust_Version3/assets/`（由 `options.rpy` 的 `config.searchpath` 掛載）。

## 自動化結果

| 檢查 | 結果 |
|------|------|
| scene/show 引用 60 個 image 有定義 | OK |
| at 引用 47 個 transform 有定義 | OK |
| `play_bgm` 18 個 profile 在對照表 | OK |
| `dog_sfx` 6 個 cue 在對照表 | OK |
| 引用實體檔案 134/134 存在 | OK |
| `validate-menus` / `validate-menu-layout` | OK |
| `validate-s01` / `validate-s10` / `validate-all-endings` | OK |
| `validate-reading-time` / `test-gallery-load` | OK |

## 本次修正

1. **新增 `tools/validate-assets.py`**：引用一致性＋實體檔案存在性一次驗，之後補資產或改劇本都可重跑。
2. **`test-gallery-load.py` 同步現行設計**：「紀念照片｜背對背」（`secret_back_to_back`）為正式內容
   （UI 按鈕、解鎖線、README 皆有），移除舊的「應刪除」斷言，改為必檢項（7 張紀念照）。

## 待辦（非阻斷）

- **P2｜圖重複**：`gallery/secret-back-to-back.png` 與 `gallery/ending-a-back.png` 為同一張圖
  （MD5 相同）。紀念照與結局 A 靜幀目前看起來一樣，建議交 visual-art 另產一張背對背紀念照。

## 重跑

```powershell
cd Ch1_Trust_Version3\Renpy_game
python tools\validate-assets.py
python tools\test-gallery-load.py
```
