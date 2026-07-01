/**
 * 引導小遊戲結果 → 狗狗反應 + 數值 + 下一場景敘事提示
 * tier: potty perfect|good|partial|miss · walk success|partial|struggle
 */
const MINIGAME_OUTCOMES = {
  potty: {
    perfect: {
      trust: 12,
      bond: 22,
      feeling: 'content',
      cue: 'yip',
      pose: 'potty',
      holdMs: 1800,
      resultLine: (s) => `${dogLabel(s)} 在尿墊上停了一下——像終於聽懂你的暗號。`,
      reactionLine: (s) => `${dogLabel(s)} 回頭看你，尾巴輕輕晃了一下。`,
      memory: 'potty_guide',
    },
    good: {
      trust: 10,
      bond: 18,
      feeling: 'curious',
      cue: 'sniff',
      pose: 'potty',
      holdMs: 1600,
      resultLine: (s) => `對了兩次。${dogLabel(s)} 在尿墊邊多停了一會，沒有再躲開。`,
      reactionLine: (s) => `${dogLabel(s)} 在尿墊邊嗅了嗅，鼻子朝你的方向動了動。`,
    },
    partial: {
      trust: 5,
      bond: 10,
      feeling: 'anxious',
      cue: 'softWhimper',
      pose: 'potty',
      holdMs: 1400,
      resultLine: (s) => `只對了一次。${dogLabel(s)} 還在試，你也還在找時機。`,
      reactionLine: (s) => `${dogLabel(s)} 在客廳和尿墊之間來回走，拿不定主意。`,
    },
    miss: {
      trust: 2,
      bond: 5,
      feeling: 'shy',
      cue: 'softWhimper',
      pose: 'corner',
      holdMs: 1400,
      resultLine: (s) => `這次沒對上。${dogLabel(s)} 縮回角落，像怕做錯事。`,
      reactionLine: (s) => `${dogLabel(s)} 把臉藏起來，只露出鼻尖。`,
    },
  },
  walk: {
    success: {
      trust: 15,
      bond: 25,
      feeling: 'content',
      cue: 'sigh',
      pose: 'walk',
      holdMs: 1800,
      resultLine: (s) => `每次回頭，你都輕聲應了。${dogLabel(s)} 的步子漸漸穩下來。`,
      reactionLine: (s) => `${dogLabel(s)} 走在你腳邊，不再那麼頻繁回頭。`,
      memory: 'walk_calm',
    },
    partial: {
      trust: 10,
      bond: 15,
      feeling: 'anxious',
      cue: 'huff',
      pose: 'walk',
      holdMs: 1500,
      resultLine: (s) => `有些時刻對上了，有些還來不及。${dogLabel(s)} 仍走幾步就回頭。`,
      reactionLine: (s) => `${dogLabel(s)} 停了一下，確認你還在，才繼續往前。`,
    },
    struggle: {
      trust: 5,
      bond: 8,
      feeling: 'hurt',
      cue: 'whimper',
      pose: 'walk',
      holdMs: 1400,
      resultLine: (s) => `街上太吵，好幾次回頭你來不及應。${dogLabel(s)} 的繩子還是繃著。`,
      reactionLine: (s) => `${dogLabel(s)} 夾緊尾巴，走幾步就僵住。`,
    },
  },
  shop: {
    perfect: {
      trust: 8,
      bond: 20,
      feeling: 'curious',
      cue: null,
      holdMs: 2000,
      resultLine: () => '店員點點頭：「全對耶。幼犬第一天，該有的都有了。」',
      reactionLine: () => '你心裡鬆了一點——至少沒有買錯。',
      memory: 'shop_perfect',
    },
    good: {
      trust: 6,
      bond: 15,
      feeling: 'curious',
      cue: null,
      holdMs: 1800,
      resultLine: () => '店員把購物袋理好：「差不多齊了，差的我幫你補。」',
      reactionLine: () => '紙箱慢慢沉下來，裡面終於有了「家」該有的味道。',
    },
    partial: {
      trust: 4,
      bond: 10,
      feeling: 'anxious',
      cue: null,
      holdMs: 1600,
      resultLine: () => '店員替你換了兩樣：「這個幼犬不能吃——還好你問了我。」',
      reactionLine: () => '你臉有點熱，但心裡還是慶幸：總算沒白跑。',
    },
    miss: {
      trust: 2,
      bond: 6,
      feeling: 'hurt',
      cue: null,
      holdMs: 1500,
      resultLine: () => '店員嘆口氣，重新幫你拿：「別急，第一次都會亂。交給阿姨。」',
      reactionLine: () => '你點點頭，把每一項都記進手機備忘錄。',
    },
  },
  vet: {
    perfect: {
      trust: 12,
      bond: 18,
      feeling: 'content',
      cue: 'breathEase',
      pose: 'knee',
      holdMs: 1800,
      resultLine: (s) => `問診和檢查都順利結束。${dogLabel(s)} 在你懷裡打了個小哈欠，身子慢慢鬆下來。`,
      reactionLine: (s) => `${dogLabel(s)} 輕輕舔了舔你的袖口——濕濕的，很小的一下。`,
    },
    good: {
      trust: 10,
      bond: 15,
      feeling: 'curious',
      cue: 'sniff',
      pose: 'shy',
      holdMs: 1600,
      resultLine: (s) => `大部分你都答對了。${dogLabel(s)} 還有些緊，但沒有掙開你的懷抱。`,
      reactionLine: (s) => `${dogLabel(s)} 把鼻子埋在你肩窩，呼吸一聲比一聲慢。`,
    },
    partial: {
      trust: 6,
      bond: 10,
      feeling: 'anxious',
      cue: 'softWhimper',
      pose: 'shy',
      holdMs: 1500,
      resultLine: (s) => `有些問題還答不完整。量體重時 ${dogLabel(s)} 抖了一下，你抱得更穩。`,
      reactionLine: (s) => `${dogLabel(s)} 耳朵還貼著，尾巴慢慢垂下來——至少你在這裡。`,
    },
    miss: {
      trust: 4,
      bond: 6,
      feeling: 'hurt',
      cue: 'whimper',
      pose: 'corner',
      holdMs: 1400,
      resultLine: (s) => `檢查時有些手忙腳亂。${dogLabel(s)} 縮成一團，整個身子都繃著。`,
      reactionLine: (s) => `${dogLabel(s)} 只從你的袖子後面探出半雙眼睛。`,
    },
  },
  home: {
    perfect: {
      trust: 15,
      bond: 22,
      feeling: 'content',
      cue: 'sigh',
      pose: 'attached',
      holdMs: 2000,
      resultLine: (s) => `一圈走下來，${dogLabel(s)} 在你懷裡完全鬆了。\n沙發、食盆、床邊、陽台——${dogPronoun(s)} 各記下一種屬於這裡的味道。`,
      reactionLine: (s) => `${dogLabel(s)} 把下巴擱在你膝上，像說：這裡，好像真的可以。`,
      memory: 'home_scent',
    },
    good: {
      trust: 12,
      bond: 18,
      feeling: 'curious',
      cue: 'sniffDeep',
      pose: 'home',
      holdMs: 1800,
      resultLine: (s) => `大部分角落都認過了。${dogLabel(s)} 經過食盆時會停一下，像在確認飯會在這裡。`,
      reactionLine: (s) => `${dogLabel(s)} 鼻子在你頸邊輕輕嗅，沒有再掙開。`,
    },
    partial: {
      trust: 8,
      bond: 12,
      feeling: 'shy',
      cue: 'huff',
      pose: 'corner',
      holdMs: 1600,
      resultLine: (s) => `只認了幾個地方，${dogLabel(s)} 還有些緊。\n但 ${dogPronoun(s)} 願意靠著你，沒有躲回紙箱。`,
      reactionLine: (s) => `${dogLabel(s)} 把臉藏在你臂彎，只露出鼻尖。`,
    },
    miss: {
      trust: 5,
      bond: 8,
      feeling: 'anxious',
      cue: 'softWhimper',
      pose: 'corner',
      holdMs: 1500,
      resultLine: (s) => `有些角落太陌生，${dogLabel(s)} 整路繃著。\n你沒有催，只是抱緊一點，讓 ${dogPronoun(s)} 聽見你的心跳。`,
      reactionLine: (s) => `${dogLabel(s)} 身子還是僵的，但沒有掙開。`,
    },
  },
  thunder: {
    perfect: {
      trust: 12,
      bond: 18,
      feeling: 'content',
      cue: 'breathEase',
      pose: 'knee',
      holdMs: 2000,
      resultLine: (s) => `雷聲還在遠處滾，但桌底的顫抖漸漸停了。\n${dogLabel(s)} 把鼻子貼向你的手心，呼吸一聲比一聲慢。`,
      reactionLine: (s) => `${dogLabel(s)} 從桌底探出半張臉，呼吸和你同步。`,
    },
    good: {
      trust: 10,
      bond: 14,
      feeling: 'content',
      cue: 'whineSoft',
      pose: 'knee',
      holdMs: 1800,
      resultLine: (s) => `大部分時刻你都選對了。\n${dogLabel(s)} 還縮著，但嗚聲一聲比一聲輕——怕還在，沒有剛才那麼急。`,
      reactionLine: (s) => `${dogLabel(s)} 用鼻尖碰了碰你的指節，很小的一下。`,
    },
    partial: {
      trust: 6,
      bond: 10,
      feeling: 'anxious',
      cue: 'softWhimper',
      pose: 'thunder',
      holdMs: 1600,
      resultLine: (s) => `有幾次選對了，有幾次 ${dogLabel(s)} 還是被嚇得更深。\n你沒有責怪，只是再試一次。`,
      reactionLine: (s) => `${dogLabel(s)} 仍在桌底，但尾巴沒有夾得那麼死。`,
    },
    miss: {
      trust: 3,
      bond: 6,
      feeling: 'hurt',
      cue: 'whimperScared',
      pose: 'thunder',
      holdMs: 1500,
      resultLine: (s) => `好幾次選錯，${dogLabel(s)} 整個縮成一小團。\n你停下來，深吸一口氣——還來得及換方式。`,
      reactionLine: (s) => `${dogLabel(s)} 只從桌布邊緣露出顫抖的耳尖。`,
    },
  },
};

