# LHTL 角色聖經參考表

> 敘事權威：`MEMORY.md` §3～§4.2 + `guide_line.md` · 本表＝濃縮查表  
> 視覺權威：`visual-art/reference.md`

## 主人「你」

| 欄位 | 值 |
|------|-----|
| 年齡 | 25 |
| 性別 | 女性（長髮） |
| 職業 | 上班族 |
| 住處 | 獨居小公寓 |
| 寵物經驗 | **成年後第一次獨立飼養**（幼年有他人狗的陰影） |
| 班表 | 週一～五 08:00–17:00 上班；週六日放假 |
| 敘事人稱 | 第二人稱「你」 |
| 核心怕 | 再靠近就再失去（虧欠感） |

### 幼年陰影（作者知情）

| 項目 | 鎖定 |
|------|------|
| 事件 | 被別家狗意外護住（擋危險）→ 該狗過世 |
| 定性 | 意外犧牲；非英雄成仁 |
| Ch1 | 半隱：過度緊張、伸手又縮；**無**車禍閃回／舊債告白 |
| 禁止 | 現犬＝贖罪／命價對等 |

## 狗狗（主角）

| 欄位 | 值 |
|------|-----|
| 品種感 | 混種幼犬 scruffy mixed breed |
| 毛色 | golden-tan / honey ochre |
| 全系列 | 同一隻；Ch2/3 僅 aging 變體 |
| 相遇前 | 短暫被愛 → **典型遺棄**（人消失）；無暴力 |
| 核心傷 | 「好過 → 突然消失」 |

### Ch1 年齡時間軸

| 故事日 | 狗年齡 | 行為合理範圍 |
|--------|--------|--------------|
| Day 1 相遇 | ~3 月 | 抖、怕、控尿差、不能獨太久 |
| Day 1–14 | ~3 月 | 分離焦慮、社會化皆第一次 |
| Day 15+ Week3 | 4–5 月 | 略長高、仍幼犬衝動 |
| Day 365 | ~1 歲 | 大一圈、仍活潑；非老犬 |

### Ch1 身世呈現（只症狀）

門縫久嗅、一時黏一時退、對紙箱／塑膠袋／引擎聲過警；半句「曾有別人／還有別人的味道」。不定罪、不講前主人全史。

### 不合理（Ch1 違規）

- 成犬穩定、老犬步態、灰吻（留 Ch3）
- Day3 像 6 個月大；Day28 像成犬
- 文案「成年犬」「老狗」（週年前）
- Ch1 旁白講完遺棄過程或車禍舊債
- 身世收集 UI／全結局圖鑑解鎖

## 兩線呼應

| | 狗 | 你 |
|--|----|----|
| 傷 | 被人丟掉 | 曾被狗護住後失去牠 |
| 怕 | 再信任又走人 | 再靠近又失去 |
| 解法 | 「還在」的重複證明 | 學會留下，不是還債 |

## 身世揭示節奏（摘要）

| 章 | 給 | 不給 |
|----|----|------|
| Ch1 | 半句＋行為 | 真相全文、蒐集任務 |
| Ch2 | 日常碎片 | 一次講完 |
| Ch3 | 氣味對齊；好好說再見 | 舊債道德綁架 |

詳見 `MEMORY.md` §4.2。

## 取名／代詞

| 函式 | 行為 |
|------|------|
| `dogLabel(s)` | 有名→名；無→「牠」 |
| `dogPronoun(s)` | female→她、male→他、else→牠 |
| `applyDogPronouns(text,s)` | 替換牠／他的 |
| `hasDogName(s)` | `dogName` 非空 |
| `setDogProfile` | 寫 `dogName`、`dogGender`、`flags.dogNamed` |

### 時間錨

| 階段 | scene | 規則 |
|------|-------|------|
| 前 | `prologue_*`～`day2_petshop` | 僅「牠」 |
| 中 | `day2_naming`／`day2_gender` | UI prompt |
| 後 | `day2_return`+ | `dogLabel`／`dogPronoun` |

## NPC

| ID | 名稱 | 類型 | 首次 |
|----|------|------|------|
| — | 寵物店店員 | 人類 NPC | day2_petshop |
| — | 獸醫 | 人類 NPC | day4_vet |
| `ah_huang` | 阿黃 | 狗友 companion | week2_elevator_dog |

阿黃資產：`assets/dog/companions/ah-huang/` · 驗證 `validate-companion-ah-huang.js`

## 跨 surface 對照

| Surface | 須一致 |
|---------|--------|
| `scenes.js` text/sub | 取名時間線、年齡感、身世半隱 |
| `choice-reactions.js` | `dogLabel(s)` 函式 |
| `ALBUM_ENTRIES` | Memory 當下語氣、取名狀態 |
| HUD | `dogLabel`、地點 label |
| 存檔 JSON | `dogName`、`dogGender`、`flags` |

## 掃描指令

```powershell
cd Ch1_Trust\game
rg "豆花" js\
rg "Day[0-9]|Week[0-9]" js\scenes.js   # 英文殘留
node tools\tw-locale-pass.js
```

*最後更新：2026-08-11 · 對齊 MEMORY／guide_line 身世鎖定；Playable＝Version3；半句落地見 MEMORY §4.2*
