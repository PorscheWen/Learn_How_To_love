const SAVE_KEY = 'lhtl_demo_save_v2';
const SAVE_KEY_LEGACY = 'lhtl_demo_save_v1';
const DEMO_VERSION = '1.1';
const FLOW_VERSION = 5;

/** 主人固定班表：週一～五 08:00–17:00；週六日放假（Demo Ch1 基準） */
const OWNER_WORK_START_HOUR = 8;
const OWNER_WORK_END_HOUR = 17;

/**
 * Demo Ch1 故事天 ↔ 星期對照（Day 1＝週三傍晚帶回家）
 * atWork：該日是否為上班日；onLeave：整日請假（劇情明示）
 */
const DEMO_DAY_CALENDAR = {
  1: { isoWeekday: 3, label: '週三', atWork: false, note: '傍晚上班後帶回家' },
  2: { isoWeekday: 4, label: '週四', atWork: false, onLeave: true, note: '請假·寵物店' },
  3: { isoWeekday: 5, label: '週五', atWork: true, note: '正常上班·可提早離開' },
  4: { isoWeekday: 6, label: '週六', atWork: false, note: '週末·寵物醫院' },
  5: { isoWeekday: 7, label: '週日', atWork: false, note: '週末·認家' },
  6: { isoWeekday: 1, label: '週一', atWork: true, note: '正常上班·傍晚雷雨' },
  7: { isoWeekday: 2, label: '週二', atWork: true, note: '正常上班·可能比平常晚回家' },
};

function getDemoDayCalendar(storyDay) {
  return DEMO_DAY_CALENDAR[storyDay] || null;
}

function isOwnerWorkday(storyDay) {
  return getDemoDayCalendar(storyDay)?.atWork === true;
}

/** 該故事日是否為刻意請假／整日不在班（需劇情或 flags 明示） */
function isOwnerOnLeave(state, storyDay) {
  const cal = getDemoDayCalendar(storyDay);
  if (cal?.onLeave) return true;
  if (storyDay === 2 && state?.memories?.includes('day2_petshop')) return true;
  if (storyDay === 3 && state?.flags?.day3LeftEarly) return true;
  return false;
}

/**
 * 審查用：上班日 08:00–17:00 主人是否應在家
 * timeOfDay: 'morning' | 'midday' | 'evening'（morning=出門前, evening=下班後）
 */
function ownerShouldBeHome(storyDay, state, timeOfDay) {
  if (!isOwnerWorkday(storyDay)) return true;
  if (isOwnerOnLeave(state, storyDay)) return true;
  if (timeOfDay === 'morning' || timeOfDay === 'evening') return true;
  if (timeOfDay === 'midday') return false;
  return true;
}

const FEELINGS = {
  anxious: { mood: 'anxious', temp: 'cold', behavior: '蜷著身子，尾巴輕輕夾緊，像在等你的下一步。' },
  curious: { mood: 'curious', temp: 'warm', behavior: '豎著耳朵，小心地往前嗅。' },
  content: { mood: 'content', temp: 'content', behavior: '側躺著，呼吸緩慢，像終於放鬆。' },
  hurt: { mood: 'hurt', temp: 'cold', behavior: '夾著尾巴，視線偏向別處。' },
  excited: { mood: 'excited', temp: 'warm', behavior: '在門口來回轉圈，壓不住期待。' },
  attached: { mood: 'attached', temp: 'content', behavior: '輕輕靠過來，把頭停在你膝上。' },
  sleepy: { mood: 'sleepy', temp: 'content', behavior: '眼皮半闔，呼吸變長，像隨時會睡著。' },
  playful: { mood: 'playful', temp: 'warm', behavior: '前腳趴低、尾巴搖快，邀請你一起玩。' },
  alert: { mood: 'alert', temp: 'cold', behavior: '豎起耳朵，身體繃緊，在聽什麼。' },
  shy: { mood: 'shy', temp: 'cold', behavior: '把臉藏起來，只露出一點點鼻尖。' },
  hungry: { mood: 'hungry', temp: 'warm', behavior: '鼻子貼地，循著食物的氣味。' },
  angry: { mood: 'angry', temp: 'cold', behavior: '低低吼了一聲，還沒準備原諒。' },
};