function computePottyTier(score, rounds) {
  if (score >= rounds) return 'perfect';
  if (score >= 2) return 'good';
  if (score >= 1) return 'partial';
  return 'miss';
}

function computeShopTier(score, rounds) {
  if (score >= rounds) return 'perfect';
  if (score >= rounds - 1) return 'good';
  if (score >= 2) return 'partial';
  return 'miss';
}

function computeVetTier(score, rounds) {
  return computeShopTier(score, rounds);
}

function computeHomeTier(score, rounds) {
  return computeShopTier(score, rounds);
}

function computeThunderTier(score, rounds) {
  return computeShopTier(score, rounds);
}

function computeWalkTier(finalCalm) {
  if (finalCalm >= 100) return 'success';
  if (finalCalm >= 50) return 'partial';
  return 'struggle';
}

function lookupMinigameOutcome(type, tier) {
  return MINIGAME_OUTCOMES[type]?.[tier] || null;
}

function applyMinigameOutcome(state, type, tier, extra = {}) {
  const out = lookupMinigameOutcome(type, tier);
  if (!out) return null;

  applyTrust(state, out.trust);
  applyBondProgress(state, out.bond);
  if (out.feeling) setFeeling(state, out.feeling);

  if (type === 'potty') {
    state.flags.pottyGuideTier = tier;
    state.flags.pottyGuideScore = tier === 'perfect' ? 3 : tier === 'good' ? 2 : tier === 'partial' ? 1 : 0;
  } else if (type === 'walk') {
    state.flags.walkGuideTier = tier;
    state.flags.walkGuideCalm = tier === 'success' ? 100 : tier === 'partial' ? 50 : 0;
  } else if (type === 'shop') {
    state.flags.shopTier = tier;
    state.flags.shopScore = extra.score ?? 0;
    state.flags.suppliesBought = true;
  } else if (type === 'vet') {
    state.flags.vetTier = tier;
    state.flags.vetScore = extra.score ?? 0;
  } else if (type === 'home') {
    state.flags.homeExploreTier = tier;
    state.flags.homeExploreScore = extra.score ?? 0;
  } else if (type === 'thunder') {
    state.flags.thunderComfortTier = tier;
    state.flags.thunderComfortScore = extra.score ?? 0;
  }

  if (out.memory) addMemory(state, out.memory);

  return out;
}

