# Demo 幼犬聲樣本（CC0）

## 樣本池

| 池 | 檔案 | cue 別名 | 來源 | 授權 |
|----|------|----------|------|------|
| whimper | puppy-whimper-a/b.wav | whimper, whimperScared | [Chihuahua Puppy Whine](https://freesound.org/people/AustinXYZ/sounds/350593/) | **CC0** |
| soft | puppy-soft-a/b.wav | softWhimper, whineSoft, whimperQuiet | [Puppy (8)](https://freesound.org/people/johnnypanic/sounds/728029/) | **CC0** |
| sigh | puppy-sigh-a/b.wav | sigh, breathEase | 同上（較短片段） | **CC0** |
| yip | puppy-yip-a.ogg, puppy-yip-b.wav | yip, yipBright, yipHappy | [Baby Animals](https://opengameart.org/content/baby-animals-sounds-pack) `Bark.ogg` | **CC0** |
| happy | puppy-bark-a/b.wav | barkHappy, happyBark | 同上 `Bark.ogg` 剪輯 | **CC0** |
| excited | puppy-excited-a/b.wav | excitedYip, yipExcited | 同上（較短、較快） | **CC0** |
| murmur | puppy-murmur-a/b.wav | murmurUneasy, murmurAnxious, murmurLow | johnnypanic + AustinXYZ 長段低音量 | **CC0** |

程序化：`sniff*`、`huff*`、`sleepBreath*`、**`sleepSnore*`**（熟睡呼嚲）、`growl`、`excitedYip`（連續快叫）

下載：`Demo/tools/download-dog-sfx.ps1`

## 隔天切音修正

- BGM 換 profile 時不再把 master gain 拉回 fade-in（避免狗聲被壓低）
- `onScene` 會等上一段 cue 播完再排下一段