/** 故事線專屬動作圖 — 對應 assets/dog/dog-{id}.png */
const DOG_POSES = {
  rain: { behavior: '在濕紙箱裡發抖，眼睛還不敢完全睜開。' },
  corner: { behavior: '縮在紙箱邊，把這一小塊當成安全邊界。' },
  kitchen: { behavior: '在碗邊嗅來嗅去，還不敢真的吃。' },
  potty: { behavior: '低頭嗅地面，在找「對的地方」。' },
  toy: { behavior: '叼著玩具跑回來，像在確認你還在。' },
  doorway: { behavior: '在門口轉圈，尾巴壓不住地搖。' },
  'doorway-wait': { behavior: '站在客廳邊緣望著你，沒有追，也沒有叫——像把整個世界縮成這一道門。' },
  'doorway-lie': { behavior: '趴在玄關地磚上，耳朵朝門豎著；眼裡是期待，身子還帶著一點膽怯。' },
  stair: { behavior: '在樓梯上停住，回頭等你。' },
  walk: { behavior: '走幾步就回頭——確認你還在。' },
  park: { behavior: '把鼻子深深埋進樹根旁的泥土裡。' },
  'follow-close': { behavior: '走在你腳邊，步調漸漸和你同步。' },
  'follow-far': { behavior: '遠遠跟著，保持能隨時逃開的距離。' },
  thunder: { behavior: '縮在桌底，整個身子還在發抖。' },
  knee: { behavior: '把頭輕靠在你大腿旁，沒有聲音。' },
  'night-accident': { behavior: '知道自己闖了禍，縮在角落發抖。' },
  window: { behavior: '望著窗外，耳朵隨風聲輕輕動。' },
  'sad-day': { behavior: '你難過時，牠不再鬧，只是靠過來。' },
  home: { behavior: '在沙發腳邊睡著，呼吸一起一伏。' },
  balcony: { behavior: '把鼻子貼在欄杆縫隙，吸很深的一口氣。' },
  repair: { behavior: '在玄關進半步、退半步，還在試探。' },
  wet: { behavior: '毛還濕著，縮成一團，被毛巾裹得只露出一雙眼睛。' },
  'vet-carry': { behavior: '縮在你懷裡，鼻子埋進袖口，耳朵還在聽醫師的聲音。' },
  'vet-walk': { behavior: '被你抱在懷裡，對週末的街頭又亮又響的世界發抖。' },
  held: { behavior: '在你懷裡輕輕嗅，身子還僵，但沒有掙開。' },
  'sunday-wake': { behavior: '在你腳邊醒來，比昨天多靠近了一點點。' },
  'home-settle': { behavior: '下巴擱在你膝上，像說：這裡，好像真的可以。' },
};

const DOG_ASSET_DIR = 'assets/dog';
const DOG_ASSET_EXT = '.png';

/** pose 圖檔別名（wet 等可沿用 rain） */
const DOG_POSE_ASSET = {
  wet: 'rain',
};

function dogAssetFile(poseOrMood) {
  const id = DOG_POSE_ASSET[poseOrMood] || poseOrMood;
  return `${DOG_ASSET_DIR}/dog-${id}${DOG_ASSET_EXT}`;
}

function resolveDogPoseKey(scene, state) {
  if (!scene?.dogPose) return null;
  if (typeof scene.dogPose === 'function') return scene.dogPose(state);
  return scene.dogPose;
}

function resolveDogVisual(scene, state) {
  const poseKey = resolveDogPoseKey(scene, state);
  const pose = poseKey && DOG_POSES[poseKey];
  const feeling = state?.feeling || scene?.feeling || 'anxious';
  const meta = FEELINGS[feeling] || FEELINGS.anxious;

  if (pose) {
    return {
      src: dogAssetFile(poseKey),
      moodClass: meta.mood,
      behavior: pose.behavior,
      temp: meta.temp,
    };
  }

  return {
    src: dogAssetFile(meta.mood),
    moodClass: meta.mood,
    behavior: meta.behavior,
    temp: meta.temp,
  };
}

