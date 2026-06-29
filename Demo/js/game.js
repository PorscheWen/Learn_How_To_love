/* Learn How to Love — Demo engine */
(function () {
  const els = {
    app: document.getElementById('app'),
    scene: document.getElementById('scene'),
    sceneBg: document.getElementById('scene-bg'),
    dayLabel: document.getElementById('day-label'),
    locationLabel: document.getElementById('location-label'),
    smellText: document.getElementById('smell-text'),
    smellBar: document.getElementById('smell-bar'),
    dog: document.getElementById('dog'),
    dogStage: document.getElementById('dog-stage'),
    dogImg: document.getElementById('dog-img'),
    dogBehavior: document.getElementById('dog-behavior'),
    sceneArt: document.getElementById('scene-art'),
    narrativeText: document.getElementById('narrative-text'),
    narrativeSub: document.getElementById('narrative-sub'),
    subtitleViewport: document.getElementById('subtitle-viewport'),
    subtitleBox: document.querySelector('.subtitle-box'),
    textSpeedSelect: document.getElementById('text-speed-select'),
    introTextSpeed: document.getElementById('intro-text-speed'),
    dayJumpSelect: document.getElementById('day-jump-select'),
    introDayJump: document.getElementById('intro-day-jump'),
    choices: document.getElementById('choices'),
    minigame: document.getElementById('minigame'),
    bondDots: document.querySelectorAll('.bond-dots .dot'),
    bondName: document.getElementById('bond-name'),
    introDialog: document.getElementById('intro-dialog'),
    albumDialog: document.getElementById('album-dialog'),
    albumList: document.getElementById('album-list'),
    albumMoments: document.getElementById('album-moments'),
    albumMomentsHint: document.getElementById('album-moments-hint'),
    momentViewDialog: document.getElementById('moment-view-dialog'),
    momentViewImg: document.getElementById('moment-view-img'),
    momentViewCaption: document.getElementById('moment-view-caption'),
  };

  let state = createInitialState();
  let typingAbort = null;
  let delaySkipper = null;
  let sceneFlowToken = 0;
  let smellAnimToken = 0;
  let musicStarted = false;
  const SCENE_BREATH_MS = 1200;
  const SCENE_ART_DIR = 'assets/scene';
  const DAY2_BREATH_MS = 2600;
  const DAY2_TEXT_MULT = 1.5;
  const PETTING_FEELINGS = new Set(['content', 'sleepy', 'attached']);
  const PETTING_MIN_DRAG = 26;
  const PETTING_TRUST_GAIN = 1;
  const PETTING_COOLDOWN_MS = 1500;

  let pettingState = {
    sceneId: '',
    rewarded: false,
    pointerDown: false,
    dragDist: 0,
    lastX: 0,
    lastY: 0,
  };
  let pettingCooldownUntil = 0;

  const SHOP_ROUNDS = [
    {
      prompt: '主食：幼犬該吃哪一種？',
      options: [
        { label: '幼犬專用糧', icon: '🐾', ok: true },
        { label: '成犬減重糧', icon: '⚖️', ok: false },
        { label: '貓主食罐', icon: '🥫', ok: false },
      ],
    },
    {
      prompt: '如廁：該準備什麼？',
      options: [
        { label: '幼犬尿墊', icon: '🧻', ok: true },
        { label: '報紙', icon: '📰', ok: false },
        { label: '貓砂', icon: '🐈', ok: false },
      ],
    },
    {
      prompt: '食盆：哪個適合幼犬？',
      options: [
        { label: '淺口防滑碗', icon: '🍽️', ok: true },
        { label: '深口大盆', icon: '🍲', ok: false },
        { label: '馬克杯', icon: '☕', ok: false },
      ],
    },
    {
      prompt: '睡覺：牠需要什麼？',
      options: [
        { label: '小毯子', icon: '🧣', ok: true },
        { label: '硬塑膠屋', icon: '🏠', ok: false },
        { label: '空紙箱就好', icon: '📦', ok: false },
      ],
    },
    {
      prompt: '玩具：可以買哪個？',
      options: [
        { label: '幼犬磨牙玩具', icon: '🎾', ok: true },
        { label: '雞骨頭', icon: '🦴', ok: false },
        { label: '人類零食', icon: '🍪', ok: false },
      ],
    },
  ];

  const VET_ROUNDS = [
    {
      prompt: '醫師：「最近食慾怎麼樣？每一餐都有吃到嗎？」',
      options: [
        { label: '還在適應，有時只吃幾口但願意試', icon: '🍽️', ok: true },
        { label: '不吃也沒關係，餓幾餐就好', icon: '🙅', ok: false },
        { label: '人類零食比較肯吃', icon: '🍪', ok: false },
      ],
    },
    {
      prompt: '醫師：「睡覺會不會驚醒？半夜會叫嗎？」',
      options: [
        { label: '第一週會叫、會醒，我有在陪', icon: '🌙', ok: true },
        { label: '從來不叫，睡得都很好', icon: '😴', ok: false },
        { label: '叫的話關起來不理就好', icon: '🚪', ok: false },
      ],
    },
    {
      prompt: '醫師：「排便正常嗎？有沒有軟便或腹瀉？」',
      options: [
        { label: '大多正常，偶爾還在找對的地方', icon: '🧻', ok: true },
        { label: '沒特別注意過', icon: '🤷', ok: false },
        { label: '小時候應該不用管', icon: '🙈', ok: false },
      ],
    },
    {
      prompt: '醫師：「之前有打過疫苗或驅蟲嗎？有帶紀錄嗎？」',
      options: [
        { label: '不太清楚，請醫師依檢查幫我排', icon: '📋', ok: true },
        { label: '應該都打完了吧', icon: '✨', ok: false },
        { label: '朋友說幼犬還不用', icon: '💬', ok: false },
      ],
    },
    {
      prompt: '醫師：「幼犬依規定應該接種哪些疫苗？你記一下。」',
      options: [
        { label: '核心疫苗（犬瘟、小病毒等）依時程，狂犬病到期再打', icon: '💉', ok: true },
        { label: '只要打狂犬病，其他的不用', icon: '🐕', ok: false },
        { label: '看起來健康就不用打', icon: '⏭️', ok: false },
      ],
    },
    {
      prompt: '醫師：「有沒有嘔吐、一直抓癢，或皮膚紅腫？」',
      options: [
        { label: '目前沒有，但我會繼續留意', icon: '👀', ok: true },
        { label: '沒看到就不用說', icon: '🙈', ok: false },
        { label: '抓癢應該是正常的', icon: '🐾', ok: false },
      ],
    },
    {
      prompt: '量體重時牠發抖——醫師說：「你可以怎麼做？」',
      options: [
        { label: '輕撫、小聲安撫，讓牠聞我的味道', icon: '🤲', ok: true },
        { label: '放手讓牠自己站在秤上', icon: '🙅', ok: false },
        { label: '大聲說「沒什麼好怕的」', icon: '📢', ok: false },
      ],
    },
    {
      prompt: '醫師：「疫苗和驅蟲要按時，回診日你會怎麼記？」',
      options: [
        { label: '記下日期、設手機提醒', icon: '📅', ok: true },
        { label: '聽過就忘，應該記得住', icon: '🎲', ok: false },
        { label: '有空再去就好', icon: '⏳', ok: false },
      ],
    },
  ];

  const HOME_ROUNDS = [
    {
      prompt: '先從哪裡開始認家？',
      options: [
        { label: '客廳沙發', icon: '🛋️', ok: true },
        { label: '門外走廊', icon: '🚪', ok: false },
        { label: '儲物間深處', icon: '📦', ok: false },
      ],
    },
    {
      prompt: '接下來帶牠聞哪裡？',
      options: [
        { label: '食盆位置', icon: '🍽️', ok: true },
        { label: '垃圾桶', icon: '🗑️', ok: false },
        { label: '洗衣機後面', icon: '🧺', ok: false },
      ],
    },
    {
      prompt: '讓牠記住「你在哪裡睡」？',
      options: [
        { label: '臥室床邊', icon: '🛏️', ok: true },
        { label: '浴室馬桶', icon: '🚽', ok: false },
        { label: '鞋櫃深處', icon: '👟', ok: false },
      ],
    },
    {
      prompt: '最後認一認外面的氣味？',
      options: [
        { label: '陽台欄杆', icon: '☀️', ok: true },
        { label: '窗縫外的車聲', icon: '🚗', ok: false },
        { label: '鄰居門口', icon: '🏢', ok: false },
      ],
    },
  ];

  const THUNDER_ROUNDS = [
    {
      prompt: '第一下雷聲滚過來，桌底下的身子抖得更厲害……',
      options: [
        {
          label: '開小夜燈，輕聲：「我在。」',
          icon: '🕯️',
          ok: true,
          react: {
            feeling: 'anxious',
            cue: 'whineSoft',
            line: (s) => `${dogLabel(s)} 的嗚聲短了一拍，像有聽見你。`,
          },
        },
        {
          label: '「沒什麼好怕的！」大聲說',
          icon: '📢',
          ok: false,
          react: {
            feeling: 'hurt',
            cue: 'whimperScared',
            line: (s) => `${dogLabel(s)} 縮得更深，耳朵貼平。`,
          },
        },
        {
          label: '硬把牠從桌底拉出來',
          icon: '✋',
          ok: false,
          react: {
            feeling: 'hurt',
            cue: 'whimper',
            line: (s) => `${dogLabel(s)} 掙了一下，整個身子繃得更緊。`,
          },
        },
      ],
    },
    {
      prompt: '閃電又亮了一下，桌底下的呼吸亂了節奏……',
      options: [
        {
          label: '坐在地上，伸手讓牠聞你的氣味',
          icon: '🤲',
          ok: true,
          react: {
            feeling: 'shy',
            cue: 'sniffQuick',
            line: (s) => `${dogLabel(s)} 的鼻尖探出桌布邊緣，小心地嗅了嗅。`,
          },
        },
        {
          label: '把所有燈都打開',
          icon: '💡',
          ok: false,
          react: {
            feeling: 'alert',
            cue: 'huff',
            line: (s) => `${dogLabel(s)} 被光嚇到，整個縮回去。`,
          },
        },
        {
          label: '拿手機拍照記錄',
          icon: '📱',
          ok: false,
          react: {
            feeling: 'hurt',
            cue: 'whimperQuiet',
            line: (s) => `${dogLabel(s)} 對閃光屏的亮嚇了一跳。`,
          },
        },
      ],
    },
    {
      prompt: '連續的雷聲，尾巴夾得死緊……',
      options: [
        {
          label: '用薄毯蓋住桌口，隔開一點光',
          icon: '🧣',
          ok: true,
          react: {
            feeling: 'content',
            cue: 'breathEase',
            line: (s) => `${dogLabel(s)} 在毯子下呼吸慢了一點。`,
          },
        },
        {
          label: '放音樂試圖蓋過雷聲',
          icon: '🎵',
          ok: false,
          react: {
            feeling: 'alert',
            cue: 'whimperScared',
            line: (s) => `${dogLabel(s)} 對突然變大的聲音更慌了。`,
          },
        },
        {
          label: '去關窗，留牠一個',
          icon: '🪟',
          ok: false,
          react: {
            feeling: 'anxious',
            cue: 'whineSoft',
            line: (s) => `${dogLabel(s)} 聽見你離開的腳步，嗚得更急。`,
          },
        },
      ],
    },
    {
      prompt: '雨勢變大，敲在窗上。桌底只剩顫抖……',
      options: [
        {
          label: '輕拍地面，陪著等雷過去',
          icon: '👋',
          ok: true,
          react: {
            feeling: 'content',
            cue: 'sleepBreath',
            line: (s) => `${dogLabel(s)} 的顫抖和你的拍子漸漸對上。`,
          },
        },
        {
          label: '責備：「別吵了。」',
          icon: '😤',
          ok: false,
          react: {
            feeling: 'hurt',
            cue: 'whimper',
            line: (s) => `${dogLabel(s)} 把臉藏起來，連嗚聲都壓住了。`,
          },
        },
        {
          label: '戴耳機，當作沒聽見',
          icon: '🎧',
          ok: false,
          react: {
            feeling: 'anxious',
            cue: 'softWhimper',
            line: (s) => `${dogLabel(s)} 獨自承受每一聲雷，身子抖個不停。`,
          },
        },
      ],
    },
  ];

  function sceneBreathMs(scene) {
    if (scene.breathMs) return scene.breathMs;
    return scene.day === 2 ? DAY2_BREATH_MS : SCENE_BREATH_MS;
  }

  function sceneTextMult(scene) {
    if (scene.textMult) return scene.textMult;
    return scene.day === 2 ? DAY2_TEXT_MULT : 1;
  }

  function minigameTitle(type) {
    if (type === 'potty') return '如廁引導';
    if (type === 'walk') return '散步 · 確認你還在';
    if (type === 'shop') return '寵物店 · 挑選用品';
    if (type === 'vet') return '醫師問診 · 配合回答';
    if (type === 'home') return '認識家 · 氣味地圖';
    if (type === 'thunder') return '雷雨 · 安撫';
    return '小遊戲';
  }


  function renderSmellBar(state, visibleCount, highlightLast) {
    if (!els.smellText) return;
    const layers = state.smellLayers || parseSmellString(state.smell);
    const total = visibleCount ?? layers.length;
    els.smellText.innerHTML = '';
    for (let i = 0; i < total && i < layers.length; i += 1) {
      if (i > 0) els.smellText.appendChild(document.createTextNode('、'));
      const span = document.createElement('span');
      span.className = 'smell-note';
      if (highlightLast && i === total - 1) span.classList.add('smell-note-new');
      span.textContent = layers[i];
      els.smellText.appendChild(span);
    }
  }

  function delay(ms) {
    return new Promise((resolve) => { setTimeout(resolve, ms); });
  }

  function clearSkippableDelay() {
    if (delaySkipper) {
      delaySkipper();
      delaySkipper = null;
    }
  }

  function setAdvanceable(on) {
    els.subtitleBox?.classList.toggle('is-advanceable', !!on);
  }

  function skippableDelay(ms) {
    if (ms <= 0 || getTextSpeedPreset().instant) return Promise.resolve();
    return new Promise((resolve) => {
      clearSkippableDelay();
      setAdvanceable(true);
      const timerId = setTimeout(() => {
        delaySkipper = null;
        setAdvanceable(!!typingAbort);
        resolve();
      }, ms);
      delaySkipper = () => {
        clearTimeout(timerId);
        delaySkipper = null;
        setAdvanceable(!!typingAbort);
        resolve();
      };
    });
  }

  function isTypingOrWaiting() {
    return !!(typingAbort || delaySkipper);
  }

  function canAdvanceStoryStep() {
    if (els.introDialog?.open) return false;
    const ae = document.activeElement;
    const tag = ae?.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return false;
    if (els.choices?.dataset.busy === '1') return false;
    if (els.minigame && !els.minigame.classList.contains('hidden')) return false;
    if (!isTypingOrWaiting()) {
      if (els.choices?.childElementCount > 0) return false;
      return false;
    }
    return true;
  }

  function hasVisibleChoices() {
    return !!els.choices?.childElementCount;
  }

  function canPetDogNow() {
    const scene = SCENES[state.sceneId];
    if (!scene) return false;
    if (isTypingOrWaiting()) return false;
    if (hasVisibleChoices()) return false;
    if (els.minigame && !els.minigame.classList.contains('hidden')) return false;
    if (!PETTING_FEELINGS.has(state.feeling)) return false;
    if (scene.hideDog || !isDogAudioEnabled(scene)) return false;
    if (els.dogStage?.classList.contains('is-hidden')) return false;
    if (els.dogImg?.classList.contains('dog-img-hidden')) return false;
    return true;
  }

  function updatePettingAvailability() {
    const canPet = canPetDogNow();
    els.dog?.classList.toggle('is-pettable', canPet);
  }

  function endPettingGesture() {
    pettingState.pointerDown = false;
    pettingState.dragDist = 0;
  }

  function triggerPettingFeedback() {
    const now = Date.now();
    if (now < pettingCooldownUntil) return;

    const scene = SCENES[state.sceneId];
    if (!scene || !canPetDogNow()) return;

    pettingCooldownUntil = now + PETTING_COOLDOWN_MS;
    els.dog?.classList.add('is-petting');
    setTimeout(() => els.dog?.classList.remove('is-petting'), 380);

    if (typeof DogSounds !== 'undefined' && isDogAudioEnabled(scene)) {
      DogSounds.playCue('breathEase', { source: 'petting', sceneId: state.sceneId });
    }

    els.dogBehavior.textContent = applyDogPronouns(
      `${dogLabel(state)} 瞇起眼睛，呼吸慢慢貼上你的節奏。`,
      state,
    );

    if (!pettingState.rewarded) {
      applyTrust(state, PETTING_TRUST_GAIN);
      pettingState.rewarded = true;
      saveGame(state);
    }

    setTimeout(() => {
      if (state.sceneId !== pettingState.sceneId) return;
      updateDogVisual(scene);
    }, 980);
  }

  function bindPettingControls() {
    if (!els.dog) return;

    els.dog.addEventListener('pointerdown', (e) => {
      if (e.button !== 0) return;
      if (!canPetDogNow()) return;
      pettingState.pointerDown = true;
      pettingState.dragDist = 0;
      pettingState.lastX = e.clientX;
      pettingState.lastY = e.clientY;
      try { els.dog.setPointerCapture(e.pointerId); } catch (_) {}
    });

    els.dog.addEventListener('pointermove', (e) => {
      if (!pettingState.pointerDown) return;
      const dx = e.clientX - pettingState.lastX;
      const dy = e.clientY - pettingState.lastY;
      pettingState.lastX = e.clientX;
      pettingState.lastY = e.clientY;
      pettingState.dragDist += Math.hypot(dx, dy);
      if (pettingState.dragDist >= PETTING_MIN_DRAG) {
        triggerPettingFeedback();
        pettingState.dragDist = 0;
      }
    });

    els.dog.addEventListener('pointerup', () => endPettingGesture());
    els.dog.addEventListener('pointercancel', () => endPettingGesture());
    els.dog.addEventListener('pointerleave', () => endPettingGesture());
  }

  function advanceStoryStep() {
    if (!canAdvanceStoryStep()) return;
    AmbientMusic.playAdvanceTick?.();
    if (typingAbort) {
      typingAbort();
      return;
    }
    if (delaySkipper) delaySkipper();
  }

  function bindAdvanceControls() {
    const onKey = (e) => {
      if (e.code !== 'Space') return;
      if (!canAdvanceStoryStep()) return;
      e.preventDefault();
      advanceStoryStep();
    };
    document.addEventListener('keydown', onKey);

    const onContext = (e) => {
      if (!canAdvanceStoryStep()) return;
      e.preventDefault();
      advanceStoryStep();
    };
    els.app?.addEventListener('contextmenu', onContext);

    els.subtitleBox?.addEventListener('click', () => {
      if (canAdvanceStoryStep()) advanceStoryStep();
    });
  }

  async function updateSmellUI(scene) {
    const token = ++smellAnimToken;
    if (!state.smellLayers) state.smellLayers = parseSmellString(state.smell);

    if (scene.smell) {
      setSmellLayers(state, resolveText(scene.smell, state));
      renderSmellBar(state);
      els.smellBar?.classList.remove('is-revealing');
      return;
    }

    const rawAdds = scene.smellAdd;
    const adds = rawAdds
      ? (Array.isArray(rawAdds) ? rawAdds : [rawAdds]).map((a) => resolveText(a, state))
      : [];
    let added = 0;
    adds.forEach((note) => {
      if (addSmellLayer(state, note)) added += 1;
    });

    if (!added) {
      renderSmellBar(state);
      return;
    }

    els.smellBar?.classList.add('is-revealing');
    const startCount = state.smellLayers.length - added;
    renderSmellBar(state, startCount);

    for (let i = 0; i < added; i += 1) {
      await delay(i === 0 ? 900 : 1500);
      if (token !== smellAnimToken) return;
      renderSmellBar(state, startCount + i + 1, true);
    }
  }

  function syncSpeedUI() {
    const id = getTextSpeedId();
    if (els.textSpeedSelect) els.textSpeedSelect.value = id;
    if (els.introTextSpeed) els.introTextSpeed.value = id;
  }

  function abortTyping() {
    if (typingAbort) {
      typingAbort();
      typingAbort = null;
    }
    els.narrativeText?.classList.remove('is-revealing');
    els.narrativeSub?.classList.remove('is-revealing');
    els.subtitleBox?.classList.remove('is-scrolling');
    setAdvanceable(!!delaySkipper);
    updatePettingAvailability();
  }

  function scrollSubtitleToBottom() {
    const vp = els.subtitleViewport;
    if (!vp) return;
    vp.scrollTop = Math.max(0, vp.scrollHeight - vp.clientHeight);
  }

  function resetSubtitleScroll() {
    if (els.subtitleViewport) els.subtitleViewport.scrollTop = 0;
  }

  function applyNarrativeHtml(el, plain) {
    const html = formatDayLabels(plain).replace(/\n/g, '<br>');
    el.innerHTML = html;
  }

  function updateDayLabel(scene) {
    if (!els.dayLabel) return;
    if (scene?.isEpilogue) {
      els.dayLabel.innerHTML = '<strong class="day-tag">Day 7</strong> · End';
      return;
    }
    const day = scene?.day ?? state.day ?? 1;
    els.dayLabel.innerHTML = `<strong class="day-tag">Day ${day}</strong>`;
  }

  function updateSceneArt(scene) {
    if (!els.sceneArt) return;
    const key = scene?.noSceneArt ? null : scene?.sceneArt;
    if (key) {
      els.sceneArt.onerror = () => {
        els.sceneArt.classList.add('hidden', 'is-missing');
        els.sceneArt.removeAttribute('src');
      };
      els.sceneArt.onload = () => {
        els.sceneArt.classList.remove('is-missing');
      };
      els.sceneArt.src = `${SCENE_ART_DIR}/scene-${key}.png`;
      // 敘事已在字幕 text/sub；勿把 sceneArtAlt 設為 alt（破圖時會顯示在背景上）
      els.sceneArt.alt = '';
      els.sceneArt.removeAttribute('aria-label');
      els.sceneArt.setAttribute('aria-hidden', 'true');
      els.sceneArt.classList.remove('hidden');
    } else {
      els.sceneArt.classList.add('hidden');
      els.sceneArt.classList.remove('is-missing');
      els.sceneArt.removeAttribute('src');
      els.sceneArt.alt = '';
      els.sceneArt.setAttribute('aria-hidden', 'true');
    }
  }

  /**
   * Reveal text char-by-char; viewport scrolls as content grows.
   * @returns {Promise<void>}
   */
  function scrollRevealText(el, text, options = {}) {
    abortTyping();
    const content = text == null ? '' : String(text);
    el.textContent = '';
    el.classList.add('is-revealing');
    els.subtitleBox?.classList.add('is-scrolling');
    setAdvanceable(true);
    updatePettingAvailability();

    const preset = getTextSpeedPreset();
    const paceMult = options.paceMult ?? 1;
    const mult = (options.subtitle ? preset.subMult : 1) * paceMult;

    if (preset.instant) {
      applyNarrativeHtml(el, content);
      el.classList.remove('is-revealing');
      scrollSubtitleToBottom();
      els.subtitleBox?.classList.remove('is-scrolling');
      setAdvanceable(!!delaySkipper);
      updatePettingAvailability();
      return Promise.resolve();
    }

    return new Promise((resolve) => {
      let i = 0;
      let cancelled = false;
      let timerId = null;

      const finish = () => {
        if (cancelled) return;
        cancelled = true;
        if (timerId) clearTimeout(timerId);
        applyNarrativeHtml(el, content);
        el.classList.remove('is-revealing');
        scrollSubtitleToBottom();
        els.subtitleBox?.classList.remove('is-scrolling');
        typingAbort = null;
        setAdvanceable(!!delaySkipper);
        updatePettingAvailability();
        resolve();
      };

      typingAbort = finish;

      const step = () => {
        if (cancelled || i >= content.length) {
          finish();
          return;
        }
        el.textContent = content.slice(0, i + 1);
        scrollSubtitleToBottom();
        const ch = content[i];
        i += 1;
        timerId = setTimeout(step, delayForChar(ch, preset, mult));
      };

      timerId = setTimeout(step, preset.base * 0.6);
    });
  }

  function startMusicForScene(scene) {
    return ensureGameAudio(scene);
  }

  async function ensureGameAudio(scene) {
    try {
      await AmbientMusic.unlock();
      await DogSounds.preload?.();
    } catch (e) {
      console.warn('[Game] Audio unlock:', e);
    }
    const s = scene || SCENES[state.sceneId] || {};
    const { profile } = AmbientMusic.profileForScene(s);
    if (!musicStarted) {
      AmbientMusic.start(profile);
      musicStarted = true;
      updateMusicBtn();
    } else {
      AmbientMusic.setProfile(profile);
    }
    AmbientMusic.setSceneAmbience?.(s);
  }

  function updateMusicBtn() {
    const btn = document.getElementById('btn-music');
    if (!btn) return;
    btn.textContent = AmbientMusic.isEnabled() ? '🎵' : '🔇';
    btn.title = AmbientMusic.isEnabled() ? '關閉背景音樂與狗聲' : '開啟背景音樂與狗聲';
  }

  function stopGameAudio() {
    AmbientMusic.shutdown();
    DogSounds.stop();
    musicStarted = false;
    updateMusicBtn();
  }

  function updateSceneVisual(scene) {
    const loc = scene.location || 'living_room';
    const meta = LOCATIONS[loc] || { label: '未知', icon: '' };
    els.sceneBg.className = 'scene-bg loc-' + loc;
    els.locationLabel.textContent = (meta.icon ? meta.icon + ' ' : '') + meta.label;

    const decor = document.getElementById('scene-decor');
    if (decor) {
      decor.className = 'scene-decor';
      if (loc === 'living_storm' || scene.music === 'storm') decor.classList.add('decor-storm');
      else if (loc === 'prologue_rain' || loc === 'window_rain' || scene.weather === 'rain') decor.classList.add('decor-rain');
      else if (loc === 'street_sunset') decor.classList.add('decor-sunset');
      else if (loc === 'living_warm' || scene.feeling === 'attached') decor.classList.add('decor-warm');
    }

    const hideDog = scene.hideDog || loc === 'balcony' || loc === 'pet_shop' || loc === 'office';
    if (els.dogStage) {
      els.dogStage.classList.toggle('is-hidden', hideDog);
    }
    if (els.dogImg) {
      els.dogImg.classList.toggle('dog-img-hidden', loc === 'balcony' || hideDog);
    }
    if (els.scene) {
      els.scene.classList.toggle('has-scene-art', hideDog && !!scene.sceneArt);
    }
    if (els.dogBehavior) {
      els.dogBehavior.classList.toggle('is-hidden', hideDog);
    }
  }

  function resolveText(fnOrStr, s) {
    const raw = typeof fnOrStr === 'function' ? fnOrStr(s) : (fnOrStr || '');
    return applyDogPronouns(raw, s);
  }

  function resolveNext(next, s) {
    if (typeof next === 'function') return next(s);
    return next;
  }

  function updateDogVisual(scene) {
    const visual = resolveDogVisual(scene, state);
    els.dog.className = 'dog mood-' + visual.moodClass;
    if (els.dogImg) {
      els.dogImg.src = visual.src;
      els.dogImg.alt = visual.behavior;
    }
    const caption = visual.behavior;
    els.dogBehavior.textContent = applyDogPronouns(caption, state);
    els.app.classList.remove('cold', 'content');
    if (visual.temp === 'cold') els.app.classList.add('cold');
    if (visual.temp === 'content') els.app.classList.add('content');
    updatePettingAvailability();
  }

  function flashDogReact() {
    els.dog?.classList.remove('is-react');
    void els.dog?.offsetWidth;
    els.dog?.classList.add('is-react');
  }

  function shouldStormThunderOnChoice(scene) {
    if (!scene) return false;
    if (scene.id === 'day6_thunder') return true;
    if (scene.id === 'day6_check' && state._thunderEligible) return true;
    return false;
  }

  async function playChoiceReaction(choice, scene, before) {
    const ctx = {
      beforeFeeling: before.feeling,
      beforeTrust: before.trust,
      afterFeeling: state.feeling,
      trustDelta: state.trust - before.trust,
      sceneId: scene.id,
      scene,
      choice,
    };
    const reaction = StoryAgent.resolve(choice, state, ctx);
    if (!reaction) return;

    const reactScene = {
      ...scene,
      feeling: reaction.feeling,
      dogPose: reaction.pose || scene.dogPose,
    };
    updateDogVisual(reactScene);
    els.dogBehavior.textContent = applyDogPronouns(reaction.text, state);
    if (scene.hideDog) {
      els.dogBehavior.classList.remove('is-hidden');
      els.dogBehavior.classList.add('is-choice-react');
    }
    flashDogReact();

    await delay(reaction.cueDelay);
    if (reaction.cue && typeof DogSounds !== 'undefined') {
      DogSounds.playCue(reaction.cue, { source: 'choice', sceneId: ctx?.sceneId });
    }
    await delay(reaction.holdMs);
    if (scene.hideDog) {
      els.dogBehavior.classList.add('is-hidden');
      els.dogBehavior.classList.remove('is-choice-react');
    }
  }

  function syncDogAudio(scene) {
    if (typeof DogSounds === 'undefined' || !scene) return;
    DogSounds.onScene(scene, state);
  }

  function triggerDay6ThunderIntro(scene) {
    if (scene?.id !== 'day6_thunder') return;
    if (typeof AmbientMusic === 'undefined' || typeof DogSounds === 'undefined') return;
    const roll = AmbientMusic.playThunderIntro?.({ volumeScale: 3 });
    const scaredDelay = roll?.peakAt != null
      ? Math.round(roll.peakAt * 1000 + 160)
      : 400;
    setTimeout(() => {
      if (state.sceneId !== 'day6_thunder') return;
      DogSounds.playThunderScaredSequence?.();
      updateDogVisual({ ...scene, dogPose: 'thunder', feeling: 'alert' });
      flashDogReact();
    }, scaredDelay);
  }

  function updateBondUI() {
    els.bondDots.forEach((dot) => {
      const lv = parseInt(dot.dataset.lv, 10);
      dot.classList.toggle('active', lv <= state.bondLevel);
    });
    els.bondName.textContent = BOND_NAMES[state.bondLevel] || '陌生';
  }

  async function playSceneText(mainText, subText, onDone, options = {}) {
    const flowToken = sceneFlowToken;
    els.narrativeSub.textContent = '';
    resetSubtitleScroll();
    const paceMult = options.paceMult ?? 1;
    await scrollRevealText(els.narrativeText, mainText, { paceMult });
    if (flowToken !== sceneFlowToken) return;
    if (subText) {
      const preset = getTextSpeedPreset();
      await skippableDelay(preset.pauseMajor * 0.85 * paceMult);
      if (flowToken !== sceneFlowToken) return;
      await scrollRevealText(els.narrativeSub, subText, { subtitle: true, paceMult });
    }
    if (flowToken !== sceneFlowToken) return;
    setAdvanceable(false);
    onDone?.();
  }

  function updateChoicesLayout() {
    const hasChoices = els.choices.childElementCount > 0;
    els.scene?.classList.toggle('has-choices', hasChoices);
    updatePettingAvailability();
  }

  function clearUI() {
    sceneFlowToken += 1;
    abortTyping();
    clearSkippableDelay();
    setAdvanceable(false);
    els.choices.innerHTML = '';
    els.minigame.innerHTML = '';
    els.minigame.classList.add('hidden');
    els.narrativeText.textContent = '';
    els.narrativeSub.textContent = '';
    els.narrativeText.classList.remove('is-revealing');
    els.narrativeSub.classList.remove('is-revealing');
    resetSubtitleScroll();
    updateSceneArt({});
    updateChoicesLayout();
    updatePettingAvailability();
  }

  function showNamePrompt() {
    const wrap = document.createElement('div');
    wrap.className = 'name-prompt fade-in';
    wrap.innerHTML = `
      <label class="name-prompt-label">替牠取名字：
        <input type="text" id="scene-dog-name" maxlength="12" placeholder="例如：豆花" autocomplete="off">
      </label>
      <button type="button" class="choice-btn" id="name-confirm">記住這個名字</button>
    `;
    els.choices.appendChild(wrap);
    updateChoicesLayout();

    const input = wrap.querySelector('#scene-dog-name');
    input.focus();

    return new Promise((resolve) => {
      const confirm = () => {
        setDogProfile(state, input.value.trim() || '豆花', null);
        saveGame(state);
        resolve();
      };
      wrap.querySelector('#name-confirm').addEventListener('click', confirm);
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') confirm();
      });
    });
  }

  function showGenderPrompt() {
    const wrap = document.createElement('div');
    wrap.className = 'name-prompt fade-in';
    wrap.innerHTML = `
      <p class="name-gender-lead">店員問：「是弟弟還是妹妹？」</p>
      <fieldset class="name-gender-field">
        <legend class="name-gender-legend">選一個就好</legend>
        <div class="name-gender-options">
          <label class="name-gender-option"><input type="radio" name="dog-gender" value="male"> 🐶 弟弟</label>
          <label class="name-gender-option"><input type="radio" name="dog-gender" value="female"> 🎀 妹妹</label>
        </div>
      </fieldset>
      <button type="button" class="choice-btn" id="gender-confirm">記下來</button>
    `;
    els.choices.appendChild(wrap);
    updateChoicesLayout();

    return new Promise((resolve) => {
      const confirm = () => {
        const gender = readGenderFromPrompt(wrap);
        if (!gender) {
          wrap.querySelector('.name-gender-field')?.classList.add('name-gender-missing');
          return;
        }
        setDogGender(state, gender);
        saveGame(state);
        resolve();
      };
      wrap.querySelector('#gender-confirm').addEventListener('click', confirm);
      wrap.querySelectorAll('input[name="dog-gender"]').forEach((el) => {
        el.addEventListener('change', () => {
          wrap.querySelector('.name-gender-field')?.classList.remove('name-gender-missing');
        });
      });
    });
  }

  function readGenderFromPrompt(wrap) {
    const checked = wrap.querySelector('input[name="dog-gender"]:checked');
    return checked?.value === 'female' ? 'female' : checked?.value === 'male' ? 'male' : null;
  }

  function showGenderOnlyPrompt() {
    const wrap = document.createElement('div');
    wrap.className = 'name-prompt fade-in';
    wrap.innerHTML = `
      <p class="name-gender-lead">${dogLabel(state)} 是弟弟還是妹妹？</p>
      <fieldset class="name-gender-field">
        <legend class="name-gender-legend">選一個就好</legend>
        <div class="name-gender-options">
          <label class="name-gender-option"><input type="radio" name="dog-gender" value="male"> 🐶 弟弟</label>
          <label class="name-gender-option"><input type="radio" name="dog-gender" value="female"> 🎀 妹妹</label>
        </div>
      </fieldset>
      <button type="button" class="choice-btn" id="gender-confirm">記下來</button>
    `;
    els.choices.innerHTML = '';
    els.choices.appendChild(wrap);
    updateChoicesLayout();

    return new Promise((resolve) => {
      const confirm = () => {
        const gender = readGenderFromPrompt(wrap);
        if (!gender) {
          wrap.querySelector('.name-gender-field')?.classList.add('name-gender-missing');
          return;
        }
        setDogGender(state, gender);
        saveGame(state);
        els.choices.innerHTML = '';
        updateChoicesLayout();
        resolve();
      };
      wrap.querySelector('#gender-confirm').addEventListener('click', confirm);
      wrap.querySelectorAll('input[name="dog-gender"]').forEach((el) => {
        el.addEventListener('change', () => {
          wrap.querySelector('.name-gender-field')?.classList.remove('name-gender-missing');
        });
      });
    });
  }

  function showChoices(choiceList) {
    choiceList.forEach((c) => {
      const btn = document.createElement('button');
      btn.className = 'choice-btn fade-in';
      btn.textContent = applyDogPronouns(c.text, state);
      btn.addEventListener('click', async () => {
        if (els.choices.dataset.busy === '1') return;
        els.choices.dataset.busy = '1';
        els.choices.querySelectorAll('.choice-btn').forEach((b) => { b.disabled = true; });

        const scene = SCENES[state.sceneId];
        const before = { feeling: state.feeling, trust: state.trust };
        c.effect?.(state);
        saveGame(state);

        try {
          if (shouldStormThunderOnChoice(scene)) {
            AmbientMusic.triggerStormThunderOnChoice?.();
          }
          await playChoiceReaction(c, scene, before);
        } catch (err) {
          console.warn('[StoryAgent]', err);
        }

        const nextId = resolveNext(c.next, state);
        els.choices.dataset.busy = '0';
        if (nextId) goToScene(nextId);
        else els.choices.querySelectorAll('.choice-btn').forEach((b) => { b.disabled = false; });
      });
      els.choices.appendChild(btn);
    });
    updateChoicesLayout();
  }

  async function playMinigameReaction(type, tier, scene, extra = {}) {
    const out = applyMinigameOutcome(state, type, tier, extra);
    if (!out) return;

    saveGame(state);
    updateBondUI();

    const reactScene = {
      ...scene,
      feeling: out.feeling,
      dogPose: out.pose || scene.dogPose,
    };
    updateDogVisual(reactScene);
    els.dogBehavior.textContent = applyDogPronouns(out.reactionLine(state), state);
    flashDogReact();

    els.minigame.classList.remove('hidden');
    els.minigame.innerHTML = `
      <h3>${minigameTitle(type)} · 結果</h3>
      <p class="minigame-result">${applyDogPronouns(out.resultLine(state), state)}</p>
    `;

    await delay(480);
    if (out.cue && isDogAudioEnabled(scene) && typeof DogSounds !== 'undefined') {
      DogSounds.playCue(out.cue);
    }
    await delay(out.holdMs ?? 2000);
    if (type === 'thunder' && isDogAudioEnabled(scene) && typeof DogSounds !== 'undefined') {
      DogSounds.playThunderCalmSequence?.(tier);
      if (tier === 'perfect' || tier === 'good') {
        setFeeling(state, 'content');
        updateDogVisual({ ...scene, feeling: 'content', dogPose: 'knee' });
        els.dogBehavior.textContent = applyDogPronouns(
          `${dogLabel(state)} 的顫抖停了，呼吸和你同步。`,
          state,
        );
        flashDogReact();
      }
      await delay(tier === 'perfect' || tier === 'good' ? 2400 : 1700);
    }
    els.minigame.classList.add('hidden');
  }

  function runPottyMinigame(onComplete) {
    updateDogVisual({ ...SCENES[state.sceneId], dogPose: 'potty', feeling: state.feeling });
    els.minigame.classList.remove('hidden');
    let score = 0;
    let round = 0;
    const rounds = 3;

    function showRoundFeedback(success) {
      const hint = document.getElementById('potty-hint');
      if (hint) {
        hint.textContent = success ? '對上了！' : '來不及……';
        hint.className = success ? 'potty-hint ok' : 'potty-hint miss';
      }
    }

    function renderRound() {
      els.minigame.innerHTML = `
        <h3>如廁引導</h3>
        <p>當 ${dogLabel(state)} 低頭嗅地面時，輕點帶牠走向尿墊。（${round + 1}/${rounds}）</p>
        <p id="potty-hint" class="potty-hint"></p>
        <div class="meter"><div class="meter-fill" id="potty-meter" style="width:${(score / rounds) * 100}%"></div></div>
        <div class="timing-game" id="potty-zones"></div>
      `;
      const zones = document.getElementById('potty-zones');
      const highlightIdx = Math.floor(Math.random() * 4);
      let clicked = false;

      for (let i = 0; i < 4; i += 1) {
        const b = document.createElement('button');
        b.className = 'timing-btn';
        b.textContent = '🐾';
        b.dataset.idx = i;
        zones.appendChild(b);
      }

      setTimeout(() => {
        zones.children[highlightIdx]?.classList.add('highlight');
        const timeout = setTimeout(() => {
          if (!clicked) nextRound(false);
        }, 2200);

        zones.querySelectorAll('.timing-btn').forEach((btn) => {
          btn.addEventListener('click', () => {
            if (clicked) return;
            clicked = true;
            clearTimeout(timeout);
            const ok = parseInt(btn.dataset.idx, 10) === highlightIdx;
            nextRound(ok);
          });
        });
      }, 800 + Math.random() * 600);
    }

    function nextRound(success) {
      if (success) score += 1;
      showRoundFeedback(success);
      round += 1;
      if (round >= rounds) {
        const tier = computePottyTier(score, rounds);
        setTimeout(() => onComplete({ type: 'potty', tier, score, rounds }), success ? 520 : 680);
      } else {
        setTimeout(() => renderRound(), 680);
      }
    }

    renderRound();
  }

  function runShopMinigame(onComplete) {
    els.minigame.classList.remove('hidden');
    let score = 0;
    let round = 0;
    const rounds = SHOP_ROUNDS.length;

    function showFeedback(ok) {
      const hint = document.getElementById('shop-hint');
      if (!hint) return;
      hint.textContent = ok ? '店員：「對啦，幼犬就是要用這個。」' : '店員：「這個不行喔——再想想？」';
      hint.className = ok ? 'shop-hint ok' : 'shop-hint miss';
    }

    function renderRound() {
      const data = SHOP_ROUNDS[round];
      els.minigame.innerHTML = `
        <h3>寵物店 · 挑選用品</h3>
        <p class="shop-prompt">${data.prompt}（${round + 1}/${rounds}）</p>
        <p id="shop-hint" class="shop-hint"></p>
        <div class="meter"><div class="meter-fill" id="shop-meter" style="width:${(score / rounds) * 100}%"></div></div>
        <div class="shop-grid" id="shop-grid"></div>
      `;
      const grid = document.getElementById('shop-grid');
      let locked = false;

      data.options.forEach((opt) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'shop-item fade-in';
        btn.innerHTML = `<span class="shop-icon">${opt.icon}</span><span class="shop-label">${opt.label}</span>`;
        btn.addEventListener('click', () => {
          if (locked) return;
          locked = true;
          grid.querySelectorAll('.shop-item').forEach((b) => { b.disabled = true; });
          btn.classList.add(opt.ok ? 'is-ok' : 'is-miss');
          if (!opt.ok) {
            const correct = [...grid.querySelectorAll('.shop-item')].find((b, i) => data.options[i].ok);
            correct?.classList.add('is-ok');
          }
          showFeedback(opt.ok);
          setTimeout(() => nextRound(opt.ok), opt.ok ? 720 : 980);
        });
        grid.appendChild(btn);
      });
    }

    function nextRound(success) {
      if (success) score += 1;
      round += 1;
      if (round >= rounds) {
        const tier = computeShopTier(score, rounds);
        setTimeout(() => onComplete({ type: 'shop', tier, score, rounds }), 640);
      } else {
        setTimeout(() => renderRound(), 520);
      }
    }

    renderRound();
  }

  function runQuizMinigame(config, onComplete) {
    const { title, rounds: roundData, hintOk, hintMiss, computeTier, type } = config;
    els.minigame.classList.remove('hidden');
    let score = 0;
    let round = 0;
    const rounds = roundData.length;

    function showFeedback(ok) {
      const hint = document.getElementById('shop-hint');
      if (!hint) return;
      hint.textContent = ok ? hintOk : hintMiss;
      hint.className = ok ? 'shop-hint ok' : 'shop-hint miss';
    }

    function renderRound() {
      const data = roundData[round];
      els.minigame.innerHTML = `
        <h3>${title}</h3>
        <p class="shop-prompt">${data.prompt}（${round + 1}/${rounds}）</p>
        <p id="shop-hint" class="shop-hint"></p>
        <div class="meter"><div class="meter-fill" id="shop-meter" style="width:${(score / rounds) * 100}%"></div></div>
        <div class="shop-grid" id="shop-grid"></div>
      `;
      const grid = document.getElementById('shop-grid');
      let locked = false;

      data.options.forEach((opt) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'shop-item fade-in';
        btn.innerHTML = `<span class="shop-icon">${opt.icon}</span><span class="shop-label">${opt.label}</span>`;
        btn.addEventListener('click', () => {
          if (locked) return;
          locked = true;
          grid.querySelectorAll('.shop-item').forEach((b) => { b.disabled = true; });
          btn.classList.add(opt.ok ? 'is-ok' : 'is-miss');
          if (!opt.ok) {
            const correct = [...grid.querySelectorAll('.shop-item')].find((b, i) => data.options[i].ok);
            correct?.classList.add('is-ok');
          }
          showFeedback(opt.ok);
          setTimeout(() => nextRound(opt.ok), opt.ok ? 720 : 980);
        });
        grid.appendChild(btn);
      });
    }

    function nextRound(success) {
      if (success) score += 1;
      round += 1;
      if (round >= rounds) {
        const tier = computeTier(score, rounds);
        setTimeout(() => onComplete({ type, tier, score, rounds }), 640);
      } else {
        setTimeout(() => renderRound(), 520);
      }
    }

    renderRound();
  }

  function runVetMinigame(onComplete) {
    runQuizMinigame({
      title: '醫師問診 · 配合回答',
      rounds: VET_ROUNDS,
      type: 'vet',
      hintOk: '醫師：「好，這樣我比較掌握狀況。」',
      hintMiss: '醫師：「這部分很重要——再想想？」',
      computeTier: computeVetTier,
    }, onComplete);
  }

  function runHomeExploreMinigame(onComplete) {
    runQuizMinigame({
      title: '認識家 · 氣味地圖',
      rounds: HOME_ROUNDS,
      type: 'home',
      hintOk: '「對，這裡有你的味道。」',
      hintMiss: '這裡還太陌生——換一個牠能安心的角落？',
      computeTier: computeHomeTier,
    }, onComplete);
  }

  async function playThunderRoundReact(opt, scene) {
    if (!opt?.react) return;
    const reactScene = {
      ...scene,
      feeling: opt.react.feeling,
      dogPose: opt.react.pose || 'thunder',
    };
    updateDogVisual(reactScene);
    const line = typeof opt.react.line === 'function' ? opt.react.line(state) : opt.react.line;
    els.dogBehavior.textContent = applyDogPronouns(line, state);
    flashDogReact();
    if (opt.react.cue && isDogAudioEnabled(scene) && typeof DogSounds !== 'undefined') {
      DogSounds.playCue(opt.react.cue, { source: 'minigame', sceneId: scene.id });
    }
    await delay(opt.ok ? 880 : 1080);
  }

  function runThunderComfortMinigame(onComplete) {
    updateDogVisual({ ...SCENES[state.sceneId], dogPose: 'thunder', feeling: 'alert' });
    els.minigame.classList.remove('hidden');
    let score = 0;
    let round = 0;
    const rounds = THUNDER_ROUNDS.length;
    const scene = SCENES[state.sceneId];

    function showFeedback(ok) {
      const hint = document.getElementById('thunder-hint');
      if (!hint) return;
      hint.textContent = ok ? '牠的呼吸慢了一點。' : '這樣只會更怕——試試別的方式？';
      hint.className = ok ? 'shop-hint ok' : 'shop-hint miss';
    }

    function renderRound() {
      const data = THUNDER_ROUNDS[round];
      els.minigame.innerHTML = `
        <h3>雷雨 · 安撫</h3>
        <p class="shop-prompt thunder-prompt">${data.prompt}（${round + 1}/${rounds}）</p>
        <p id="thunder-hint" class="shop-hint"></p>
        <div class="meter"><div class="meter-fill" id="thunder-meter" style="width:${(score / rounds) * 100}%"></div></div>
        <div class="shop-grid" id="thunder-grid"></div>
      `;
      const grid = document.getElementById('thunder-grid');
      let locked = false;

      data.options.forEach((opt) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'shop-item fade-in';
        btn.innerHTML = `<span class="shop-icon">${opt.icon}</span><span class="shop-label">${opt.label}</span>`;
        btn.addEventListener('click', () => {
          if (locked) return;
          locked = true;
          grid.querySelectorAll('.shop-item').forEach((b) => { b.disabled = true; });
          btn.classList.add(opt.ok ? 'is-ok' : 'is-miss');
          if (!opt.ok) {
            const correct = [...grid.querySelectorAll('.shop-item')].find((b, i) => data.options[i].ok);
            correct?.classList.add('is-ok');
          }
          showFeedback(opt.ok);
          playThunderRoundReact(opt, scene).then(() => {
            nextRound(opt.ok);
          });
        });
        grid.appendChild(btn);
      });
    }

    function nextRound(success) {
      if (success) score += 1;
      round += 1;
      if (round >= rounds) {
        const tier = computeThunderTier(score, rounds);
        setTimeout(() => onComplete({ type: 'thunder', tier, score, rounds }), 640);
      } else {
        setTimeout(() => renderRound(), 480);
      }
    }

    renderRound();
  }

  function runWalkMinigame(onComplete) {
    updateDogVisual({ ...SCENES[state.sceneId], dogPose: 'walk', feeling: state.feeling });
    els.minigame.classList.remove('hidden');
    let calm = 0;
    const target = 100;
    let decayId;
    let lookBackId;
    let lookBackActive = false;

    els.minigame.innerHTML = `
      <h3>散步 · 確認你還在</h3>
      <p>當 ${dogLabel(state)} 回頭看你時（按鈕發光），按住「輕聲喚牠」。不要拉緊繩子。</p>
      <div class="meter"><div class="meter-fill" id="walk-meter" style="width:0%"></div></div>
      <button class="hold-btn" id="walk-hold">輕聲喚牠（按住）</button>
      <p id="walk-hint" class="walk-hint">等 ${dogLabel(state)} 回頭……</p>
    `;

    const meter = document.getElementById('walk-meter');
    const hold = document.getElementById('walk-hold');
    const hint = document.getElementById('walk-hint');
    let holding = false;

    let finished = false;
    const finish = (finalCalm) => {
      if (finished) return;
      finished = true;
      clearInterval(decayId);
      clearInterval(tickId);
      clearInterval(lookBackId);
      clearTimeout(failSafe);
      const tier = computeWalkTier(finalCalm);
      onComplete({ type: 'walk', tier, calm: finalCalm });
    };

    function setLookBack(active) {
      lookBackActive = active;
      hold.classList.toggle('look-back', active);
      if (hint) {
        hint.textContent = active
          ? `${dogLabel(state)} 回頭看你——輕聲喚牠！`
          : `等 ${dogLabel(state)} 回頭……`;
        hint.classList.toggle('active', active);
      }
      if (active && typeof DogSounds !== 'undefined') DogSounds.playCue('huff');
    }

    function pulseLookBack() {
      if (finished) return;
      setLookBack(true);
      setTimeout(() => {
        if (!finished) setLookBack(false);
      }, 1800);
    }

    lookBackId = setInterval(pulseLookBack, 3500);
    pulseLookBack();

    decayId = setInterval(() => {
      if (!holding && calm > 0) calm = Math.max(0, calm - 3);
      meter.style.width = calm + '%';
      if (calm >= target) finish(calm);
    }, 120);

    const start = () => { holding = true; };
    const end = () => { holding = false; };
    const tickId = setInterval(() => {
      if (holding) {
        const gain = lookBackActive ? 9 : 1;
        calm = Math.min(target, calm + gain);
        meter.style.width = calm + '%';
        if (calm >= target) finish(calm);
      }
    }, 100);

    hold.addEventListener('mousedown', start);
    hold.addEventListener('mouseup', end);
    hold.addEventListener('mouseleave', end);
    hold.addEventListener('touchstart', (e) => { e.preventDefault(); start(); });
    hold.addEventListener('touchend', end);

    const failSafe = setTimeout(() => {
      finish(calm);
    }, 45000);
  }

  function renderEpilogue() {
    clearUI();
    updateSceneVisual(SCENES.epilogue);
    updateDogVisual(SCENES.epilogue);
    startMusicForScene(SCENES.epilogue);
    syncDogAudio(SCENES.epilogue);
    updateSmellUI(SCENES.epilogue);
    els.dayLabel.innerHTML = '<strong class="day-tag">Day 7</strong> · End';
    const payload = exportSaveJson(state);

    playSceneText(
      resolveText(SCENES.epilogue.text, state),
      resolveText(SCENES.epilogue.sub, state),
      () => {
        const personal = buildEpiloguePersonalLines(state);
        const card = document.createElement('div');
        card.className = 'epilogue-card fade-in';
        card.innerHTML = `
          <p class="epilogue-kicker">Demo · First Steps</p>
          <p class="epilogue-line">${dogLabel(state)} 與你走過這七天。</p>
          <p class="epilogue-line epilogue-muted">相簿裡多了 ${state.memories.length} 個腳印 · 時刻快照 ${state.capturedMoments?.length || 0} 張 · 羈絆 ${BOND_NAMES[state.bondLevel] || '陌生'}</p>
          ${personal.map((line) => `<p class="epilogue-line epilogue-personal">${line}</p>`).join('')}
          <div class="epilogue-actions">
            <button class="choice-btn" id="copy-save">複製本趟歷程</button>
            <button class="choice-btn" id="restart-demo">再玩一次</button>
            <button class="choice-btn epilogue-link-btn" id="btn-music-credits-epilogue" type="button">音樂來源</button>
          </div>
        `;
        els.choices.appendChild(card);
        updateChoicesLayout();
        document.getElementById('copy-save').addEventListener('click', () => {
          navigator.clipboard?.writeText(payload).then(() => {
            const btn = document.getElementById('copy-save');
            if (btn) {
              const prev = btn.textContent;
              btn.textContent = '已複製';
              setTimeout(() => { btn.textContent = prev; }, 1800);
            }
          });
        });
        document.getElementById('restart-demo').addEventListener('click', async () => {
          stopGameAudio();
          clearUI();
          localStorage.removeItem(SAVE_KEY);
          localStorage.removeItem(SAVE_KEY_LEGACY);
          await resetMomentGallery(state);
          state = createInitialState();
          ensureMomentSession(state);
          els.introDialog.showModal();
          syncSpeedUI();
        });
        document.getElementById('btn-music-credits-epilogue')?.addEventListener('click', showMusicCreditsDialog);
      }
    );
    saveGame(state);
  }

  async function goToScene(sceneId) {
    const scene = SCENES[sceneId];
    if (!scene) return;

    state.sceneId = sceneId;
    state.day = scene.day;
    pettingState = {
      sceneId,
      rewarded: false,
      pointerDown: false,
      dragDist: 0,
      lastX: 0,
      lastY: 0,
    };
    pettingCooldownUntil = 0;
    clearUI();

    updateSceneVisual(scene);
    updateSceneArt(scene);
    await startMusicForScene(scene);

    if (scene.isEpilogue) {
      renderEpilogue();
      return;
    }

    if (scene.feeling) {
      const feeling = typeof scene.feeling === 'function' ? scene.feeling(state) : scene.feeling;
      setFeeling(state, feeling);
    }
    scene.onEnter?.(state);
    updateDogVisual(scene);
    syncDogAudio(scene);
    triggerDay6ThunderIntro(scene);
    updateBondUI();
    updateDayLabel(scene);
    updateSmellUI(scene);

    if (needsGenderPrompt(scene, state)) {
      await showGenderOnlyPrompt();
    }

    const sessionId = ensureMomentSession(state);
    MomentGallery.scheduleCapture(sessionId, scene, state, (sceneId) => {
      if (!state.capturedMoments.includes(sceneId)) {
        state.capturedMoments.push(sceneId);
        saveGame(state);
      }
    });

    const mainText = resolveText(scene.text, state);
    const subText = resolveText(scene.sub, state);

    playSceneText(mainText, subText, async () => {
      const flowToken = sceneFlowToken;
      const breathMs = sceneBreathMs(scene);
      const paceMult = sceneTextMult(scene);
      await skippableDelay(breathMs);
      if (flowToken !== sceneFlowToken) return;
      if (scene.minigame === 'potty') {
        runPottyMinigame(async (result) => {
          try {
            await playMinigameReaction(result.type, result.tier, scene, { score: result.score });
          } catch (err) {
            console.warn('[Minigame]', err);
          }
          goToScene(scene.next);
        });
        return;
      }
      if (scene.minigame === 'shop') {
        runShopMinigame(async (result) => {
          try {
            await playMinigameReaction(result.type, result.tier, scene, { score: result.score });
          } catch (err) {
            console.warn('[Minigame]', err);
          }
          goToScene(scene.next);
        });
        return;
      }
      if (scene.minigame === 'vet') {
        runVetMinigame(async (result) => {
          try {
            await playMinigameReaction(result.type, result.tier, scene, { score: result.score });
          } catch (err) {
            console.warn('[Minigame]', err);
          }
          goToScene(scene.next);
        });
        return;
      }
      if (scene.minigame === 'home') {
        runHomeExploreMinigame(async (result) => {
          try {
            await playMinigameReaction(result.type, result.tier, scene, { score: result.score });
          } catch (err) {
            console.warn('[Minigame]', err);
          }
          goToScene(scene.next);
        });
        return;
      }
      if (scene.minigame === 'walk') {
        runWalkMinigame(async (result) => {
          try {
            await playMinigameReaction(result.type, result.tier, scene, { calm: result.calm });
          } catch (err) {
            console.warn('[Minigame]', err);
          }
          goToScene(scene.next);
        });
        return;
      }
      if (scene.minigame === 'thunder') {
        runThunderComfortMinigame(async (result) => {
          try {
            await playMinigameReaction(result.type, result.tier, scene, { score: result.score });
          } catch (err) {
            console.warn('[Minigame]', err);
          }
          if (scene.choices) showChoices(scene.choices);
        });
        return;
      }

      if (scene.namePrompt) {
        await showNamePrompt();
        goToScene(scene.next);
        return;
      }

      if (scene.genderPrompt) {
        await showGenderPrompt();
        goToScene(scene.next);
        return;
      }

      if (scene.choices) showChoices(scene.choices);
    }, { paceMult: sceneTextMult(scene) });

    saveGame(state);
  }

  function setAlbumTab(tabId) {
    els.albumDialog?.querySelectorAll('.album-tab').forEach((btn) => {
      const active = btn.dataset.tab === tabId;
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-selected', active ? 'true' : 'false');
    });
    els.albumList?.classList.toggle('hidden', tabId !== 'memories');
    els.albumMoments?.classList.toggle('hidden', tabId !== 'moments');
    els.albumMomentsHint?.classList.toggle('hidden', tabId !== 'moments');
  }

  function openMomentViewer(record) {
    if (!record || !els.momentViewDialog) return;
    els.momentViewImg.src = record.dataUrl;
    els.momentViewCaption.textContent = record.caption || record.sceneId;
    els.momentViewDialog.dataset.downloadName = `lhtl-day${record.day}-${record.sceneId}.jpg`;
    els.momentViewDialog.showModal();
  }

  async function renderAlbumMoments() {
    if (!els.albumMoments) return;
    els.albumMoments.innerHTML = '';
    const sessionId = ensureMomentSession(state);
    const items = await MomentGallery.listForSession(sessionId);
    if (!items.length) {
      const empty = document.createElement('p');
      empty.className = 'album-moments-empty';
      empty.textContent = '還沒有快照。繼續旅程，每個場景都會自動收藏。';
      els.albumMoments.appendChild(empty);
      return;
    }
    items.forEach((record) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'moment-thumb';
      btn.innerHTML = `
        <img src="${record.dataUrl}" alt="${record.caption || ''}" loading="lazy">
        <span class="moment-thumb-label">${record.caption || record.sceneId}</span>
      `;
      btn.addEventListener('click', () => openMomentViewer(record));
      els.albumMoments.appendChild(btn);
    });
  }

  function renderAlbum() {
    setAlbumTab('memories');
    els.albumList.innerHTML = '';
    Object.entries(ALBUM_ENTRIES).forEach(([id, entry]) => {
      const li = document.createElement('li');
      const unlocked = state.memories.includes(id);
      li.className = unlocked ? '' : 'locked';
      li.textContent = unlocked ? `${entry.title} — ${entry.desc}` : `${entry.title} — 尚未解鎖`;
      els.albumList.appendChild(li);
    });
    renderAlbumMoments();
    els.albumDialog.showModal();
  }

  function normalizeSmellState(s) {
    if (!s.smellLayers?.length) {
      setSmellLayers(s, s.smell || '舊紙箱、雨、陌生的房間');
    }
  }

  function boot(saved) {
    if (saved) {
      state = migrateSaveState(saved);
      if (!state.playTimeStart) state.playTimeStart = Date.now();
      normalizeSmellState(state);
      ensureMomentSession(state);
    }
    syncSpeedUI();
    els.introDialog.showModal();
  }

  async function jumpToDay(key) {
    if (!key) return;
    const sceneId = applyDayJumpState(state, key);
    if (!sceneId || !SCENES[sceneId]) {
      alert('無法跳轉至該日');
      return;
    }
    abortTyping();
    els.minigame?.classList.add('hidden');
    els.choices.innerHTML = '';
    els.introDialog?.close();
    normalizeSmellState(state);
    musicStarted = false;
    await goToScene(sceneId);
    saveGame(state);
    if (els.dayJumpSelect) els.dayJumpSelect.value = '';
  }

  function applySpeedFromIntro() {
    const id = els.introTextSpeed?.value || DEFAULT_TEXT_SPEED;
    setTextSpeedId(id);
    syncSpeedUI();
  }

  bindAdvanceControls();
  bindPettingControls();

  els.textSpeedSelect?.addEventListener('change', (e) => {
    setTextSpeedId(e.target.value);
    syncSpeedUI();
  });

  els.dayJumpSelect?.addEventListener('change', async (e) => {
    const key = e.target.value;
    if (!key) return;
    await jumpToDay(key);
  });

  els.introTextSpeed?.addEventListener('change', (e) => {
    setTextSpeedId(e.target.value);
    syncSpeedUI();
  });

  document.getElementById('btn-continue').addEventListener('click', async () => {
    applySpeedFromIntro();
    let raw = null;
    try {
      const key = localStorage.getItem(SAVE_KEY) ? SAVE_KEY : SAVE_KEY_LEGACY;
      raw = JSON.parse(localStorage.getItem(key) || 'null');
    } catch (_) {}
    const saved = loadGame();
    if (saved && saved.sceneId) {
      if (raw && raw.sceneId !== saved.sceneId) {
        const label = LOCATIONS[saved.sceneId]?.label || saved.sceneId;
        alert(`故事已更新，將從「${label}」接續新章節（第一夜吹乾／請假·寵物店）。`);
      }
      state = saved;
      normalizeSmellState(state);
      els.introDialog.close();
      musicStarted = false;
      await goToScene(saved.sceneId);
    } else {
      alert('沒有存檔，請選「新開始」。');
    }
  });

  document.getElementById('btn-new').addEventListener('click', async () => {
    applySpeedFromIntro();
    const jumpKey = els.introDayJump?.value;
    localStorage.removeItem(SAVE_KEY);
    localStorage.removeItem(SAVE_KEY_LEGACY);
    await resetMomentGallery(state);
    state = createInitialState();
    ensureMomentSession(state);
    els.introDialog.close();
    musicStarted = false;
    if (jumpKey) {
      await jumpToDay(jumpKey);
    } else {
      await goToScene('prologue_rain');
    }
  });

  document.getElementById('btn-music').addEventListener('click', async () => {
    try {
      await AmbientMusic.unlock();
    } catch (_) {}
    if (!musicStarted) {
      const scene = SCENES[state.sceneId] || {};
      const { profile } = AmbientMusic.profileForScene(scene);
      AmbientMusic.start(profile);
      musicStarted = true;
      syncDogAudio(scene);
    } else {
      AmbientMusic.toggle();
    }
    updateMusicBtn();
  });

  document.getElementById('btn-album').addEventListener('click', renderAlbum);

  els.albumDialog?.querySelectorAll('.album-tab').forEach((btn) => {
    btn.addEventListener('click', () => {
      setAlbumTab(btn.dataset.tab);
      if (btn.dataset.tab === 'moments') renderAlbumMoments();
    });
  });

  document.getElementById('moment-download')?.addEventListener('click', () => {
    const src = els.momentViewImg?.src;
    if (!src) return;
    const name = els.momentViewDialog?.dataset.downloadName || 'lhtl-moment.jpg';
    const a = document.createElement('a');
    a.href = src;
    a.download = name;
    a.click();
  });
  document.getElementById('btn-music-credits-intro')?.addEventListener('click', showMusicCreditsDialog);
  document.getElementById('btn-save').addEventListener('click', () => {
    const json = exportSaveJson(state);
    navigator.clipboard?.writeText(json).then(() => alert('存檔 JSON 已複製到剪貼簿'));
  });

  window.addEventListener('pagehide', stopGameAudio);

  const saved = loadGame();
  boot(saved);
})();
