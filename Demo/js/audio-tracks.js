/**
 * BGM manifest — Demo 混音：背景音樂 + 狗聲（無環境雜音）。
 * See assets/audio/CREDITS.md · deploy: tools/deploy-audio.ps1
 *
 * AUDIO_GAIN: 全域音量倍率（目前 2 = 在基準混音上再放大兩倍）
 */
const AUDIO_GAIN = 2;

const BGM_TRACKS = {
  warm:    { file: 'assets/audio/warm.ogg',   volume: 0.34 },
  calm:    { file: 'assets/audio/calm.ogg',   volume: 0.30 },
  tender:  { file: 'assets/audio/tender.ogg', volume: 0.32 },
  hopeful: { file: 'assets/audio/warm.ogg',   volume: 0.36 },
  sunny:   { file: 'assets/audio/warm.ogg',   volume: 0.32 },
  sunset:  { file: 'assets/audio/tender.ogg', volume: 0.30 },
  night:   { file: 'assets/audio/calm.ogg',   volume: 0.26, playbackRate: 0.93, filterHz: 1300 },
  rain:    { file: 'assets/audio/calm.ogg',   volume: 0.28, filterHz: 1500 },
  tense:   { file: 'assets/audio/calm.ogg',   volume: 0.24, playbackRate: 0.88, filterHz: 850 },
  storm:   { file: 'assets/audio/calm.ogg',   volume: 0.22, playbackRate: 0.85, filterHz: 800 },
  melancholy: {
    file: 'assets/audio/melancholy.ogg',
    volume: 0.28,
    playbackRate: 0.90,
    filterHz: 950,
  },
};

/** Loop padding (seconds) to reduce OGG seam clicks */
const BGM_LOOP_PAD = 0.035;

if (typeof module !== 'undefined') module.exports = { BGM_TRACKS, BGM_LOOP_PAD, AUDIO_GAIN };
