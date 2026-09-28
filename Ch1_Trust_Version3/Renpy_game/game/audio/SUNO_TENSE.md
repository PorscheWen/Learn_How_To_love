# Suno prompt｜S08 `tense`（機車擦過）

> Profile：`tense` → `assets/audio/tense-2.ogg`（Suno take 2）  
> 原 take 1 `tense.ogg` 改掛 S09 `almost_gave`  
> 場景：巷口轉角機車呼嘯；短拍，禁 jump scare、禁人聲、不搶旁白

## 在 Suno 貼這一段（Chat / Simple）

```
Instrumental only, no vocals. Tense but warm visual novel underscore for a scooter passing too close in a narrow alley. Sparse low piano, muted strings, anxious pulse, 76 BPM. No jump scare, no horror, no EDM, no epic orchestra. Soft start then hovering tension. Leave space for dialogue.
```

## Custom Mode（較準）

**Title：** Alley Pass Tense

**Style of Music：**

```
Instrumental only, no vocals, no lyrics. Restrained Taiwan slice-of-life visual novel score. Sudden tense swell without jump scare. Sparse low piano, muted strings, dry anxious pulse like a held breath. 76 BPM minor but warm, not horror, not EDM, not epic orchestra. Seamless loopable bed for a scooter passing too close in a narrow alley. Leave space for spoken dialogue. Soft start, quick rise, then hovering tension.
```

**Lyrics：**

```
[instrumental]
[no vocals]
```

## 匯入遊戲

1. Suno 下載 MP3（選無人聲、不過亮的那一版）。
2. 放到任意路徑後執行：

```powershell
cd Ch1_Trust_Version3
ffmpeg -y -i "下載的檔.mp3" -c:a libvorbis -q:a 5 assets\audio\tense.ogg
```

3. 劇本 `play_bgm("tense")` 指到 `audio/tense-2.ogg`（機車出現前切曲）。AceData 產線：

```powershell
cd Ch1_Trust_Version3\Renpy_game
python tools\suno-generate.py --preset tense
```

預設安裝第一首。兩版 MP3 在 `tools/output/suno/`。S08 現用第二首：

```powershell
ffmpeg -y -i tools\output\suno\20260919-203234-2.mp3 -c:a libvorbis -q:a 5 ..\assets\audio\tense-2.ogg
```

原第一首 `tense.ogg` 保留給 S09 `almost_gave`。
