# Learn How to Love — Demo

**Chapter 1: First Steps（信任）** · 接回家第 1–7 天 · 約 35 分鐘

---

## 快速開始

**雙擊啟動（Windows）：**

- `開啟遊戲.bat` 或 `play.bat`（會自動部署 BGM 檔）

**首次或 BGM 無聲時：**

1. **請用 `開啟遊戲.bat` 啟動**（會開 `http://localhost:8765/`，勿直接雙擊 index.html）
2. 或手動部署 + 伺服器：

```powershell
cd Learn_How_To_Love\Demo
powershell -ExecutionPolicy Bypass -File tools\deploy-audio.ps1
python -m http.server 8765
# 瀏覽器開 http://localhost:8765/
```

> 直接 `file://` 開啟時，瀏覽器常擋 OGG 載入；遊戲會改走 HTML Audio / 程序化 fallback，但仍建議用本機 HTTP。

### Windows（PowerShell）

```powershell
Start-Process "C:\Users\BaoGo\Documents\ClaudeCode_Project\Learn_How_To_Love\Demo\index.html"
```

---

## Demo 內容

| 項目 | 說明 |
|------|------|
| 時間範圍 | Day 1–7（Day 2 試探可玩） |
| 場景數 | 28 個（含 20 種視覺場景） |
| 感受 | Anxious、Curious、Content、Hurt、Excited、Attached |
| 羈絆 | Lv1 陌生 → Lv2 習慣 |
| 背景音樂 | 開源 OGG 鋼琴 ambient（OpenGameArt）+ 程序化 fallback；🎵 切換 |
| 必觸發 | Moment《第一次跟脚》（Trust 高時完整版） |
| 條件事件 | Memory《第一次自己吃》《尿墊之夜》《雷雨》《陽台》《公園》等 |
| 結尾 | 「羈絆才剛開始寫。」 |

### 場景一覽

雨天紙箱 → 第一夜 → **Day 2 試探**（廚房／聲響）→ Day 3 早晨 → 廚房 → **陽台** → 如廁訓練 → 深夜尿墊 → 修復/早晨 → **下午玩玩具** → 門口 → **樓梯** → 街道 → **小公園** → 夕陽回家 → 週末雷雨/靜日 → Day 7 傍晚 → Epilogue

---

## 操作

- **選項按鈕**：推進劇情；選擇會影響 Trust / Bond（數值隱藏，僅見耳尾與色溫）。
- **🎵**：開關背景音樂
- **文字速度**（頁尾或開場）：緩 / 舒 / 常 / 快 / 即時（預設 **緩**）
- **點擊正文**：立刻顯示完當前段落
- **小遊戲**：如廁引導（點擊時機）、散步（按住「輕聲喚牠」）。
- **🐾 腳印集**：已解鎖的特別事件。
- **💾**：複製跨作存檔 JSON。
- **繼續旅程**：讀取 localStorage 存檔。

---

## 檔案結構

```
Demo/
├── index.html          # 入口
├── css/style.css       # 視覺與色溫 UI
├── js/
│   ├── systems.js      # Trust / Bond / 存檔
│   ├── locations.js    # 場景標籤與視覺對照
│   ├── audio.js        # 程序化 BGM
│   ├── scenes.js       # 場景與分支
│   └── game.js         # 引擎與小遊戲
├── DEMO_DESIGN.md      # 設計文件
└── README.md
```

---

## 設計對齊

本 Demo 遵循 `../guide_line.md`：

- ✅ 後果服務「學會愛」，無 permadeath
- ✅ 無數字 stat 面板（感受以視覺呈現）
- ✅ 壞選擇可修復（Day 4 修復線）
- ✅ 跨作存檔 JSON 原型

---

## 驗收

- [ ] 通關約 25–35 分鐘
- [ ] 至少解鎖 2 個 Moment + 1 個 Memory
- [ ] Bond 達 Lv2
- [ ] 匯出 JSON 含 `dogName`、`memories`、`flags`

詳見 `DEMO_DESIGN.md`。
