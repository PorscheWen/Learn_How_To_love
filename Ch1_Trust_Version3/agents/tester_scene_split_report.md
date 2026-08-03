# Tester 報告｜場景拆分（對齊 S01 回家三拍）

> 日期：2026-08-03  
> 範圍：`script.rpy` S02／S07／S08／S09／S10 場景切換；`image_bg.md` 速查表

## 變更摘要

| Sec | 拆分 |
|-----|------|
| S02 | `office`（關螢幕）→ `convenience` → `street`（巷口）→ `backdoor` → `street`（抱走／電梯）→ **`entrance`（進門）** → `living`（自我介紹） |
| S07 | `living` → **`kitchen_night`（倒水）** → `living`（門線）→ `office` |
| S08 | 返家後客廳聞胸背帶 → **`office_night`（週一同事）** |
| S09 | `office`（茶水間）→ **`living_night`（三晚猶豫）** → `living_day`（打包）→ `entrance` → `cafe` |
| S10 送走 | **`alley_night` → `entrance` → `kitchen` → `living`** |
| S10 留下 | **`street`（買碗）→ `entrance` → `living`（掛勾）→ `kitchen`（雙碗）→ `living`（停電）** |
| 結局 | A 維持客廳睡姿；B／C／D 既有 `entrance` 短切，未再改 |

S03／S04／S05／S06：主幹已對齊，未硬拆（無浴室／臥室資產）。

## 自動化結果

```text
python tools/validate-s01.py              OK
python tools/validate-s10.py              OK（A～D 皆 ≥5 分）
python tools/validate-all-endings.py      OK
python tools/validate-menus.py            OK
python tools/validate-reading-time.py     OK（S01～S07≥5；S08／S09≥8）
python tools/validate-assets.py           OK（含 bg-kitchen-night；0 缺檔）
python tools/validate-narration.py        OK
python tools/validate-menu-layout.py      OK（需 PYTHONIOENCODING=utf-8；否則 cp950 印 ≤ 會炸）
```

## 閱讀時間（最短路徑）

| 段 | 分鐘 | 門檻 |
|----|------|------|
| S01 | 7.06 | ≥5 |
| S02 | 10.00 | ≥5 |
| S03 | 7.17 | ≥5 |
| S04 | 6.24 | ≥5 |
| S05 | 6.29 | ≥5 |
| S06 | 5.70 | ≥5 |
| S07 | 5.54 | ≥5 |
| S08 | 10.23 | ≥8 |
| S09 | 10.50 | ≥8 |
| S10-A～D | 7.66～9.26 | ≥5 |

## 殘餘（非阻塞）

- [P2] S03 洗澡／S04 關浴室／S07 床場：仍用 `living` 代理（無浴室／臥室 bg）
- [P2] `validate-menu-layout.py` 在 Windows cp950 主控台印 `≤` 會 UnicodeEncodeError；設 `PYTHONIOENCODING=utf-8` 即過

## 建議實機抽測

1. S02 抱狗回家：街→玄關→客廳立繪不重疊
2. S07 倒水：廚房切換後狗立繪依關門／留縫正確恢復
3. S10 送走：空玄關→洗碗→空掛勾節奏
4. S10 留下：雙碗在廚房、停電回客廳
