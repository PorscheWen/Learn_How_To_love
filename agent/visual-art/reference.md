# 美術參考

## 角色外型聖經

**權威來源：** 本節為全系列狗／主人／NPC 外型的唯一細規格。`guide_line.md` §6.6、`SKILL.md` 摘要均須與此一致。生成 PNG、審查舊圖、撰寫 image prompt 前必讀。

---

### 狗狗（全三部曲 · 同一角色）

| 項目 | 規格 |
|------|------|
| **品種感** | 台灣常見 **混種幼犬**（scruffy mixed breed）；毛略蓬、略捲；**不可**畫成柯基、贵宾、柴犬、哈士奇等可一眼辨識的純種 |
| **年齡感** | **Ch1 Demo：約 2–4 個月**；體型小、腿短、肚略圓、步態還在學；Ch2 略大穩重；Ch3 老犬（灰吻、動作慢）— 仍是**同一隻** |
| **毛色** | 主色 **golden-tan / honey ochre（金褐、蜂蜜 ochre）**；背脊、耳尖略深褐；胸口、吻部、尾尖略淺奶油 |
| **筆觸** | 數位水彩／ gouache 感；邊緣晕染、筆觸可見；**無硬黑描邊、無平塗卡通** |
| **五官** | 圓而暖的 **深褐** 眼睛（非誇張大眼）；中等長吻；**半垂耳**（好奇、期待、警戒時可豎起） |
| **尾巴** | 中等長；不安時夾尾；開心時小幅度搖，不誇張扇形 |
| **主參考圖** | `Demo/assets/dog/dog-anxious.png` |
| **檔案** | `assets/dog/dog-{id}.png`；RGBA 透明；去背 `remove_dog_bg.py` |

**禁止：** 換品種或配色、多狗同框、廉價 Q 版、寫實照片、SVG／幾何拼接、把狗畫進背景 PNG。

#### 特殊 pose 構圖（含主人局部）

| pose | 構圖規則 |
|------|----------|
| `knee` | 狗頭**輕靠大腿旁／膝上緣**；僅露主人**大腿／褲管／裙擺上緣**；**禁止**小腿、腳踝、腳、鞋 |
| `held` / `vet-carry` | 幼犬在**臂彎**；可見主人前臂＋**簡素袖口**；不露臉 |
| `home-settle` | 下巴擱膝上；同 `knee` 構圖規則 |

#### Aging（Ch2 / Ch3）

- 同一水彩風格、同一毛色基調。
- 可新增 `dog-grey-muzzle.png`、`dog-slow.png` 等；**不可**換成另一隻狗。

---

### 主人／玩家（「你」）

| 項目 | 規格 |
|------|------|
| **年齡** | **25 歲** |
| **性別／外型** | **年輕長髮女性**；一般身形；非健美、非動漫誇張比例 |
| **髮型** | **長髮**（自然深褐或黑；及肩或過肩；微卷或直髮皆可；不誇張染燙） |
| **身份** | **上班族**；人生過渡期、獨居小公寓（Demo：需請假／打卡、剛帶幼犬回家） |
| **寵物經驗** | **第一次養寵物**；不懂規矩、會慌，但願意學 |
| **性格（敘事）** | **感情豐富**——易共感、內心戲多、會內疚也會溫柔；不寫成誇張戲劇或無腦衝動 |
| **敘事視角** | 第二人稱「你」；玩家代入此固定主角 |
| **Demo 呈現** | **不露全臉、無全立繪**；第一人稱；僅 story pose 必要時露**手、臂、大腿、髮絲** |
| **膚色** | 自然 **暖調**（與 UI `--warm-bg` `#f5e6d3` 協調） |
| **服裝** | 簡素日常：**米白、燕麦、灰褐、深棕、低飽和牛仔**；棉／ knit；居家寬褲或及膝裙；**無 Logo、無鮮豔撞色** |
| **手／臂** | 纖細自然；無浮誇美甲、大戒指、智慧手錶特寫 |

**禁止：** 全臉立繪（Demo）、指定真實名人臉、男性化／中性化到偏離「長髮女性」設定、與 UI 色溫衝突的螢光色服裝。

---

### NPC（scene-art · 與狗同 watercolor 風）

| 角色 | 外型 | 參考檔 |
|------|------|--------|
| 寵物店店員 | 中年大姐、圍裙、親切笑容、專業但不嚴厲 | `scene-petshop-clerk.png` |
| 寵物店結帳 | 同上或店員在櫃台 | `scene-petshop-checkout.png` |
| 獸醫 | 白袍、聽診器、穩重溫和 | `scene-vet-doctor.png` |
| 醫院櫃台 | 制服或櫃台人員、專業 | `scene-vet-bill.png` |

NPC 亦：**無硬黑描邊**、單角色、白底去背、與狗 PNG 同 gouache／水彩 indie 基調。

---

### AI 繪圖 Prompt 模板（複製後替換 `{pose}`）

**狗（單獨）：**

```
Digital watercolor illustration, single scruffy golden-tan mixed breed puppy,
2-4 months old, honey ochre fur with slightly darker ears and back,
lighter cream chest and muzzle, semi-floppy ears, warm dark brown eyes,
soft watercolor brushstrokes, no hard black outlines, {pose description},
centered full body, clean white background, gentle indie game character sprite.
Style reference: dog-anxious.png
```

