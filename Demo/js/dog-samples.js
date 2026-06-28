/**
 * 幼犬樣本池 — 同 cue 多變體，避免連續相同聲音。
 * See assets/dog/sfx/CREDITS.md · deploy: tools/download-dog-sfx.ps1
 */
const DOG_SAMPLE_POOLS = {
  whimper: [
    { id: 'whimper_a', file: 'assets/dog/sfx/puppy-whimper-a.wav', volume: 0.90 },
    { id: 'whimper_b', file: 'assets/dog/sfx/puppy-whimper-b.wav', volume: 0.84 },
  ],
  soft: [
    { id: 'soft_a', file: 'assets/dog/sfx/puppy-soft-a.wav', volume: 0.76 },
    { id: 'soft_b', file: 'assets/dog/sfx/puppy-soft-b.wav', volume: 0.70 },
  ],
  sigh: [
    { id: 'sigh_a', file: 'assets/dog/sfx/puppy-sigh-a.wav', volume: 0.68 },
    { id: 'sigh_b', file: 'assets/dog/sfx/puppy-sigh-b.wav', volume: 0.62 },
  ],
  yip: [
    { id: 'yip_a', file: 'assets/dog/sfx/puppy-yip-a.ogg', volume: 0.88 },
    { id: 'yip_b', file: 'assets/dog/sfx/puppy-yip-b.wav', volume: 0.82, playbackRate: 1.05 },
  ],
  happy: [
    { id: 'bark_a', file: 'assets/dog/sfx/puppy-bark-a.wav', volume: 0.86 },
    { id: 'bark_b', file: 'assets/dog/sfx/puppy-bark-b.wav', volume: 0.80, playbackRate: 1.06 },
  ],
  excited: [
    { id: 'exc_a', file: 'assets/dog/sfx/puppy-excited-a.wav', volume: 0.90, playbackRate: 1.10 },
    { id: 'exc_b', file: 'assets/dog/sfx/puppy-excited-b.wav', volume: 0.86, playbackRate: 1.14 },
  ],
  murmur: [
    { id: 'mur_a', file: 'assets/dog/sfx/puppy-murmur-a.wav', volume: 0.52, playbackRate: 0.92 },
    { id: 'mur_b', file: 'assets/dog/sfx/puppy-murmur-b.wav', volume: 0.48, playbackRate: 0.88 },
  ],
};

/** cue 名稱 → 樣本池 */
const CUE_POOL_MAP = {
  whimper: 'whimper',
  whimperScared: 'whimper',
  softWhimper: 'soft',
  whineSoft: 'soft',
  whimperQuiet: 'soft',
  sigh: 'sigh',
  breathEase: 'sigh',
  yip: 'yip',
  yipBright: 'yip',
  yipHappy: 'yip',
  barkHappy: 'happy',
  happyBark: 'happy',
  yipExcited: 'excited',
  excitedYip: 'excited',
  murmurUneasy: 'murmur',
  murmurAnxious: 'murmur',
  murmurLow: 'murmur',
};

/** 舊版相容 */
const DOG_SAMPLES = {
  whimper: DOG_SAMPLE_POOLS.whimper[0],
  softWhimper: DOG_SAMPLE_POOLS.soft[0],
  yip: DOG_SAMPLE_POOLS.yip[0],
};

if (typeof module !== 'undefined') {
  module.exports = { DOG_SAMPLE_POOLS, CUE_POOL_MAP, DOG_SAMPLES };
}