const BOND_NAMES = { 1: '陌生', 2: '習慣' };

const ALBUM_ENTRIES = {
  prologue_rain: { title: '雨天相遇', desc: '紙箱裡的第一次對視。' },
  first_night: { title: '第一夜', desc: '吹乾、哀鳴、和三步外的陪伴。' },
  day2_petshop: { title: '寵物店', desc: '請假那天，店員阿姨教了你很多。' },
  dog_named: { title: '取名', desc: '名字與性別，第一個專屬於你們的小秘密。' },
  day2_first_meal: { title: '第一次自己吃', desc: '你退開，牠才肯靠近碗。' },
  door_wait: { title: '門口的等待', desc: '你提早回家，牠趴在玄關等你。' },
  balcony_sun: { title: '陽台上的風', desc: '一起曬過一次太陽。' },
  potty_guide: { title: '如廁暗號', desc: '對的瞬間，牠終於聽懂了。' },
  vet_visit: { title: '寵物醫院', desc: '週六的健康檢查，和第一筆認真的帳。' },
  home_scent: { title: '家的氣味', desc: '週日懷裡繞一圈，牠記住了這裡。' },
  walk_calm: { title: '散步的節奏', desc: '回頭時你都在，步子漸漸穩了。' },
  potty_night: { title: '尿墊之夜', desc: '你選擇了不罵、清理、陪坐。' },
  knee: { title: '靠膝', desc: '牠第一次把頭放在你膝上。' },
  park_tree: { title: '第一次聞樹', desc: '公園裡，牠把鼻子埋進泥土。' },
  follow_foot: { title: '第一次跟腳', desc: '回家路上，牠走在你腳邊，一步也不願離太遠。' },
  thunder: { title: '雷雨', desc: '你開了小燈，陪牠度過。' },
  sad_day: { title: '你難過的那一天', desc: '你難過時，牠不再鬧，只是靠過來。' },
};

function dogPronoun(state) {
  if (state?.dogGender === 'female') return '她';
  if (state?.dogGender === 'male') return '他';
  return '牠';
}

function hasDogGender(state) {
  return state?.dogGender === 'male' || state?.dogGender === 'female';
}

/** 取名後依性別將文案中的「牠」改為他／她 */
function applyDogPronouns(text, state) {
  if (!text || !hasDogGender(state)) return text;
  const sub = dogPronoun(state);
  const poss = sub === '她' ? '她的' : '他的';
  return String(text).replace(/牠的/g, poss).replace(/牠/g, sub);
}

function dogLabel(state) {
  const n = state?.dogName;
  return n && String(n).trim() ? String(n).trim() : dogPronoun(state);
}

function hasDogName(state) {
  return !!(state?.dogName && String(state.dogName).trim());
}

/** 此場景／選項是否應播放狗叫（寵物店、獨自外出等無狗在場時為 false） */
function isDogAudioEnabled(scene, choice) {
  if (choice?.noDogSound) return false;
  if (!scene) return false;
  if (scene.noDogAudio || scene.hideDog) return false;
  const loc = scene.location || '';
  if (loc === 'pet_shop') return false;
  return true;
}

function setDogName(state, name) {
  setDogProfile(state, name, state?.dogGender || null);
}

function setDogProfile(state, name, gender) {
  const trimmed = String(name || '').trim();
  state.dogName = trimmed || '豆花';
  if (gender === 'female' || gender === 'male') {
    state.dogGender = gender;
    state.flags.dogGender = gender;
  }
  state.flags.dogNamed = true;
  addMemory(state, 'dog_named');
}

function setDogGender(state, gender) {
  if (gender !== 'female' && gender !== 'male') return;
  state.dogGender = gender;
  state.flags.dogGender = gender;
}