**狗 + 主人局部（knee）：**

```
(same dog as above), gently resting head against side of young woman's upper thigh,
25-year-old office worker, only upper thigh and lap in soft neutral oatmeal/gray-brown skirt or lounge pants visible,
slender feminine proportions, NO calves, NO feet, NO shoes, NO lower legs below knee,
clean white background, digital watercolor, no hard outlines, no face.
```

**主人臂彎（held / vet-carry）：** 同上狗描述 + `cradled in young woman's arms, simple cream or gray-brown sleeve cuff, slender wrists, no face`.

---

## CSS 色票（style.css）

| 變數 | 用途 | 色值 |
|------|------|------|
| `--warm-bg` | 安全、預設 | `#f5e6d3` |
| `--warm-accent` | 強調 | `#c4846c` |
| `--warm-text` | 正文 | `#3d2c29` |
| `--cold-bg` | 不安、雷雨 | `#d4dce8` |
| `--cold-accent` | 冷調強調 | `#6b8499` |
| `--content-glow` | 滿足、默契 | `#e8c49a` |
| `--hurt-dim` | 受傷、低落 | `#8a7b78` |

字體：`Cormorant Garamond`（標題）、`Noto Sans TC`（正文）。

## 沉浸式版面變數（Demo 基準，維持勿改模式）

| 變數 | 預設 | 用途 |
|------|------|------|
| `--art-share` | `70%` | 主視覺區概念比例 |
| `--dialogue-share` | `30%` | 底部字幕 overlay 高度 |
| `--scene-inner-h` | `100dvh - hud - footer` | 可玩區高度 |
| `--dog-max-h` | `scene-inner-h * 0.52` | 狗 PNG 最大高度 |
| `--dog-max-w` | `min(440px, 84vw)` | 狗 PNG 最大寬度 |
| `--behavior-top` | `2.65rem` | 狗狗反應字幕距頂（氣味列下） |
| `--hud-h` / `--footer-h` | `3.1rem` | 上下 chrome 估算 |

### DOM 疊層（z-index）

| 元素 | z-index | 備註 |
|------|---------|------|
| `.scene-bg` | 0 | 背景 + 輕 vignette `::after` |
| `.scene-art` | 1 | NPC（狗後方） |
| `.scene-stage` / `.dog-stage` | 2 | 狗、行為字幕 |
| `.smell-bar` | 5 | 頂部浮動 |
| `.scene-dialogue` | 4 | 底部漸層 overlay |
| `.hud` | 6 | 標題列 |

### 構圖規則摘要

1. **單一畫布**：`.scene-stage` 與 `.scene-dialogue` 同屬 `.scene`，對話不另開「下方黑箱」。
2. **狗的位置**：`.dog-stage { bottom: calc(var(--dialogue-share) + 2%) }`，腳踩字幕帶上緣。
3. **行為字幕**：`.dog-behavior` 只在上方；半透明膠囊，不遮主圖。
4. **選項可見**：`.choices { flex-shrink: 0 }`；`.scene.has-choices` 時字幕 viewport 略縮。
5. **短螢幕**：`@media (max-height: 720px)` 微調 `--dog-max-*`、`--behavior-top`，仍保持 70/30。

## 情緒圖清單（12）

| 檔名 | Feeling |
|------|---------|
| dog-anxious.png | Anxious |
| dog-curious.png | Curious |
| dog-content.png | Content |
| dog-hurt.png | Hurt |
| dog-excited.png | Excited |
| dog-attached.png | Attached |
| dog-sleepy.png | Sleepy |
| dog-playful.png | Playful |
| dog-alert.png | Alert |
| dog-shy.png | Shy |
| dog-hungry.png | Hungry |
| dog-angry.png | Angry |

## 故事動作圖（Demo · 節錄）

rain, corner, kitchen, balcony, potty, home, night-accident, knee, repair, toy, doorway, doorway-wait, doorway-lie, stair, walk, park, follow-close, follow-far, thunder, window, sad-day, vet-carry, vet-walk, held, sunday-wake, home-settle, paw-smell-1/2/3

## 色溫 ↔ Feelings 建議

| Feelings 群 | `#app` class |
|-------------|--------------|
| Content, Attached, Sleepy | warm 或 content |
| Anxious, Hurt, Alert, Angry | cold |
| Curious, Playful, Excited | warm |
| 雷雨場景 | cold + 可選暗角 |

## 背景場景原則

- Demo：**gouache／水彩感 PNG**（`Demo/assets/bg/`），`cover` + 預設 `center 28%`。
- 狗永遠独立 PNG 叠在 `.scene-stage`；背景不含狗、不含主人全形。
- `#app.cold .scene-bg`：`saturate(0.7) brightness(0.95)`；`#app.content` 略提亮。
- location id 與 `locations.js`、`audio.js` 的 `WEATHER_BY_LOCATION` 對齊。

## 去背流程

```bash
cd Learn_How_To_Love
python Demo/tools/remove_dog_bg.py
```

依賴 rembg；新增 PNG 後必跑。