function resolvePottyAfternoonCopy(state) {
  const tier = state.flags.pottyGuideTier;
  const name = dogLabel(state);
  if (!tier) {
    return `午後很長，也很安靜。\n光從百葉窗漏進來，在地磚上畫出慢慢移動的條紋。\n\n${name} 在客廳來回嗅聞，\n開始記得：哪裡是門、哪裡是窩、\n哪裡是你常坐、會發出輕聲的位置。`;
  }
  if (tier === 'miss') {
    return `午後很長。\n${name} 大多縮在角落，對尿墊仍有些猶豫。\n\n你沒有嘆氣，只是把墊子再鋪平一點。\n還在試——\n找對的時機，找對的方式，\n找一種不會把彼此嚇到的距離。`;
  }
  if (tier === 'partial') {
    return `午後很長，也很安靜。\n${name} 在客廳和尿墊之間來回，\n像還在確認規則。\n\n有一點進步，但還沒完全放心。\n你坐在不遠處，\n讓牠知道：著急沒關係，可以慢慢來。`;
  }
  if (tier === 'good') {
    return `午後很長，也很安靜。\n${name} 在客廳來回嗅聞，\n經過尿墊時會停一下。\n\n開始記得：哪裡是門、哪裡是窩、\n哪裡是你常坐的位置。`;
  }
  return `午後很長，也很安靜。\n${name} 在客廳來回嗅聞，\n經過尿墊時會停一下——\n像終於把「對的地方」記進身體裡。\n\n你沒有說「做得好」，\n只是輕輕摸了摸牠的背。\n有些進步，適合小聲一點。`;
}

