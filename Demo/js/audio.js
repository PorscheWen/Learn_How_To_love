/**
 * Ambient BGM — OGG loops (+ HTML Audio fallback).
 * Storm profile adds distant thunder rumble on weatherBus (Day 6 evening).
 */
const AmbientMusic = (function () {
  let ctx = null;
  let masterGain = null;
  let musicBus = null;
  let weatherBus = null;
  let reverbGain = null;
  let dryGain = null;
  let enabled = true;
  let started = false;
  let currentProfile = 'warm';
  let nodes = { weather: null };
  let timers = [];
  let buffers = {};
  let buffersReady = false;
  let loadPromise = null;
  let activeTracks = [];
  let htmlFallbackReady = false;
  let padNodes = { oscs: [], gains: [], filters: [] };
  let musicState = {
    progressionIdx: 0,
    chordIdx: 0,
    phraseIdx: 0,
    phraseNote: 0,
    rootShift: 0,
  };

  const GAIN = typeof AUDIO_GAIN === 'number' ? AUDIO_GAIN : 1;
  const capGain = (v) => Math.min(1, v * GAIN);

  const MASTER_VOLUME = capGain(0.58);
  const MASTER_FADE_IN = capGain(0.35);
  const FADE_SEC = 2.8;
  const LOOP_PAD = typeof BGM_LOOP_PAD === 'number' ? BGM_LOOP_PAD : 0.035;

  const PROFILES = {
    warm:    { root: 220, mood: 'major', volume: 0.1, speed: 9500 },
    calm:    { root: 196, mood: 'major', volume: 0.08, speed: 11500 },
    tense:   { root: 174, mood: 'minor', volume: 0.07, speed: 7500 },
    storm:   { root: 155, mood: 'minor', volume: 0.06, speed: 5500, weather: 'storm' },
    tender:  { root: 207, mood: 'major', volume: 0.09, speed: 12500 },
    hopeful: { root: 247, mood: 'major', volume: 0.09, speed: 10000 },
    night:   { root: 165, mood: 'minor', volume: 0.07, speed: 13500 },
    rain:    { root: 185, mood: 'minor', volume: 0.07, speed: 10500, weather: 'rain' },
    sunny:   { root: 262, mood: 'major', volume: 0.08, speed: 9000, weather: 'sunny' },
    sunset:  { root: 233, mood: 'major', volume: 0.08, speed: 10000, weather: 'sunset' },
    melancholy: { root: 164, mood: 'minor', volume: 0.065, speed: 14500, weather: 'rain' },
  };

  const WEATHER_BY_LOCATION = {
    prologue_rain: 'rain',
    window_rain: 'rain',
    living_storm: 'storm',
    street_sunset: 'sunset',
    balcony: 'sunny',
    park: 'sunny',
    street: 'sunny',
    kitchen_morning: 'sunny',
    living_sunday: 'sunny',
  };

  const PROGRESSIONS = {
    major: [
      [[0, 4, 7], [5, 9, 12], [7, 11, 14], [9, 12, 16]],
      [[0, 4, 7], [9, 12, 16], [5, 9, 12], [7, 11, 14]],
    ],
    minor: [
      [[0, 3, 7], [5, 8, 12], [7, 10, 14], [8, 12, 15]],
      [[0, 3, 7], [8, 12, 15], [5, 8, 12], [7, 10, 14]],
    ],
  };

  const MELODY_PHRASES = {
    major: [[0, 2, 4, 7, 4], [7, 9, 7, 4], [4, 7, 9, 7]],
    minor: [[0, 3, 5, 3], [7, 10, 7], [8, 10, 8]],
  };

  function randJitter(ms) {
    return (Math.random() - 0.5) * ms;
  }

  function getProfile() {
    return PROFILES[currentProfile] || PROFILES.warm;
  }

  function getTrackDef(profile) {
    if (typeof BGM_TRACKS === 'undefined') return null;
    return BGM_TRACKS[profile] || null;
  }

  function canPlayFileProfile(profile) {
    return !!getTrackDef(profile)?.file;
  }

  function hasBufferForProfile(profile) {
    const def = getTrackDef(profile);
    return !!(def && buffers[def.file]);
  }

  function shouldUseProcedural(profile) {
    return false;
  }

  function effectiveTrackVolume(def) {
    return Math.min(1, capGain(def.volume ?? 0.32));
  }

  function getProgression(p) {
    const sets = PROGRESSIONS[p.mood] || PROGRESSIONS.major;
    return sets[musicState.progressionIdx % sets.length];
  }

  function rootFreq(p, semiOffset = 0) {
    return p.root * Math.pow(2, (semiOffset + musicState.rootShift) / 12);
  }

  function resetMusicState() {
    musicState = {
      progressionIdx: Math.floor(Math.random() * 2),
      chordIdx: 0,
      phraseIdx: Math.floor(Math.random() * 2),
      phraseNote: 0,
      rootShift: 0,
    };
  }

  function createReverb() {
    const convolver = ctx.createConvolver();
    const rate = ctx.sampleRate;
    const length = Math.floor(rate * 2.4);
    const impulse = ctx.createBuffer(2, length, rate);
    for (let c = 0; c < 2; c += 1) {
      const data = impulse.getChannelData(c);
      for (let i = 0; i < length; i += 1) {
        data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / length, 2.4) * 0.28;
      }
    }
    convolver.buffer = impulse;
    return convolver;
  }

  function createMusicCompressor() {
    const comp = ctx.createDynamicsCompressor();
    comp.threshold.value = -22;
    comp.knee.value = 18;
    comp.ratio.value = 2.8;
    comp.attack.value = 0.012;
    comp.release.value = 0.28;
    return comp;
  }

  function ensureContext() {
    if (!ctx) {
      ctx = new (window.AudioContext || window.webkitAudioContext)();
      masterGain = ctx.createGain();
      masterGain.gain.value = enabled ? MASTER_VOLUME : 0;
      masterGain.connect(ctx.destination);

      weatherBus = ctx.createGain();
      weatherBus.gain.value = 1;
      weatherBus.connect(masterGain);

      musicBus = ctx.createGain();
      musicBus.gain.value = 1;
      const comp = createMusicCompressor();
      const reverb = createReverb();
      reverbGain = ctx.createGain();
      reverbGain.gain.value = 0.32;
      dryGain = ctx.createGain();
      dryGain.gain.value = 0.78;

      musicBus.connect(comp);
      comp.connect(dryGain);
      comp.connect(reverb);
      reverb.connect(reverbGain);
      dryGain.connect(masterGain);
      reverbGain.connect(masterGain);
    }
    if (ctx.state === 'suspended') ctx.resume();
  }

  async function unlock() {
    ensureContext();
    if (ctx.state === 'suspended') {
      await ctx.resume();
    }
    if (!loadPromise) loadPromise = loadBuffers();
    await loadPromise;
    htmlFallbackReady = typeof BGM_TRACKS !== 'undefined';
    return ctx.state;
  }

  async function loadBuffers() {
    if (typeof BGM_TRACKS === 'undefined') {
      buffersReady = true;
      return;
    }
    if (!ctx) {
      buffersReady = true;
      return;
    }
    const paths = new Set();
    Object.values(BGM_TRACKS).forEach((t) => { if (t.file) paths.add(t.file); });
    await Promise.all([...paths].map(async (path) => {
      if (buffers[path]) return;
      try {
        const res = await fetch(path);
        if (!res.ok) throw new Error(String(res.status));
        const ab = await res.arrayBuffer();
        buffers[path] = await ctx.decodeAudioData(ab);
      } catch (e) {
        console.warn('[AmbientMusic] fetch BGM failed (file:// ?):', path, e.message);
      }
    }));
    buffersReady = true;
  }

  function preload() {
    return unlock().catch((e) => {
      console.warn('[AmbientMusic] preload skipped:', e.message);
    });
  }

  function clearTimers() {
    timers.forEach((id) => { clearInterval(id); clearTimeout(id); });
    timers = [];
  }

  function scheduleLoop(fn, baseMs, jitterMs = 0) {
    const run = () => {
      if (!enabled || !started) return;
      fn();
      timers.push(setTimeout(run, Math.max(140, baseMs + randJitter(jitterMs || baseMs * 0.08))));
    };
    fn();
    timers.push(setTimeout(run, baseMs));
  }

  function fadeOutTrack(entry, dur = FADE_SEC) {
    if (!entry) return;
    if (entry.isElement && entry.html) {
      const el = entry.html;
      if (entry.gain && ctx) {
        const t = ctx.currentTime;
        try {
          entry.gain.gain.cancelScheduledValues(t);
          entry.gain.gain.setValueAtTime(entry.gain.gain.value, t);
          entry.gain.gain.linearRampToValueAtTime(0.001, t + dur);
        } catch (_) {}
        setTimeout(() => { try { el.pause(); el.removeAttribute('src'); } catch (_) {} }, (dur + 0.25) * 1000);
      } else {
        el.volume = 0;
        try { el.pause(); el.removeAttribute('src'); } catch (_) {}
      }
      return;
    }
    if (!entry?.gain || !ctx) return;
    const t = ctx.currentTime;
    try {
      entry.gain.gain.cancelScheduledValues(t);
      entry.gain.gain.setValueAtTime(entry.gain.gain.value, t);
      entry.gain.gain.linearRampToValueAtTime(0.001, t + dur);
      setTimeout(() => { try { entry.src?.stop(); } catch (_) {} }, (dur + 0.25) * 1000);
    } catch (_) {}
  }

  /** 立即切斷單轨（關閉遊戲／回主選單用，不做 crossfade） */
  function killTrack(entry) {
    if (!entry) return;
    if (entry.isElement && entry.html) {
      const el = entry.html;
      try {
        el.pause();
        el.currentTime = 0;
        el.removeAttribute('src');
        el.load?.();
      } catch (_) {}
      return;
    }
    try {
      if (entry.gain && ctx) entry.gain.gain.cancelScheduledValues(ctx.currentTime);
      entry.src?.stop();
    } catch (_) {}
  }

  function stopActiveTracks() {
    activeTracks.forEach((e) => fadeOutTrack(e));
    activeTracks = [];
  }

  function stopActiveTracksImmediate() {
    activeTracks.forEach((e) => killTrack(e));
    activeTracks = [];
  }

  function stopPadNodes() {
    const t = ctx.currentTime;
    padNodes.gains.forEach((g) => {
      if (g) g.gain.setTargetAtTime(0.001, t, 0.5);
    });
    setTimeout(() => {
      padNodes.oscs.forEach((o) => { try { o.stop(); } catch (_) {} });
      padNodes = { oscs: [], gains: [], filters: [] };
    }, 800);
  }

  function stopPadNodesImmediate() {
    padNodes.oscs.forEach((o) => { try { o.stop(); } catch (_) {} });
    padNodes = { oscs: [], gains: [], filters: [] };
  }

  function makeBrownNoiseBuffer(durationSec = 3) {
    const len = Math.floor(ctx.sampleRate * durationSec);
    const buf = ctx.createBuffer(1, len, ctx.sampleRate);
    const d = buf.getChannelData(0);
    let last = 0;
    for (let i = 0; i < len; i += 1) {
      const white = Math.random() * 2 - 1;
      last = (last + 0.02 * white) / 1.02;
      d[i] = last * 2.8;
    }
    return buf;
  }

  function stopWeatherLayer(fadeSec = 0.9) {
    const w = nodes.weather;
    if (!w) return;
    if (w.thunderTimer) {
      clearTimeout(w.thunderTimer);
      w.thunderTimer = null;
    }
    if (w.rumbleGain && ctx) {
      try {
        w.rumbleGain.gain.setTargetAtTime(0.001, ctx.currentTime, fadeSec * 0.45);
      } catch (_) {}
    }
    setTimeout(() => {
      try { w.rumbleSrc?.stop(); } catch (_) {}
      if (nodes.weather === w) nodes.weather = null;
    }, fadeSec * 1000 + 120);
  }

  function stopWeatherLayerImmediate() {
    const w = nodes.weather;
    if (!w) return;
    if (w.thunderTimer) {
      clearTimeout(w.thunderTimer);
      w.thunderTimer = null;
    }
    try { w.rumbleSrc?.stop(); } catch (_) {}
    nodes.weather = null;
  }

  function playThunderRoll(opts = {}) {
    const kind = opts.kind || 'ambient';
    const volumeScale = opts.volumeScale ?? 1;
    if (!ctx || !weatherBus || !enabled || !started) return;
    if (kind === 'ambient' && currentProfile !== 'storm') return;
    if (kind !== 'ambient' && currentProfile !== 'storm' && !opts.force) return;

    const t = ctx.currentTime;
    const isIntro = kind === 'intro';
    const isChoice = kind === 'choice' || isIntro;
    const dur = isIntro
      ? 2.8 + Math.random() * 1.6
      : isChoice
        ? 1.8 + Math.random() * 2.2
        : 2.2 + Math.random() * 2.8;
    const bufLen = Math.floor(ctx.sampleRate * dur);
    const buf = ctx.createBuffer(1, bufLen, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < bufLen; i += 1) {
      d[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufLen * (isIntro ? 0.22 : 0.28 + Math.random() * 0.12)));
    }

    const src = ctx.createBufferSource();
    src.buffer = buf;
    const lp = ctx.createBiquadFilter();
    lp.type = 'lowpass';
    lp.frequency.setValueAtTime(
      (isIntro ? 980 : isChoice ? 820 : 720) + Math.random() * (isIntro ? 320 : 280),
      t,
    );
    lp.frequency.exponentialRampToValueAtTime(isIntro ? 110 : 90, t + dur);
    lp.Q.value = isIntro ? 0.72 : 0.55;

    const gain = ctx.createGain();
    const basePeak = isIntro
      ? 0.16 + Math.random() * 0.07
      : isChoice
        ? 0.14 + Math.random() * 0.06
        : 0.09 + Math.random() * 0.05;
    const peak = capGain(basePeak * volumeScale);
    const attack = isIntro
      ? 0.02 + Math.random() * 0.06
      : isChoice
        ? 0.05 + Math.random() * 0.18
        : 0.12 + Math.random() * 0.55;
    gain.gain.setValueAtTime(0.001, t);
    gain.gain.linearRampToValueAtTime(peak, t + attack);
    gain.gain.exponentialRampToValueAtTime(0.001, t + dur);

    src.connect(lp);
    lp.connect(gain);
    gain.connect(weatherBus);
    src.start(t);
    src.stop(t + dur + 0.05);

    if ((isChoice || isIntro) && nodes.weather?.rumbleGain) {
      const bump = capGain((isIntro ? 0.11 : 0.058) * Math.min(volumeScale, 3));
      try {
        nodes.weather.rumbleGain.gain.cancelScheduledValues(t);
        nodes.weather.rumbleGain.gain.setValueAtTime(nodes.weather.rumbleGain.gain.value, t);
        nodes.weather.rumbleGain.gain.linearRampToValueAtTime(bump, t + 0.08);
        nodes.weather.rumbleGain.gain.linearRampToValueAtTime(capGain(0.042), t + (isIntro ? 2.2 : 1.4));
      } catch (_) {}
    }

    return { dur, peakAt: attack };
  }

  /** Day 6 雷雨開場：放大雷聲後接狗狗害怕（由 DogSounds 播放） */
  function playThunderIntro(opts = {}) {
    ensureContext();
    if (!enabled || !started) return null;
    const scale = opts.volumeScale ?? 3;
    return playThunderRoll({ kind: 'intro', force: true, volumeScale: scale });
  }

  function triggerStormThunderOnChoice() {
    ensureContext();
    if (!enabled || !started) return;
    playThunderRoll({ kind: 'choice', force: true });
  }

  function scheduleThunderRolls() {
    if (!nodes.weather || !enabled || !started || currentProfile !== 'storm') return;
    playThunderRoll();
    const nextMs = 8500 + Math.random() * 13000;
    nodes.weather.thunderTimer = setTimeout(() => scheduleThunderRolls(), nextMs);
  }

  function startStormWeatherLayer() {
    if (!ctx || !weatherBus || nodes.weather) return;

    const rumbleBuf = makeBrownNoiseBuffer(4);
    const rumbleSrc = ctx.createBufferSource();
    rumbleSrc.buffer = rumbleBuf;
    rumbleSrc.loop = true;

    const lp = ctx.createBiquadFilter();
    lp.type = 'lowpass';
    lp.frequency.value = 260;
    lp.Q.value = 0.35;

    const rumbleGain = ctx.createGain();
    rumbleGain.gain.value = 0.001;
    rumbleSrc.connect(lp);
    lp.connect(rumbleGain);
    rumbleGain.connect(weatherBus);
    rumbleSrc.start();

    const t = ctx.currentTime;
    rumbleGain.gain.linearRampToValueAtTime(capGain(0.042), t + 2.2);

    nodes.weather = { rumbleSrc, rumbleGain, lp, thunderTimer: null };
    nodes.weather.thunderTimer = setTimeout(
      () => scheduleThunderRolls(),
      1800 + Math.random() * 3200,
    );
  }

  function startWeatherLayer() {}

  function startWeatherForProfile(profile) {
    stopWeatherLayerImmediate();
    if (!enabled || !started || profile !== 'storm') return;
    startStormWeatherLayer();
  }

  function stopNodes() {
    stopActiveTracks();
    stopPadNodes();
    stopWeatherLayer();
  }

  function stopNodesImmediate() {
    stopActiveTracksImmediate();
    stopPadNodesImmediate();
    stopWeatherLayerImmediate();
  }

  function playSoftTone(freq, dur, vol, opts = {}) {
    const bus = opts.bus || musicBus;
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const filter = ctx.createBiquadFilter();
    const t = ctx.currentTime;
    filter.type = 'lowpass';
    filter.frequency.value = opts.cutoff ?? 2000;
    filter.Q.value = 0.5;
    osc.type = opts.type ?? 'sine';
    osc.frequency.setValueAtTime(freq, t);
    gain.gain.setValueAtTime(0, t);
    gain.gain.linearRampToValueAtTime(vol, t + 0.15);
    gain.gain.exponentialRampToValueAtTime(0.001, t + dur + 1.2);
    osc.connect(filter);
    filter.connect(gain);
    gain.connect(bus);
    osc.start(t);
    osc.stop(t + dur + 1.4);
  }

  function morphPadChord(chord, profile) {
    const p = PROFILES[profile] || PROFILES.warm;
    const t = ctx.currentTime;
    const tones = chord.slice(0, 3);
    while (padNodes.oscs.length < 3) {
      const i = padNodes.oscs.length;
      const osc = ctx.createOscillator();
      const filter = ctx.createBiquadFilter();
      const gain = ctx.createGain();
      filter.type = 'lowpass';
      filter.frequency.value = profile === 'storm' ? 900 : 1400;
      osc.type = i === 0 ? 'sine' : 'triangle';
      osc.connect(filter);
      filter.connect(gain);
      gain.connect(musicBus);
      gain.gain.value = 0;
      osc.start();
      padNodes.oscs.push(osc);
      padNodes.filters.push(filter);
      padNodes.gains.push(gain);
    }
    tones.forEach((semi, i) => {
      padNodes.oscs[i].frequency.setTargetAtTime(rootFreq(p, semi - 12), t, 3);
      padNodes.gains[i].gain.setTargetAtTime(capGain(p.volume * (i === 0 ? 0.28 : 0.16)), t, 2.8);
    });
  }

  function startPadLayer(profile) {
    const p = PROFILES[profile] || PROFILES.warm;
    const tick = () => {
      if (!enabled || !started || !shouldUseProcedural(currentProfile)) return;
      const prog = getProgression(p);
      morphPadChord(prog[musicState.chordIdx % prog.length], profile);
      musicState.chordIdx += 1;
    };
    tick();
    scheduleLoop(tick, p.speed * 1.15, 600);
  }

  function startSoftMelody(profile) {
    const p = PROFILES[profile] || PROFILES.warm;
    const phrases = MELODY_PHRASES[p.mood] || MELODY_PHRASES.major;
    scheduleLoop(() => {
      if (!enabled || !started || !shouldUseProcedural(currentProfile)) return;
      if (Math.random() > 0.62) return;
      const prog = getProgression(p);
      const root = prog[musicState.chordIdx % prog.length][0];
      const phrase = phrases[musicState.phraseIdx % phrases.length];
      const semi = root + phrase[musicState.phraseNote % phrase.length];
      playSoftTone(rootFreq(p, semi + 12), 2.4, capGain(p.volume * 0.11), { cutoff: 2400 });
      musicState.phraseNote += 1;
      if (musicState.phraseNote >= phrase.length) {
        musicState.phraseNote = 0;
        musicState.phraseIdx = (musicState.phraseIdx + 1) % phrases.length;
      }
    }, p.speed * 0.6, 500);
  }

  function startFileTrack(profile) {
    const def = getTrackDef(profile);
    const buf = def && buffers[def.file];
    if (!def || !buf) return false;

    stopPadNodes();
    activeTracks.forEach((e) => fadeOutTrack(e));

    const src = ctx.createBufferSource();
    src.buffer = buf;
    src.loop = true;
    if (def.playbackRate) src.playbackRate.value = def.playbackRate;
    if (buf.duration > LOOP_PAD * 3) {
      src.loopStart = LOOP_PAD;
      src.loopEnd = buf.duration - LOOP_PAD;
    }

    const hp = ctx.createBiquadFilter();
    hp.type = 'highpass';
    hp.frequency.value = 72;
    hp.Q.value = 0.6;

    const lp = ctx.createBiquadFilter();
    lp.type = 'lowpass';
    lp.frequency.value = def.filterHz ?? 11000;
    lp.Q.value = 0.65;

    const gain = ctx.createGain();
    gain.gain.value = 0;

    src.connect(hp);
    hp.connect(lp);
    lp.connect(gain);
    gain.connect(musicBus);
    src.start();

    const t = ctx.currentTime;
    const target = effectiveTrackVolume(def);
    gain.gain.linearRampToValueAtTime(target, t + FADE_SEC);

    activeTracks = [{ src, gain, filter: lp }];
    return true;
  }

  /** file:// fallback — HTMLAudioElement when fetch/decode fails */
  function startElementTrack(profile) {
    const def = getTrackDef(profile);
    if (!def?.file || !htmlFallbackReady) return false;

    stopPadNodes();
    activeTracks.forEach((e) => fadeOutTrack(e));
    activeTracks = [];

    const audio = new Audio(def.file);
    audio.loop = true;
    audio.preload = 'auto';
    if (def.playbackRate) audio.playbackRate = def.playbackRate;

    const target = effectiveTrackVolume(def);
    let entry = { html: audio, isElement: true };

    if (ctx && musicBus) {
      try {
        const src = ctx.createMediaElementSource(audio);
        const gain = ctx.createGain();
        gain.gain.value = 0;
        src.connect(gain);
        gain.connect(musicBus);
        entry.gain = gain;
        entry.mediaSrc = src;
      } catch (e) {
        console.warn('[AmbientMusic] MediaElementSource fallback:', e.message);
      }
    }

    const fadeIn = () => {
      if (entry.gain && ctx) {
        const t = ctx.currentTime;
        entry.gain.gain.linearRampToValueAtTime(target, t + FADE_SEC);
      } else {
        audio.volume = target;
      }
    };

    audio.addEventListener('error', () => {
      console.warn('[AmbientMusic] HTML Audio failed:', def.file);
    });

    audio.play().then(fadeIn).catch((err) => {
      console.warn('[AmbientMusic] play() blocked or missing file:', def.file, err.message);
    });

    activeTracks = [entry];
    return true;
  }

  function startMusicLayers(profile) {
    resetMusicState();
    if (startFileTrack(profile)) return;
    if (startElementTrack(profile)) return;
    console.warn('[AmbientMusic] No BGM file for profile:', profile);
  }

  function applyProfile(profile) {
    currentProfile = profile;
    clearTimers();
    stopActiveTracks();
    stopPadNodes();
    stopWeatherLayerImmediate();
    startMusicLayers(profile);
    startWeatherForProfile(profile);
  }

  function setProfile(profile) {
    if (!started) return;
    if (profile === currentProfile) return;
    applyProfile(profile);
    if (enabled && masterGain && ctx) {
      masterGain.gain.cancelScheduledValues(ctx.currentTime);
      masterGain.gain.setValueAtTime(MASTER_VOLUME, ctx.currentTime);
    }
  }

  function rampMasterVolume(target = MASTER_VOLUME, dur = 2.6) {
    if (!masterGain || !ctx) return;
    masterGain.gain.cancelScheduledValues(ctx.currentTime);
    masterGain.gain.setValueAtTime(MASTER_FADE_IN, ctx.currentTime);
    masterGain.gain.linearRampToValueAtTime(enabled ? target : 0, ctx.currentTime + dur);
  }

  function start(profile = 'warm') {
    ensureContext();
    started = true;
    applyProfile(profile);
    if (enabled && masterGain && ctx) {
      masterGain.gain.cancelScheduledValues(ctx.currentTime);
      masterGain.gain.setValueAtTime(enabled ? MASTER_VOLUME : 0, ctx.currentTime);
    }
  }

  function stop() {
    started = false;
    clearTimers();
    stopNodes();
  }

  /** 關閉遊戲／離開分頁：立刻靜音並釋放所有音源 */
  function shutdown() {
    started = false;
    clearTimers();
    stopNodesImmediate();
    if (masterGain && ctx) {
      try {
        masterGain.gain.cancelScheduledValues(ctx.currentTime);
        masterGain.gain.setValueAtTime(0, ctx.currentTime);
      } catch (_) {}
    }
    if (ctx && ctx.state === 'running') {
      ctx.suspend().catch(() => {});
    }
  }

  function toggle() {
    enabled = !enabled;
    if (masterGain) {
      masterGain.gain.setTargetAtTime(enabled ? MASTER_VOLUME : 0, ctx.currentTime, 0.4);
    }
    if (typeof DogSounds !== 'undefined') DogSounds.setEnabled(enabled);
    return enabled;
  }

  function isEnabled() { return enabled; }
  function getContext() { return ctx; }
  function getMasterGain() { return masterGain; }
  function usesFileTracks() { return buffersReady && Object.keys(buffers).length > 0; }

  function profileForScene(scene) {
    if (!scene) return { profile: 'warm' };

    const loc = scene.location || '';
    let profile = scene.music || null;

    if (!profile && WEATHER_BY_LOCATION[loc]) {
      profile = WEATHER_BY_LOCATION[loc];
    }

    if (!profile) {
      if (loc.includes('night') || loc === 'entrance_night') profile = 'night';
      else if (scene.feeling === 'hurt' || scene.feeling === 'anxious') profile = 'tense';
      else if (scene.feeling === 'attached' || scene.isEpilogue) profile = 'tender';
      else if (scene.feeling === 'content') profile = 'calm';
      else profile = 'warm';
    }

    return { profile };
  }

  return {
    start, stop, shutdown, setProfile, toggle, isEnabled, profileForScene, preload, unlock,
    ensureContext, getContext, getMasterGain, usesFileTracks, triggerStormThunderOnChoice,
    playThunderIntro,
  };
})();

if (typeof module !== 'undefined') module.exports = { AmbientMusic };