/** 取名前場景（仍用「牠」） */
const PRE_DOG_PROFILE_SCENES = new Set([
  'prologue_rain', 'prologue_home', 'prologue_dry', 'prologue_night', 'prologue_dawn',
  'day2_empty', 'day2_leave', 'day2_rush', 'day2_petshop', 'day2_petshop_after', 'day2_naming', 'day2_gender',
]);

function needsGenderPrompt(scene, state) {
  return hasDogName(state)
    && !hasDogGender(state)
    && scene?.id
    && scene.id !== 'day2_naming'
    && scene.id !== 'day2_gender'
    && !PRE_DOG_PROFILE_SCENES.has(scene.id);
}

function ensureMomentSession(state) {
  if (!state.momentSessionId) {
    state.momentSessionId = typeof crypto !== 'undefined' && crypto.randomUUID
      ? crypto.randomUUID()
      : `m${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
  }
  if (!Array.isArray(state.capturedMoments)) state.capturedMoments = [];
  return state.momentSessionId;
}

async function resetMomentGallery(state) {
  const prev = state.momentSessionId;
  if (prev && typeof MomentGallery !== 'undefined') {
    await MomentGallery.clearSession(prev);
  }
  state.momentSessionId = typeof crypto !== 'undefined' && crypto.randomUUID
    ? crypto.randomUUID()
    : `m${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
  state.capturedMoments = [];
}

function createInitialState() {
  return {
    sceneId: 'prologue_rain',
    day: 1,
    dogName: '',
    dogGender: '',
    trust: 35,
    bondLevel: 1,
    bondProgress: 0,
    feeling: 'anxious',
    smell: '舊紙箱、雨、陌生的房間',
    smellLayers: ['舊紙箱', '雨', '陌生的房間'],
    memories: [],
    flags: {
      pottyNightKind: false,
      afraidOfThunder: false,
      favoriteSpot: 'corner',
      yelledOnce: false,
      thunderHandled: false,
      day2CalmSound: false,
      followVariant: 'close',
      pottyGuideTier: null,
      pottyGuideScore: null,
      walkGuideTier: null,
      walkGuideCalm: null,
      shopTier: null,
      shopScore: null,
      suppliesBought: false,
      dryGentle: false,
      firstNightCalm: false,
      dogNamed: false,
      dogGender: '',
    },
    playTimeStart: Date.now(),
    demoVersion: DEMO_VERSION,
    flowVersion: FLOW_VERSION,
    momentSessionId: '',
    capturedMoments: [],
  };
}

function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

function applyTrust(state, delta) {
  state.trust = clamp(state.trust + delta, 0, 100);
}

function applyBondProgress(state, amount) {
  state.bondProgress += amount;
  if (state.bondLevel === 1 && state.bondProgress >= 100) {
    state.bondLevel = 2;
    state.bondProgress = 100;
  }
}

function addMemory(state, id) {
  if (!state.memories.includes(id)) {
    state.memories.push(id);
  }
}

function setFeeling(state, key) {
  state.feeling = key;
  const f = FEELINGS[key];
  if (f) state._moodMeta = f;
}

function parseSmellString(str) {
  if (!str) return [];
  return String(str).split(/[、,，]/).map((s) => s.trim()).filter(Boolean);
}

function setSmellLayers(state, scents) {
  const layers = Array.isArray(scents) ? scents : parseSmellString(scents);
  state.smellLayers = [...layers];
  state.smell = state.smellLayers.join('、');
}

/** @returns {boolean} whether a new layer was added */
function addSmellLayer(state, scent) {
  const note = String(scent || '').trim();
  if (!note) return false;
  if (!state.smellLayers) state.smellLayers = parseSmellString(state.smell);
  if (state.smellLayers.includes(note)) return false;
  state.smellLayers.push(note);
  state.smell = state.smellLayers.join('、');
  return true;
}

function getSavePayload(state) {
  return {
    dogName: state.dogName,
    dogGender: state.dogGender || '',
    trustFinal: state.trust,
    bondLevel: state.bondLevel,
    memories: [...state.memories],
    flags: { ...state.flags },
    sceneId: state.sceneId,
    demoVersion: DEMO_VERSION,
    playMinutes: Math.round((Date.now() - state.playTimeStart) / 60000),
  };
}

function saveGame(state) {
  state.flowVersion = FLOW_VERSION;
  localStorage.setItem(SAVE_KEY, JSON.stringify(state));
}

const DAY1_FLOW_SCENES = new Set([
  'prologue_rain', 'prologue_home', 'prologue_dry', 'prologue_night', 'prologue_dawn',
]);
const DAY2_SHOP_SCENES = new Set([
  'day2_empty', 'day2_leave', 'day2_rush', 'day2_petshop', 'day2_petshop_after', 'day2_naming', 'day2_gender', 'day2_return',
]);
const DAY2_HOME_SCENES = new Set([
  'day2_morning', 'day2_wait', 'day2_hurt', 'day2_kitchen', 'day2_midday',
  'day2_afternoon', 'day2_evening',
]);
const DAY3_LEGACY_SCENES = new Set([
  'day3_kitchen', 'day3_balcony',
]);
const DAY4_LEGACY_SCENES = new Set([
  'day4_potty_intro', 'day4_morning', 'day4_afternoon',
]);
const DAY5_LEGACY_SCENES = new Set([
  'day5_prep', 'day5_stairwell', 'day5_walk', 'day5_park', 'day5_follow',
]);

/** 舊存檔補接 Day1 夜間 / Day2 請假·寵物店 新流程 */
function migrateSaveState(raw) {
  if (!raw) return null;
  const base = createInitialState();
  const s = {
    ...base,
    ...raw,
    flags: { ...base.flags, ...(raw.flags || {}) },
    memories: Array.isArray(raw.memories) ? [...raw.memories] : [],
  };

  if ((s.flowVersion || 0) >= FLOW_VERSION) {
    if (!hasDogName(s) && s.sceneId === 'day2_return') s.sceneId = 'day2_naming';
    if (hasDogName(s) && !hasDogGender(s) && s.sceneId === 'day2_return') s.sceneId = 'day2_gender';
    ensureMomentSession(s);
    if (!Array.isArray(s.capturedMoments)) s.capturedMoments = [];
    return s;
  }

  const mem = s.memories;
  if (!mem.includes('first_night') && !DAY1_FLOW_SCENES.has(s.sceneId)) {
    s.sceneId = 'prologue_home';
    s.day = 1;
  } else if (
    mem.includes('first_night')
    && !mem.includes('day2_petshop')
    && DAY2_HOME_SCENES.has(s.sceneId)
  ) {
    s.sceneId = 'day2_empty';
    s.day = 2;
  } else if (!mem.includes('first_night') && DAY2_SHOP_SCENES.has(s.sceneId)) {
    s.sceneId = 'prologue_home';
    s.day = 1;
  } else if ((s.flowVersion || 0) < 3 && s.sceneId === 'day2_leave') {
    s.sceneId = 'day2_empty';
    s.day = 2;
  } else if ((s.flowVersion || 0) < 4 && DAY3_LEGACY_SCENES.has(s.sceneId)) {
    s.sceneId = 'day3_breakfast_rush';
    s.day = 3;
  } else if ((s.flowVersion || 0) < 4 && s.sceneId === 'day3_curious') {
    s.sceneId = 'day3_breakfast_rush';
    s.day = 3;
  } else if ((s.flowVersion || 0) < 4 && s.sceneId === 'day3_hurt') {
    s.sceneId = 'day3_breakfast_rush';
    s.day = 3;
  } else if ((s.flowVersion || 0) < 4 && s.sceneId === 'day4_morning') {
    s.sceneId = 'day4_off';
    s.day = 4;
  } else if ((s.flowVersion || 0) < 5 && DAY4_LEGACY_SCENES.has(s.sceneId)) {
    s.sceneId = 'day4_off';
    s.day = 4;
  } else if ((s.flowVersion || 0) < 5 && DAY5_LEGACY_SCENES.has(s.sceneId)) {
    s.sceneId = 'day5_sunday';
    s.day = 5;
  }

  s.flowVersion = FLOW_VERSION;
  s.demoVersion = DEMO_VERSION;
  return s;
}

function loadGame() {
  try {
    const raw = localStorage.getItem(SAVE_KEY) || localStorage.getItem(SAVE_KEY_LEGACY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    const migrated = migrateSaveState(parsed);
    if (migrated && localStorage.getItem(SAVE_KEY_LEGACY) && !localStorage.getItem(SAVE_KEY)) {
      saveGame(migrated);
    }
    return migrated;
  } catch {
    return null;
  }
}

function exportSaveJson(state) {
  return JSON.stringify(getSavePayload(state), null, 2);
}

/** 測試用：各 Day 開場場景與最低限度前置狀態 */
const DAY_JUMP_TARGETS = {
  1: { sceneId: 'prologue_rain', seed: (s) => { seedDevDay1(s); } },
  2: { sceneId: 'day2_empty', seed: (s) => { seedDevDay2(s); } },
  3: { sceneId: 'day3_breakfast_rush', seed: (s) => { seedDevDay3(s); } },
  4: { sceneId: 'day4_off', seed: (s) => { seedDevDay4(s); } },
  5: { sceneId: 'day5_sunday', seed: (s) => { seedDevDay5(s); } },
  6: { sceneId: 'day6_morning', seed: (s) => { seedDevDay6(s); } },
  7: { sceneId: 'day7_morning', seed: (s) => { seedDevDay7(s); } },
  epilogue: { sceneId: 'epilogue', seed: (s) => { seedDevEpilogue(s); } },
};

function seedDevDay1(s) {
  s.trust = 35;
  s.bondProgress = 0;
  s.feeling = 'anxious';
}

function seedDevDay2(s) {
  addMemory(s, 'prologue_rain');
  addMemory(s, 'first_night');
  s.trust = 40;
  s.bondProgress = 15;
  s.feeling = 'anxious';
}

function seedDevDay3(s) {
  seedDevDay2(s);
  setDogProfile(s, '小布丁', 'male');
  addMemory(s, 'day2_petshop');
  addMemory(s, 'day2_first_meal');
  s.flags.suppliesBought = true;
  s.flags.shopTier = 'good';
  s.trust = 48;
  s.bondProgress = 42;
  s.feeling = 'anxious';
}

function seedDevDay4(s) {
  seedDevDay3(s);
  addMemory(s, 'door_wait');
  s.trust = 52;
  s.bondProgress = 55;
  s.feeling = 'content';
}

function seedDevDay5(s) {
  seedDevDay4(s);
  addMemory(s, 'vet_visit');
  s.flags.vetTier = 'good';
  s.flags.vetBillAcknowledged = true;
  s.trust = 58;
  s.bondProgress = 68;
  s.bondLevel = 2;
  s.feeling = 'content';
}

function seedDevDay6(s) {
  seedDevDay5(s);
  addMemory(s, 'home_scent');
  s.flags.homeExploreTier = 'good';
  s.trust = 62;
  s.bondProgress = 78;
}

function seedDevDay7(s) {
  seedDevDay6(s);
  addMemory(s, 'thunder');
  s.flags.thunderHandled = true;
  s.flags.afraidOfThunder = true;
  s.trust = 68;
  s.bondProgress = 88;
  s.bondLevel = 2;
}

function seedDevEpilogue(s) {
  seedDevDay7(s);
  addMemory(s, 'knee');
  s.trust = 72;
  s.bondProgress = 95;
}

/** 重置並套用指定 Day 的測試狀態；回傳 sceneId 或 null */
function applyDayJumpState(state, key) {
  const target = DAY_JUMP_TARGETS[key === 'epilogue' ? 'epilogue' : Number(key)];
  if (!target) return null;

  const fresh = createInitialState();
  Object.assign(state, fresh);
  state.flags = { ...fresh.flags };
  state.memories = [];
  state.capturedMoments = [];

  target.seed(state);
  state.sceneId = target.sceneId;
  state.flowVersion = FLOW_VERSION;
  ensureMomentSession(state);
  return target.sceneId;
}

/** 依跨作標記產生 Epilogue 個人化文案（story-narrative agent） */
function buildEpiloguePersonalLines(state) {
  const name = dogLabel(state);
  const lines = [];

  if (state.memories.includes('follow_foot')) {
    lines.push(`回程的路上，${name} 已經會走在你腳邊。`);
  } else if (state.flags.followVariant === 'far') {
    lines.push(`${name} 仍隔著幾步，但每次都會回頭——確認你還在。`);
  }

  if (state.memories.includes('first_night')) {
    lines.push(applyDogPronouns('第一夜你手忙腳亂吹乾牠，也聽懂了夜裡那幾聲哀鳴。', state));
  }

  if (state.memories.includes('day2_petshop')) {
    lines.push('請假去寵物店那天，店員說的話你記到現在。');
  }

  if (state.memories.includes('vet_visit')) {
    lines.push(applyDogPronouns('週六帶牠去寵物醫院那天，檢查單上的數字讓你愣了一下——但也懂了這是責任。', state));
  }

  if (state.memories.includes('home_scent')) {
    lines.push(applyDogPronouns('週日懷裡繞完一圈，牠記住了沙發、食盆，還有你的床單味。', state));
  }

  if (state.memories.includes('potty_guide')) {
    lines.push(applyDogPronouns('如廁引導那次，對的瞬間牠終於聽懂了你的暗號。', state));
  }

  if (state.memories.includes('walk_calm')) {
    lines.push(applyDogPronouns('散步時每次回頭你都在，牠的步子漸漸穩了下來。', state));
  }

  if (state.memories.includes('potty_night')) {
    lines.push(applyDogPronouns('尿墊之夜，你選了不罵、清理、陪坐；牠把頭放在你膝上。', state));
  } else if (!state.flags.pottyNightKind) {
    lines.push('有些夜裡的事還在記憶裡——但你們都還在，還來得及補。');
  }

  if (state.memories.includes('thunder')) {
    lines.push(
      state.flags.thunderHandled
        ? '怕雷這件事會記很久——包括，誰在桌邊開了那盞小夜燈。'
        : '雷雨來過；下次響起時，你們會知道該怎麼陪。'
    );
  }

  if (state.memories.includes('sad_day')) {
    lines.push(`你難過那天，${name} 沒有吵，只是靠過來——和 Day 3 那夜一樣輕。`);
  }

  if (state.memories.includes('park_tree')) {
    lines.push('公園那棵樹的泥土味，已經寫進腳印集。');
  }

  if (state.memories.includes('balcony_sun')) {
    lines.push('陽台上的風，你們一起曬過一次。');
  }

  if (lines.length === 0) {
    lines.push('七天還很短——但「開始」這兩個字，已經有了重量。');
  }

  return lines;
}

if (typeof module !== 'undefined') module.exports = {
  SAVE_KEY, SAVE_KEY_LEGACY, FLOW_VERSION, FEELINGS, BOND_NAMES, ALBUM_ENTRIES, DOG_POSES, DOG_ASSET_DIR, DOG_ASSET_EXT,
  createInitialState, applyTrust, applyBondProgress,
  addMemory, setFeeling, parseSmellString, setSmellLayers, addSmellLayer,
  resolveDogPoseKey, resolveDogVisual, migrateSaveState, dogLabel, dogPronoun, applyDogPronouns,
  hasDogName, hasDogGender, isDogAudioEnabled, setDogName, setDogProfile, setDogGender, needsGenderPrompt,
  ensureMomentSession, resetMomentGallery,
  getSavePayload, saveGame, loadGame, exportSaveJson, buildEpiloguePersonalLines,
  DAY_JUMP_TARGETS, applyDayJumpState,
  OWNER_WORK_START_HOUR, OWNER_WORK_END_HOUR, DEMO_DAY_CALENDAR,
  getDemoDayCalendar, isOwnerWorkday, isOwnerOnLeave, ownerShouldBeHome,
};
