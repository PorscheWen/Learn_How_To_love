/**
 * Demo 內容流程架構 — 對照 Other_games.md「溫情互動」層
 *
 * 場景生命週期：
 *   narrative（打字）→ breath（留白／可撫摸）→ choice | minigame | prompt → 下一場景
 *
 * 手繪日記：memories（里程碑）+ moment-gallery（場景快照）由 game.js 串接
 */
const ContentFlow = (function () {
  const PHASE = Object.freeze({
    NARRATIVE: 'narrative',
    BREATH: 'breath',
    CHOICE: 'choice',
    MINIGAME: 'minigame',
    PROMPT: 'prompt',
    IDLE: 'idle',
  });

  /** 預設可撫摸情緒（呼吸空檔） */
  const PETTABLE_BASE = new Set(['content', 'sleepy', 'attached']);
  /** scene.pettable 時額外開放 */
  const PETTABLE_SOFT = new Set(['shy', 'curious', 'anxious', 'hurt', 'playful']);

  function resolvePhase(ctx) {
    if (ctx.typing) return PHASE.NARRATIVE;
    if (ctx.minigameOpen) return PHASE.MINIGAME;
    if (ctx.hasChoices) return PHASE.CHOICE;
    if (ctx.nameOrGenderPrompt) return PHASE.PROMPT;
    if (ctx.breathGap) return PHASE.BREATH;
    return PHASE.IDLE;
  }

  function pettableFeelings(scene) {
    const set = new Set(PETTABLE_BASE);
    if (scene?.pettable) {
      PETTABLE_SOFT.forEach((f) => set.add(f));
    }
    return set;
  }

  /**
   * @param {object} scene — SCENES 項目
   * @param {object} state — 遊戲狀態
   * @param {object} ctx — { typing, breathGap, hasChoices, minigameOpen, dogHidden, nameOrGenderPrompt }
   */
  function canPet(scene, state, ctx) {
    if (!scene || scene.hideDog || scene.noPetting) return false;
    if (ctx.dogHidden) return false;
    if (typeof isDogAudioEnabled === 'function' && !isDogAudioEnabled(scene)) return false;

    const phase = resolvePhase(ctx);
    if (phase === PHASE.NARRATIVE || phase === PHASE.MINIGAME || phase === PHASE.CHOICE || phase === PHASE.PROMPT) {
      return false;
    }

    const inBreath = phase === PHASE.BREATH;
    const inIdlePettable = phase === PHASE.IDLE && scene.pettable;
    if (!inBreath && !inIdlePettable) return false;

    const feeling = state?.feeling || scene.feeling;
    return pettableFeelings(scene).has(feeling);
  }

  function interactionHint(scene, phase, petAllowed) {
    if (!petAllowed || phase !== PHASE.BREATH) return '';
    return scene?.petHint || '文字停了一下——可以在空白裡，輕輕撫摸牠。';
  }

  /** 依故事天整理日記頁（ALBUM_ENTRIES 需含 day） */
  function groupAlbumByDay(entries, unlockedIds) {
    const groups = new Map();
    Object.entries(entries).forEach(([id, entry]) => {
      const day = entry.day ?? 0;
      if (!groups.has(day)) groups.set(day, []);
      groups.get(day).push({
        id,
        unlocked: unlockedIds.includes(id),
        title: entry.title,
        desc: entry.desc,
      });
    });
    return [...groups.entries()]
      .sort((a, b) => a[0] - b[0])
      .map(([day, items]) => ({ day, items }));
  }

  return {
    PHASE,
    resolvePhase,
    pettableFeelings,
    canPet,
    interactionHint,
    groupAlbumByDay,
  };
})();

if (typeof module !== 'undefined') module.exports = { ContentFlow };
