/**
 * 幼犬 vocal — 樣本池 + 場景／選項 cue；避免連續相同聲音。
 */
const DogSounds = (function () {
  let dogGain = null;
  let enabled = true;
  let sceneCueTimer = null;
  let noiseBuffer = null;
  let sampleBuffers = {};
  let samplesReady = false;
  let loadSamplesPromise = null;
  let lastSampleId = null;
  let lastCueName = null;
  let activeCueUntil = 0;
  let thunderSeqTimers = [];

  const POOLS = typeof DOG_SAMPLE_POOLS !== 'undefined' ? DOG_SAMPLE_POOLS : {
    whimper: [{ id: 'whimper_a', file: 'assets/dog/sfx/puppy-whimper-a.wav', volume: 0.90 }],
    soft: [{ id: 'soft_a', file: 'assets/dog/sfx/puppy-soft-a.wav', volume: 0.76 }],
    sigh: [{ id: 'sigh_a', file: 'assets/dog/sfx/puppy-sigh-a.wav', volume: 0.68 }],
    yip: [{ id: 'yip_a', file: 'assets/dog/sfx/puppy-yip-a.ogg', volume: 0.88 }],
    happy: [{ id: 'bark_a', file: 'assets/dog/sfx/puppy-bark-a.wav', volume: 0.86 }],
    excited: [{ id: 'exc_a', file: 'assets/dog/sfx/puppy-excited-a.wav', volume: 0.90 }],
    murmur: [{ id: 'mur_a', file: 'assets/dog/sfx/puppy-murmur-a.wav', volume: 0.52 }],
  };

  const POOL_MAP = typeof CUE_POOL_MAP !== 'undefined' ? CUE_POOL_MAP : {
    whimper: 'whimper', softWhimper: 'soft', sigh: 'sigh', yip: 'yip',
  };

  const CUE_DURATION_MS = {
    sleepBreath: 3200,
    sleepBreathDeep: 5200,
    sleepSnore: 4800,
    sleepSnoreDeep: 6200,
    excitedYip: 900,
    yipExcited: 900,
    sniff: 450,
    sniffQuick: 350,
    sniffDeep: 650,
    huff: 350,
    huffSoft: 300,
    growl: 700,
    grumble: 1100,
  };

  const DOG_GAIN = typeof AUDIO_GAIN === 'number' ? AUDIO_GAIN : 1;
  const DOG_VOCAL_BOOST = 1.55;
  const capDog = (v) => Math.min(1, v * DOG_GAIN * DOG_VOCAL_BOOST);
  const DOG_BUS_VOLUME = capDog(0.52);

  const SCENE_CUES = {
    prologue_rain: { delay: 1200, cue: 'murmurAnxious' },
    prologue_home: { delay: 1800, cue: 'whineSoft' },
    prologue_dry: { delay: 900, cue: 'murmurUneasy' },
    prologue_night: { delay: 2200, cue: 'murmurAnxious' },
    prologue_dawn: { delay: 1800, cue: 'sleepSnoreDeep' },
    day2_empty: { delay: 1600, cue: 'sniffQuick' },
    day2_leave: { delay: 1400, cue: 'murmurLow' },
    day2_rush: { delay: 900, cue: 'breathEase' },
    day2_petshop: { delay: 1200, cue: 'murmurUneasy' },
    day2_petshop_after: { delay: 1400, cue: 'huff' },
    day2_return: { delay: 1000, cue: 'excitedYip' },
    day2_morning: { delay: 1000, cue: 'breathEase' },
    day2_kitchen: { delay: 800, cue: 'sniffQuick' },
    day2_afternoon: { delay: 600, cue: 'huff' },
    day2_evening: { delay: 1600, cue: 'sleepSnore' },
    day3_morning: { delay: 1400, cue: 'sleepBreath' },
    day3_hurt: { delay: 900, cue: 'murmurAnxious' },
    day3_potty_intro: { delay: 1100, cue: 'sniffDeep' },
    day3_night: { delay: 1500, cue: 'whimper' },
    day3_night_after: { delay: 2400, cue: 'sleepSnoreDeep' },
    day4_repair: { delay: 900, cue: 'whineSoft' },
    day4_off: { delay: 1300, cue: 'sniffQuick' },
    day4_vet_go: { delay: 600, cue: 'murmurUneasy' },
    day4_vet_reception: { delay: 800, cue: 'sniffQuick' },
    day4_vet_intake: { delay: 900, cue: 'murmurAnxious' },
    day4_vet: { delay: 1000, cue: 'murmurAnxious' },
    day4_vet_bill: { delay: 1200, cue: 'huff' },
    day4_evening: { delay: 1800, cue: 'sleepSnoreDeep' },
    day5_sunday: { delay: 700, cue: 'sleepBreath' },
    day5_home_intro: { delay: 850, cue: 'sniffDeep' },
    day5_home_after: { delay: 900, cue: 'sigh' },
    day5_evening: { delay: 1600, cue: 'sleepSnoreDeep' },
    day6_morning: { delay: 800, cue: 'yipExcited' },
    day6_thunder_after: { delay: 900, cue: 'sleepBreath' },
    day6_quiet: { delay: 1600, cue: 'sleepSnore' },
    day7_evening: { delay: 1600, cue: 'whineSoft' },
    day7_moment: { delay: 1000, cue: 'sigh' },
    epilogue: { delay: 2200, cue: 'breathEase' },
  };

  function ensureBus() {
    AmbientMusic.ensureContext();
    const ctx = AmbientMusic.getContext();
    const master = AmbientMusic.getMasterGain();
    if (!ctx || !master) return null;
    if (!dogGain) {
      dogGain = ctx.createGain();
      dogGain.gain.value = enabled ? DOG_BUS_VOLUME : 0;
      dogGain.connect(master);
    }
    if (!noiseBuffer) {
      const len = ctx.sampleRate * 0.15;
      noiseBuffer = ctx.createBuffer(1, len, ctx.sampleRate);
      const d = noiseBuffer.getChannelData(0);
      for (let i = 0; i < len; i += 1) d[i] = Math.random() * 2 - 1;
    }
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  function rand(min, max) {
    return min + Math.random() * (max - min);
  }

  function markActiveCue(ms) {
    activeCueUntil = Math.max(activeCueUntil, Date.now() + ms);
  }

  function allSampleDefs() {
    const out = [];
    Object.values(POOLS).forEach((pool) => pool.forEach((d) => out.push(d)));
    return out;
  }

  async function loadSamples() {
    if (samplesReady) return;
    if (loadSamplesPromise) return loadSamplesPromise;

    loadSamplesPromise = (async () => {
      ensureBus();
      const ctx = AmbientMusic.getContext();
      if (!ctx) {
        samplesReady = true;
        return;
      }
      const paths = new Set(allSampleDefs().map((d) => d.file).filter(Boolean));
      await Promise.all([...paths].map(async (path) => {
        if (sampleBuffers[path]) return;
        try {
          const res = await fetch(path);
          if (!res.ok) throw new Error(String(res.status));
          const ab = await res.arrayBuffer();
          sampleBuffers[path] = await ctx.decodeAudioData(ab);
        } catch (e) {
          console.warn('[DogSounds] fetch sample failed (file:// ?):', path, e.message);
        }
      }));
      samplesReady = true;
    })();

    return loadSamplesPromise;
  }

  function pickFromPool(poolKey, opts = {}) {
    const pool = POOLS[poolKey];
    if (!pool?.length) return null;

    let candidates = pool;
    if (opts.sampleId) {
      const forced = pool.find((s) => s.id === opts.sampleId);
      if (forced) return forced;
    }
    if (pool.length > 1) {
      candidates = pool.filter((s) => s.id !== lastSampleId);
      if (!candidates.length) candidates = pool;
    }
    return candidates[Math.floor(Math.random() * candidates.length)];
  }

  function playSampleDef(def, opts = {}) {
    if (!enabled || !def?.file) return false;
    let vol = capDog((def.volume ?? 0.8) * (opts.volumeMult ?? 1));
    const rate = (def.playbackRate ?? 1) * (opts.playbackRateMult ?? 1);

    const ctx = ensureBus();
    const buf = sampleBuffers[def.file];
    if (ctx && buf && dogGain) {
      const src = ctx.createBufferSource();
      const gain = ctx.createGain();
      const t = ctx.currentTime;
      src.buffer = buf;
      src.playbackRate.value = rate;
      gain.gain.setValueAtTime(0, t);
      gain.gain.linearRampToValueAtTime(vol, t + 0.02);
      const dur = buf.duration / rate;
      gain.gain.setValueAtTime(vol, t + Math.max(0.05, dur - 0.08));
      gain.gain.linearRampToValueAtTime(0.001, t + dur + 0.06);
      src.connect(gain);
      gain.connect(dogGain);
      src.start(t);
      src.stop(t + dur + 0.1);
      lastSampleId = def.id;
      markActiveCue(dur * 1000 + 120);
      return true;
    }

    try {
      const audio = new Audio(def.file);
      audio.volume = vol;
      if (rate !== 1) audio.playbackRate = Math.min(2, Math.max(0.5, rate));
      audio.play().catch(() => {});
      lastSampleId = def.id;
      markActiveCue(900);
      return true;
    } catch (_) {
      return false;
    }
  }

  function playPoolCue(cueName, opts = {}) {
    const poolKey = POOL_MAP[cueName];
    if (!poolKey) return false;
    const def = pickFromPool(poolKey, opts);
    if (!def) return false;
    const volMult = cueName === 'whimperQuiet' || cueName === 'breathEase' ? 0.88
      : (cueName.startsWith('murmur') ? 1 : 1);
    const rateMult = cueName === 'yipBright' || cueName === 'yipHappy' ? 1.06
      : cueName === 'yipExcited' || cueName === 'excitedYip' ? 1.08
      : cueName.startsWith('murmur') ? 1
      : cueName === 'barkHappy' || cueName === 'happyBark' ? 1.04
      : 1;
    return playSampleDef(def, { volumeMult: volMult, playbackRateMult: rateMult, ...opts });
  }

  function playExcitedBurst() {
    const poolKey = 'excited';
    const first = pickFromPool(poolKey);
    if (!first) return;
    playSampleDef(first, { playbackRateMult: 1.1 });
    setTimeout(() => {
      if (!enabled) return;
      const second = pickFromPool(poolKey);
      if (second) playSampleDef(second, { playbackRateMult: 1.14, volumeMult: 0.92 });
    }, rand(130, 210));
    markActiveCue(CUE_DURATION_MS.excitedYip);
    lastSampleId = 'excited_burst';
  }

  function playNoiseBurst(t, dur, vol, freq, q = 1.1) {
    const ctx = ensureBus();
    if (!ctx || !enabled) return;
    const src = ctx.createBufferSource();
    src.buffer = noiseBuffer;
    src.loop = true;
    const filter = ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.value = freq;
    filter.Q.value = q;
    const gain = ctx.createGain();
    gain.gain.setValueAtTime(0, t);
    gain.gain.linearRampToValueAtTime(vol, t + 0.015);
    gain.gain.exponentialRampToValueAtTime(0.001, t + dur);
    src.connect(filter);
    filter.connect(gain);
    gain.connect(dogGain);
    src.start(t);
    src.stop(t + dur + 0.02);
  }

  function playSniff(variant = 'normal') {
    const ctx = ensureBus();
    if (!ctx || !enabled) return;
    const counts = { quick: 2, deep: 4, normal: 3 };
    const count = counts[variant] || 3;
    const baseFreq = variant === 'deep' ? rand(480, 620) : variant === 'quick' ? rand(720, 920) : rand(600, 850);
    let t = ctx.currentTime;
    for (let i = 0; i < count; i += 1) {
      playNoiseBurst(t, variant === 'quick' ? 0.03 : 0.04, capDog(0.07 + i * 0.008), baseFreq + i * rand(40, 90), variant === 'deep' ? 1.0 : 1.35);
      t += variant === 'quick' ? 0.05 : 0.07;
    }
    lastSampleId = `sniff_${variant}_${count}`;
    markActiveCue(CUE_DURATION_MS[variant === 'quick' ? 'sniffQuick' : variant === 'deep' ? 'sniffDeep' : 'sniff']);
  }

  function playHuff(variant = 'normal') {
    const ctx = ensureBus();
    if (!ctx || !enabled) return;
    const dur = variant === 'soft' ? rand(0.05, 0.08) : rand(0.06, 0.11);
    playNoiseBurst(ctx.currentTime, dur, capDog(variant === 'soft' ? 0.08 : 0.1), rand(280, 420), 0.75);
    lastSampleId = `huff_${variant}`;
    markActiveCue(CUE_DURATION_MS[variant === 'soft' ? 'huffSoft' : 'huff']);
  }

  function playSleepBreath(deep = false) {
    const ctx = ensureBus();
    if (!ctx || !enabled) return;
    const cycles = deep ? 3 : 2;
    let t = ctx.currentTime;
    const vol = capDog(deep ? 0.032 : 0.042);
    for (let i = 0; i < cycles; i += 1) {
      const inDur = deep ? rand(0.22, 0.32) : rand(0.14, 0.22);
      const gap = deep ? rand(0.9, 1.35) : rand(0.7, 1.05);
      playNoiseBurst(t, inDur, vol, rand(300, 380), 0.5);
      t += inDur + rand(0.08, 0.14);
      playNoiseBurst(t, inDur * 1.15, vol * 0.82, rand(240, 310), 0.42);
      t += inDur * 1.15 + gap;
    }
    lastSampleId = deep ? 'sleep_deep' : 'sleep_breath';
    markActiveCue(CUE_DURATION_MS[deep ? 'sleepBreathDeep' : 'sleepBreath']);
  }

  function playSnoreCycle(t, dur, vol, deep) {
    const ctx = ensureBus();
    if (!ctx || !enabled) return;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const f0 = deep ? rand(88, 102) : rand(98, 118);
    const f1 = deep ? rand(68, 82) : rand(78, 92);
    osc.type = 'sine';
    osc.frequency.setValueAtTime(f0, t);
    osc.frequency.exponentialRampToValueAtTime(Math.max(40, f1), t + dur);
    playNoiseBurst(t + dur * 0.15, dur * 0.75, vol * 0.55, deep ? rand(150, 210) : rand(170, 230), 0.32);
    playNoiseBurst(t + dur * 0.55, dur * 0.25, vol * 0.35, rand(380, 480), 1.4);
    gain.gain.setValueAtTime(0.001, t);
    gain.gain.linearRampToValueAtTime(vol * 0.42, t + dur * 0.18);
    gain.gain.setValueAtTime(vol * 0.38, t + dur * 0.72);
    gain.gain.exponentialRampToValueAtTime(0.001, t + dur + 0.04);
    osc.connect(gain);
    gain.connect(dogGain);
    osc.start(t);
    osc.stop(t + dur + 0.06);
  }

  function playSleepSnore(deep = false) {
    const ctx = ensureBus();
    if (!ctx || !enabled) return;
    const cycles = deep ? 4 : 3;
    let t = ctx.currentTime;
    const vol = capDog(deep ? 0.034 : 0.028);
    for (let i = 0; i < cycles; i += 1) {
      const dur = deep ? rand(0.42, 0.58) : rand(0.32, 0.46);
      const gap = deep ? rand(0.55, 0.85) : rand(0.45, 0.7);
      playSnoreCycle(t, dur, vol, deep);
      t += dur + gap;
    }
    lastSampleId = deep ? 'snore_deep' : 'snore';
    markActiveCue(CUE_DURATION_MS[deep ? 'sleepSnoreDeep' : 'sleepSnore']);
  }

  function playPant(opts = {}) {
    const ctx = ensureBus();
    if (!ctx || !enabled) return;
    const t = ctx.currentTime;
    const dur = opts.slow ? rand(0.14, 0.22) : rand(0.08, 0.14);
    const vol = capDog(opts.vol ?? 0.08);
    playNoiseBurst(t, dur, vol, opts.filter ?? 500, opts.slow ? 0.9 : 1.2);
    if (!opts.slow) {
      playNoiseBurst(t + dur * 0.55, dur * 0.85, vol * 0.85, (opts.filter ?? 500) + 40, 1.1);
    }
    lastSampleId = 'pant';
    markActiveCue(600);
  }

  function playGrowl() {
    const ctx = ensureBus();
    if (!ctx || !enabled) return;
    const t = ctx.currentTime;
    const dur = rand(0.35, 0.55);
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(rand(85, 110), t);
    osc.frequency.linearRampToValueAtTime(rand(70, 95), t + dur);
    playNoiseBurst(t, dur, capDog(0.08), 180, 0.6);
    gain.gain.setValueAtTime(0, t);
    gain.gain.linearRampToValueAtTime(capDog(0.14), t + 0.06);
    gain.gain.setValueAtTime(capDog(0.11), t + dur * 0.6);
    gain.gain.exponentialRampToValueAtTime(0.001, t + dur);
    osc.connect(gain);
    gain.connect(dogGain);
    osc.start(t);
    osc.stop(t + dur);
    lastSampleId = 'growl';
    markActiveCue(CUE_DURATION_MS.growl);
  }

  function playGrumble() {
    playGrowl();
    setTimeout(() => { if (enabled) playCue('whineSoft'); }, 280);
    markActiveCue(CUE_DURATION_MS.grumble);
  }

  const PROCEDURAL = {
    sniff: () => playSniff('normal'),
    sniffQuick: () => playSniff('quick'),
    sniffDeep: () => playSniff('deep'),
    huff: () => playHuff('normal'),
    huffSoft: () => playHuff('soft'),
    pant: () => playPant(),
    sleepBreath: () => playSleepBreath(false),
    sleepBreathDeep: () => playSleepBreath(true),
    sleepSnore: () => playSleepSnore(false),
    sleepSnoreDeep: () => playSleepSnore(true),
    growl: () => playGrowl(),
    grumble: () => playGrumble(),
    excitedYip: () => playExcitedBurst(),
    yipExcited: () => playExcitedBurst(),
  };

  const CUE_SWAP = {
    whimper: 'whimperQuiet',
    whimperScared: 'murmurAnxious',
    whimperQuiet: 'murmurLow',
    whineSoft: 'softWhimper',
    softWhimper: 'murmurUneasy',
    murmurUneasy: 'murmurAnxious',
    murmurAnxious: 'murmurLow',
    murmurLow: 'murmurUneasy',
    sigh: 'breathEase',
    breathEase: 'huffSoft',
    yip: 'yipBright',
    yipBright: 'yipHappy',
    yipHappy: 'barkHappy',
    barkHappy: 'yipExcited',
    yipExcited: 'excitedYip',
    excitedYip: 'barkHappy',
    sleepBreath: 'sleepBreathDeep',
    sleepBreathDeep: 'sleepSnore',
    sleepSnore: 'sleepSnoreDeep',
    sleepSnoreDeep: 'sleepBreath',
  };

  function clearThunderSeq() {
    thunderSeqTimers.forEach((id) => clearTimeout(id));
    thunderSeqTimers = [];
  }

  function queueThunderSeq(fn, ms) {
    thunderSeqTimers.push(setTimeout(fn, ms));
  }

  /** 雷聲後緊接：幼犬害怕（whimper → murmur 漸強） */
  function playThunderScaredSequence() {
    if (!enabled) return;
    clearThunderSeq();
    ensureBus();
    loadSamples();
    lastCueName = null;
    playCue('whimperScared', { noSwap: true, volumeMult: 1.38 });
    queueThunderSeq(() => playCue('whimper', { noSwap: true, volumeMult: 1.28 }), 380);
    queueThunderSeq(() => playCue('murmurAnxious', { noSwap: true, volumeMult: 1.22 }), 820);
    queueThunderSeq(() => playCue('whimperQuiet', { noSwap: true, volumeMult: 1.12 }), 1380);
  }

  /** 安撫小遊戲結束：狗狗漸漸不怕了 */
  function playThunderCalmSequence(tier) {
    if (!enabled) return;
    clearThunderSeq();
    ensureBus();
    lastCueName = null;
    const good = tier === 'perfect' || tier === 'good';
    const ok = tier !== 'miss';
    playCue('breathEase', { noSwap: true, volumeMult: ok ? 1.05 : 0.92 });
    if (good) {
      queueThunderSeq(() => playCue('sleepBreath', { noSwap: true, volumeMult: 1.08 }), 720);
      queueThunderSeq(() => playCue('sigh', { noSwap: true, volumeMult: 1.1 }), 1850);
    } else if (ok) {
      queueThunderSeq(() => playCue('huffSoft', { noSwap: true }), 640);
      queueThunderSeq(() => playCue('breathEase', { noSwap: true }), 1300);
    } else {
      queueThunderSeq(() => playCue('whimperQuiet', { noSwap: true, volumeMult: 0.82 }), 520);
      queueThunderSeq(() => playCue('huffSoft', { noSwap: true }), 1100);
    }
  }

  function playCue(name, opts = {}) {
    if (!enabled || !name) return;

    let cueName = name;
    if (!opts.noSwap && lastCueName === name && CUE_SWAP[name]) {
      cueName = CUE_SWAP[name];
    }

    if (PROCEDURAL[cueName]) {
      if (lastCueName === cueName && cueName.startsWith('sniff')) {
        const alt = cueName === 'sniff' ? 'sniffQuick' : cueName === 'sniffQuick' ? 'sniffDeep' : 'sniff';
        PROCEDURAL[alt]?.();
        lastCueName = alt;
        return;
      }
      if (lastCueName === cueName && (cueName === 'sleepBreath' || cueName === 'sleepBreathDeep'
        || cueName === 'sleepSnore' || cueName === 'sleepSnoreDeep')) {
        const sleepAlt = {
          sleepBreath: 'sleepSnore',
          sleepBreathDeep: 'sleepSnoreDeep',
          sleepSnore: 'sleepBreathDeep',
          sleepSnoreDeep: 'sleepBreath',
        };
        const alt = sleepAlt[cueName] || 'sleepBreath';
        PROCEDURAL[alt]?.();
        lastCueName = alt;
        return;
      }
      if (lastCueName === cueName && (cueName === 'huff' || cueName === 'huffSoft')) {
        const alt = cueName === 'huff' ? 'huffSoft' : 'huff';
        PROCEDURAL[alt]();
        lastCueName = alt;
        return;
      }
      PROCEDURAL[cueName]();
      lastCueName = cueName;
      return;
    }

    if (playPoolCue(cueName, { ...opts, avoidCue: lastCueName })) {
      lastCueName = cueName;
      if (!CUE_DURATION_MS[cueName]) markActiveCue(850);
      return;
    }
    console.warn('[DogSounds] unknown or missing cue:', cueName);
  }

  function stopLoop() {
    if (sceneCueTimer) { clearTimeout(sceneCueTimer); sceneCueTimer = null; }
    clearThunderSeq();
  }

  function setMood() {
    ensureBus();
  }

  function onScene(scene, state) {
    ensureBus();
    loadSamples();
    stopLoop();
    setMood();

    const cueDef = SCENE_CUES[scene?.id];
    if (!cueDef || !enabled) return;

    const now = Date.now();
    const remaining = Math.max(0, activeCueUntil - now);
    const delay = cueDef.delay + remaining + (remaining > 0 ? 400 : 0);

    sceneCueTimer = setTimeout(() => {
      sceneCueTimer = null;
      playCue(cueDef.cue, { source: 'scene', sceneId: scene?.id });
    }, delay);
  }

  function setEnabled(on) {
    enabled = on;
    if (dogGain) {
      const ctx = AmbientMusic.getContext();
      if (ctx) {
        dogGain.gain.setTargetAtTime(on ? DOG_BUS_VOLUME : 0, ctx.currentTime, 0.25);
      }
    }
    if (!on) {
      stopLoop();
      lastSampleId = null;
      lastCueName = null;
      activeCueUntil = 0;
    }
  }

  function stop() {
    stopLoop();
    lastSampleId = null;
    lastCueName = null;
    activeCueUntil = 0;
  }

  return { setMood, onScene, playCue, setEnabled, stop, preload: loadSamples,
    playThunderScaredSequence, playThunderCalmSequence };
})();

if (typeof module !== 'undefined') module.exports = { DogSounds };
