/**
 * Story Agent — 每個選項必須有狗狗反應（視覺 + 叫聲 + 行為文字）
 */
const StoryAgent = (function () {
  const TRUST_TIER = [
    { min: 12, key: 'trust_up_high' },
    { min: 4, key: 'trust_up' },
    { min: -3, key: 'trust_neutral' },
    { min: -12, key: 'trust_down' },
    { min: -999, key: 'trust_down_hard' },
  ];

  const TRUST_LINES = {
    trust_up_high: (s) => `${dogLabel(s)} 的耳朵動了一下，身子慢慢鬆了一點。`,
    trust_up: (s) => `${dogLabel(s)} 看你一眼，沒有再退。`,
    trust_neutral: (s) => `${dogLabel(s)} 停了一下，像在等你的下一個動作。`,
    trust_down: (s) => `${dogLabel(s)} 往後縮了半步。`,
    trust_down_hard: (s) => `${dogLabel(s)} 夾緊尾巴，整個身子又小了一圈。`,
  };

  const FEELING_LINES = {
    anxious: (s) => `${dogLabel(s)} 還沒準備好，但沒有跑開。`,
    curious: (s) => `${dogLabel(s)} 豎了豎耳朵，小心地嗅了嗅。`,
    content: (s) => `${dogLabel(s)} 呼出一口氣，像終於敢放鬆一點。`,
    hurt: (s) => `${dogLabel(s)} 把視線移開，不再看你。`,
    excited: (s) => `${dogLabel(s)} 尾巴晃了一下，又克制住。`,
    attached: (s) => `${dogLabel(s)} 輕輕靠過來，停在你能碰到的地方。`,
    sleepy: (s) => `${dogLabel(s)} 眼皮半闔，呼吸變長。`,
    playful: (s) => `${dogLabel(s)} 前腳趴低，邀請再來一次。`,
    alert: (s) => `${dogLabel(s)} 豎起耳朵，在聽什麼。`,
    shy: (s) => `${dogLabel(s)} 把臉藏起來，只露出鼻尖。`,
    hungry: (s) => `${dogLabel(s)} 鼻子貼地，循著氣味。`,
    angry: (s) => `${dogLabel(s)} 低低哼了一聲，還在生氣。`,
  };

  const FEELING_CUE_OPTIONS = {
    anxious: ['murmurUneasy', 'murmurAnxious', 'murmurLow', 'whimperQuiet'],
    curious: ['sniff', 'sniffQuick', 'huff'],
    content: ['sigh', 'breathEase', 'huffSoft'],
    hurt: ['whimper', 'whimperQuiet', 'murmurAnxious'],
    excited: ['excitedYip', 'yipExcited', 'barkHappy'],
    attached: ['breathEase', 'sigh', 'whineSoft'],
    sleepy: ['sleepSnore', 'sleepSnoreDeep', 'sleepBreath', 'sleepBreathDeep'],
    playful: ['barkHappy', 'yipHappy', 'yipExcited'],
    alert: ['huff', 'sniffQuick', 'murmurLow'],
    shy: ['murmurLow', 'whineSoft', 'whimperQuiet'],
    hungry: ['sniff', 'sniffDeep', 'sniffQuick'],
    angry: ['growl', 'whimper', 'murmurAnxious'],
  };

  function pickFromOptions(options) {
    if (!options?.length) return 'huff';
    return options[Math.floor(Math.random() * options.length)];
  }

  function trustTier(delta) {
    for (let i = 0; i < TRUST_TIER.length; i += 1) {
      if (delta >= TRUST_TIER[i].min) return TRUST_TIER[i].key;
    }
    return 'trust_down_hard';
  }

  function pickLine(state, feeling, trustDelta) {
    const tier = trustTier(trustDelta);
    if (Math.abs(trustDelta) >= 8) {
      const fn = TRUST_LINES[tier];
      if (fn) return fn(state);
    }
    const feelFn = FEELING_LINES[feeling];
    if (feelFn) return feelFn(state);
    const meta = FEELINGS[feeling];
    return meta?.behavior || TRUST_LINES.trust_neutral(state);
  }

  function pickCue(feeling, trustDelta) {
    if (trustDelta <= -12) return pickFromOptions(['whimper', 'whimperScared', 'whimperQuiet']);
    if (trustDelta <= -5 && (feeling === 'hurt' || feeling === 'angry')) {
      return pickFromOptions(['softWhimper', 'whimperQuiet', 'whineSoft']);
    }
    if (trustDelta >= 10 && (feeling === 'content' || feeling === 'attached')) {
      return pickFromOptions(['sigh', 'breathEase', 'whineSoft']);
    }
    if (trustDelta >= 8 && feeling === 'playful') {
      return pickFromOptions(['barkHappy', 'yipExcited', 'yipHappy']);
    }
    if (trustDelta >= 8 && feeling === 'excited') {
      return pickFromOptions(['excitedYip', 'barkHappy', 'yipExcited']);
    }
    return pickFromOptions(FEELING_CUE_OPTIONS[feeling]) || 'huff';
  }

  function resolvePose(rawPose, state) {
    if (!rawPose) return null;
    if (typeof rawPose === 'function') return rawPose(state);
    return rawPose;
  }

  function normalize(raw, state, ctx) {
    const feeling = raw.feeling || ctx.afterFeeling || state.feeling;
    const trustDelta = ctx.trustDelta;
    const withDog = isDogAudioEnabled(ctx.scene, ctx.choice);
    const cue = raw.noDogSound || !withDog
      ? null
      : (raw.cue ?? pickCue(feeling, trustDelta));
    return {
      text: applyDogPronouns(
        typeof raw.text === 'function' ? raw.text(state, ctx) : (raw.text || pickLine(state, feeling, trustDelta)),
        state,
      ),
      feeling,
      pose: resolvePose(raw.pose, state),
      cue,
      cueDelay: raw.cueDelay ?? 380,
      holdMs: raw.holdMs ?? (Math.abs(trustDelta) >= 10 ? 2100 : 1800),
    };
  }

  function lookupMapped(choice, state, ctx) {
    if (typeof lookupChoiceReaction === 'function') {
      const mapped = lookupChoiceReaction(ctx.sceneId, choice.text);
      if (mapped) return normalize(mapped, state, ctx);
    }
    return null;
  }

  /**
   * 一律回傳反應；僅 choice.skipReact 可略過（供除錯）
   * @returns {object}
   */
  function resolve(choice, state, ctx) {
    if (choice.skipReact) return null;
    if (!isDogAudioEnabled(ctx.scene, choice)) return null;

    if (choice.react) {
      const raw = typeof choice.react === 'function' ? choice.react(state, ctx) : choice.react;
      return normalize(raw, state, ctx);
    }

    const mapped = lookupMapped(choice, state, ctx);
    if (mapped) return mapped;

    const feeling = ctx.afterFeeling || state.feeling;
    return {
      text: applyDogPronouns(pickLine(state, feeling, ctx.trustDelta), state),
      feeling,
      pose: null,
      cue: pickCue(feeling, ctx.trustDelta),
      cueDelay: 380,
      holdMs: Math.abs(ctx.trustDelta) >= 10 ? 2100 : 1800,
    };
  }

  return { resolve };
})();

if (typeof module !== 'undefined') module.exports = { StoryAgent };
