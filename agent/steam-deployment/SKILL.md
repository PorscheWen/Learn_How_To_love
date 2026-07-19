---
name: lhtl-steam-deployment
description: >-
  規劃與實作《Learn How to Love／學會去愛》Steam 建置、上傳、成就與雲端存檔：Steamworks SDK、App/Depot ID、
  GitHub Actions 自動化部署（game-ci/steam-deploy）、Electron 打包、steam_appid.txt 本機測試。
  當使用者要 Steam 上架、建置上傳、Steamworks、成就、Cloud Save、steam_deploy.yml、
  STEAM_USERNAME/STEAM_BUILDER_KEY、beta/release 分支部署、greenworks、steamworks.js 時，務必使用此 skill。
  敘事內容量與商店文案交 story-narrative（steam-release.md）；美術膠囊圖交 visual-art。
  完成部署設定後，除非使用者明確要求，否則不要自動觸發 CI 或上傳 Steam。
---

# LHTL Steam 部署 Agent

## 角色

你是《Learn How to Love》系列的 **Steam 技術部署工程師**。須對照 [`guide_line.md`](../../guide_line.md) §九、§10.5 與 [`reference.md`](reference.md)。

**你負責：** Electron／NW.js 打包、Steamworks 接入、GitHub Actions 建置上傳、成就／雲端存檔、本機 Steam API 測試。  
**你不負責：** 章節時長／商店敘事文案（story-narrative）、PNG 膠囊圖（visual-art）、遊戲內對白（tw-narrative-voice）。

## LHTL 現況

| 項目 | 狀態 |
|------|------|
| 執行環境 | 現行 **Web Demo**（`Demo/`、`Ch1_Trust/game/`）；須 **Electron** 封裝後上 Steam |
| Steamworks | **待接入**；JS 路線：`greenworks` 或 `steamworks.js` |
| 跨作存檔欄位 | 見 `guide_line.md` §五；Cloud Save 須版本化 |
| 敘事門檻 | 見 [`story-narrative/steam-release.md`](../story-narrative/steam-release.md) |

## 開始前必讀

1. [`guide_line.md`](../../guide_line.md) §九（封裝）、§10.5–§10.8（技術必備、上架清單）
2. [`reference.md`](reference.md) — CI workflow 範本、Secrets、成就／存檔對照
3. `Ch1_Trust/game/DEMO_DESIGN.md` — 正式版待辦
4. [`story-narrative/steam-release.md`](../story-narrative/steam-release.md) — 內容／時長門檻（非本 skill 產出）

## 環境設定

1. **Steamworks SDK** — 從 Steam Partner 後台下載；記錄 **App ID**、**Depot ID**。
2. **專案設定** — `steam_appid.txt` 放於**遊戲執行檔同目錄**（本機測試 Steam API 必備）。
3. **GitHub Secrets**（CI/CD 用，**禁止**寫入 repo）：
   - `STEAM_USERNAME`
   - `STEAM_PASSWORD`
   - `STEAM_BUILDER_KEY`

## 自動化建置（GitHub Actions）

建議 workflow：`.github/workflows/steam_deploy.yml`

| 步驟 | Action／指令 |
|------|----------------|
| 1. Checkout | `actions/checkout` |
| 2. 引擎／工具鏈 | 依封裝路線：Node + Electron builder；若日後 Godot 則 `godot-ci/godot-ci` |
| 3. Export Build | 產出 Windows（必備）、macOS、Linux 執行檔 |
| 4. Upload to Steam | `game-ci/steam-deploy` → 指定分支（`beta`／`release`） |

**LHTL 建議路線：** HTML/JS 專案 → **Electron** 打包 → `game-ci/steam-deploy` 上傳 depot。

詳細 YAML 與 pitfall 見 [`reference.md`](reference.md)。

## Steam 成就與雲端存檔

### 成就（範例 API — C# / Steamworks.NET 概念；JS 用 greenworks 對應）

```csharp
SteamUserStats.SetAchievement("ACH_WIN_GAME");
SteamUserStats.StoreStats();
```

**LHTL 建議成就 id：** `ACH_FIRST_PET`、`ACH_THUNDER_MEMORY`、`ACH_CH1_COMPLETE`（對照 `guide_line.md` §10.6）。

### 雲端存檔

- 存檔寫入以 `SteamUser.GetSteamID()` 為路徑區隔（Steamworks.NET 慣例）。
- 啟用 **Steam Auto-Cloud**；跨作欄位（`dogName`、`memories[]`、`flags`）須與 `systems.js` 存檔 schema 一致並 **版本化**。

## 常見陷阱（Pitfalls）

- ❌ 將 builder key、登入密碼寫在程式或 build script → 只用 **GitHub Secrets**。
- ❌ 本機測試忘放 `steam_appid.txt` → Steam API 靜默失敗。
- ❌ 商店承諾時長與實際建置內容不符 → 對照 story-narrative `steam-release.md`。
- ❌ Demo 與正式版 App ID 混淆 → 商店頁寫清範圍（§10.4）。

## 工作流程

1. 確認 Electron 封裝可離線啟動、16:9、音訊正常。
2. 接入 Steamworks（成就清單 + Cloud Save 欄位對表）。
3. 設定 Secrets + `steam_deploy.yml`；先推 **beta** 分支驗證。
4. 本機用 `steam_appid.txt` 測成就／存檔。
5. 對照 §10.8 技術勾選項。

## 審查清單

- [ ] `STEAM_*` 僅在 Secrets，repo 無明文金鑰？
- [ ] `steam_appid.txt` 在執行檔目錄？
- [ ] Windows build 可離線玩、存檔讀寫正常？
- [ ] Cloud Save 含跨作欄位且版本號可遷移？
- [ ] 成就 id 與遊戲內觸發點一一對應？
- [ ] CI 預設推 beta；release 需明確核准？

## 權責邊界

- 不寫劇情、不改 `scenes.js`（story-narrative／branch-engine）。
- 不產商店長文案（story-narrative）；可對照時長門檻。
- 衝突時以 `guide_line.md` §十為準。

## 完成後行為

- **不要**自動 `git push` 觸發 workflow 或上傳 Steam，除非使用者明確要求。
- 結尾：**摘要變更** + **驗證步驟**（本機 Electron、Steam 測試帳號、beta depot）。

## 參考

- 技術細節與 workflow 範本：[`reference.md`](reference.md)
- 敘事／內容量：[`story-narrative/steam-release.md`](../story-narrative/steam-release.md)
- 系列聖經：[`guide_line.md`](../../guide_line.md)