function resolveWalkParkCopy(state) {
  const tier = state.flags.walkGuideTier;
  const name = dogLabel(state);
  if (!tier) {
    return `小公園。\n${name} 把鼻子埋進樹根旁的土裡，吸得很深。\n\n這大概是牠第一次，\n認真「聞」這個世界——\n不是恐懼裡的嗅探，\n而是好奇裡的停留。`;
  }
  if (tier === 'struggle') {
    return `小公園到了，但 ${name} 仍走幾步就回頭。\n\n樹根旁的泥土味很誘人，\n牠卻不敢埋太久。\n\n你坐在長椅邊，不催。\n街上太吵，這一步還沒完全穩——\n但願意來到這裡，\n本身就已經很勇敢。`;
  }
  if (tier === 'partial') {
    return `小公園。\n${name} 把鼻子探向樹根旁的土裡，又回頭看你。\n\n確認你在，才敢再聞深一點——\n這大概是牠第一次，\n認真「聞」這個世界。\n\n風從樹葉間穿過，\n把害怕吹淡了一點點。`;
  }
  return `小公園。\n${name} 把鼻子埋進樹根旁的土裡，吸得很深。\n\n剛才街上的緊繃鬆了一點——\n你們在這裡待了一會，\n誰也沒有急著離開。\n\n這大概是牠第一次，\n認真「聞」這個世界，\n而且覺得：好像也可以。`;
}

function resolvePottyAfternoonFeeling(state) {
  const tier = state.flags.pottyGuideTier;
  if (!tier) return 'content';
  if (tier === 'miss') return 'anxious';
  if (tier === 'partial') return 'curious';
  if (tier === 'good') return 'curious';
  return 'content';
}

function resolveWalkParkFeeling(state) {
  const tier = state.flags.walkGuideTier;
  if (!tier) return 'curious';
  if (tier === 'struggle') return 'anxious';
  if (tier === 'partial') return 'curious';
  return 'content';
}

if (typeof module !== 'undefined') {
  module.exports = {
    MINIGAME_OUTCOMES,
    computePottyTier,
    computeWalkTier,
    computeShopTier,
    computeVetTier,
    computeHomeTier,
    computeThunderTier,
    lookupMinigameOutcome,
    applyMinigameOutcome,
    resolvePottyAfternoonCopy,
    resolveWalkParkCopy,
    resolvePottyAfternoonFeeling,
    resolveWalkParkFeeling,
  };
}
