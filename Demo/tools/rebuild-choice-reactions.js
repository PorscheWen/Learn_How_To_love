/**
 * 從 agent transcript 還原 choice-reactions.js，並補齊 scenes.js 現有選項
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const TRANSCRIPT =
  'C:/Users/BaoGo/.cursor/projects/c-Users-BaoGo-Documents-ClaudeCode-Project/agent-transcripts/f2384e48-d3e2-4864-a12b-9a5b9e520f5a/f2384e48-d3e2-4864-a12b-9a5b9e520f5a.jsonl';
const OUT = path.join(ROOT, 'js/choice-reactions.js');

const lines = fs.readFileSync(TRANSCRIPT, 'utf8').split(/\n/);
let cr = null;
const patches = [];

for (const line of lines) {
  try {
    const o = JSON.parse(line);
    for (const c of o.message?.content || []) {
      if (c.name === 'Write' && c.input?.path?.includes('choice-reactions.js')) {
        const contents = c.input.contents || '';
        if (!contents.startsWith('const fs = require')) {
          cr = contents;
        }
      }
      if (c.name === 'StrReplace' && c.input?.path?.includes('choice-reactions.js')) {
        patches.push(c.input);
      }
    }
  } catch (_) {}
}

if (!cr) {
  console.error('No valid Write found in transcript');
  process.exit(1);
}

let applied = 0;
for (const patch of patches) {
  const { old_string, new_string, replace_all } = patch;
  if (!old_string || new_string === undefined) continue;
  if (replace_all) {
    if (cr.includes(old_string)) {
      cr = cr.split(old_string).join(new_string);
      applied += 1;
    }
  } else if (cr.includes(old_string)) {
    cr = cr.replace(old_string, new_string);
    applied += 1;
  }
}

cr = cr.replace(/\$\{s\.dogName\}/g, '${dogLabel(s)}');

// --- 覆蓋 prologue / day2 開場（現行 scenes.js）---
const prologueBlock = `  'prologue_home::深吸一口氣，手忙腳亂找毛巾和吹風機': {
    text: (s) => \`\${dogLabel(s)} 跟著你轉圈，尾巴夾緊，不知道你要做什麼。\`,
    feeling: 'anxious', cue: 'whimperScared',
  },

  'prologue_dry::吹風機調到低檔，先讓牠聞聞風': {
    text: (s) => \`\${dogLabel(s)} 嗅了嗅風，身子還緊，但沒有再掙。\`,
    feeling: 'shy', cue: 'sniffQuick',
  },
  'prologue_dry::一手按穩、一手吹，越弄越亂也沒停': {
    text: (s) => \`\${dogLabel(s)} 被毛巾裹著，只露出一雙濕漉漉的眼睛。\`,
    feeling: 'anxious', cue: 'whineSoft',
  },
  'prologue_dry::放棄吹風機，只用毛巾慢慢擦到半乾': {
    text: (s) => \`\${dogLabel(s)} 在毛巾裡慢慢鬆了一點，像終於不那麼冷。\`,
    feeling: 'curious', cue: 'breathEase',
  },

  'prologue_night::走到三步外，輕聲說：「我在，沒事了。」': {
    text: (s) => \`\${dogLabel(s)} 的哀鳴短了一拍，又低低地哼了一聲。\`,
    feeling: 'shy', cue: 'whineSoft', holdMs: 1800,
  },
  'prologue_night::開小夜燈，坐在地上，不強抱，等聲音慢下來': {
    text: (s) => \`\${dogLabel(s)} 的呼吸漸漸和你同步，哀鳴一聲比一聲輕。\`,
    feeling: 'content', cue: 'sleepBreath', holdMs: 2000,
  },
  'prologue_night::困得發煩，還是壓低聲音陪在遠處': {
    text: (s) => \`\${dogLabel(s)} 仍偶爾哼一下，但沒有再撕心裂肺地叫。\`,
    feeling: 'anxious', cue: 'whimperQuiet', holdMs: 1600,
  },

  'prologue_dawn::撐到起床……': {
    text: (s) => \`\${dogLabel(s)} 在紙箱邊睡著了，呼吸比夜裡穩一點。\`,
    feeling: 'sleepy', cue: 'sleepSnoreDeep', holdMs: 4800,
  },

  'day2_leave::回覆主管：「謝謝，明天會補上進度。」': {
    text: (s) => \`\${dogLabel(s)} 不知道你在忙什麼，只是安靜地待著。\`,
    feeling: 'anxious', cue: 'breathEase',
  },
  'day2_leave::打電話跟主管說：昨天帶回一隻狗，今天需要在家安頓一下': {
    text: (s) => \`\${dogLabel(s)} 的耳朵動了一下，像聽見你聲音裡的緊張。\`,
    feeling: 'curious', cue: 'huffSoft',
  },

  'day2_petshop_after::「還沒想好……可以現在取嗎？」': {
    text: () => '（店員把紙筆推過來，等你想一個名字。）',
    feeling: 'curious', cue: 'breathEase', holdMs: 1200,
  },

  'day2_return::換好水，開始這個請假的早晨': {
    text: (s) => \`\${dogLabel(s)} 的鼻子貼向新食盆，又迅速縮回去。\`,
    feeling: 'curious', cue: 'sniffDeep',
  },

  'day2_morning::`;

if (cr.includes("'prologue_home::Day 2")) {
  cr = cr.replace(
    /  'prologue_home::Day 2[\s\S]*?  'day2_morning::/,
    prologueBlock
  );
} else if (!cr.includes("'prologue_home::深吸一口氣")) {
  cr = cr.replace(
    /  'prologue_home::[\s\S]*?  'day2_morning::/,
    prologueBlock
  );
}

// Day 3 新流程 + Day 4–5 週末線
const day3to5Block = `
  'day3_breakfast_rush::匆忙倒好飼料，來不及等牠吃完就出門': {
    text: (s) => \`\${dogLabel(s)} 還在舔碗邊，門已經關上了。\`,
    feeling: 'anxious', cue: 'whimperQuiet',
  },
  'day3_breakfast_rush::邊綁鞋帶邊推碗靠近：「乖乖的，我很快回來。」': {
    text: (s) => \`\${dogLabel(s)} 抬頭看你，尾巴輕輕動了一下。\`,
    feeling: 'shy', cue: 'whineSoft',
  },
  'day3_breakfast_rush::硬是多留五分鐘，看牠舔了一口才走': {
    text: (s) => \`\${dogLabel(s)} 舔完那一口，還追著你的腳步到門口。\`,
    feeling: 'curious', cue: 'sniffQuick',
  },

  'day3_homecoming::蹲下來，什麼都不說，先讓牠聞聞你': {
    text: (s) => \`\${dogLabel(s)} 的鼻子在你手背上蹭了蹭，整個身子慢慢鬆下來。\`,
    feeling: 'attached', cue: 'breathEase', pose: 'doorway-lie', holdMs: 2000,
  },
  'day3_homecoming::輕聲說：「對不起，讓你等了。」': {
    text: (s) => \`\${dogLabel(s)} 把頭靠過來，像終於等到這句話。\`,
    feeling: 'content', cue: 'sigh', pose: 'doorway-lie',
  },
  'day3_homecoming::看見家裡還算整齊，鬆了口氣，把牠抱緊一點': {
    text: (s) => \`\${dogLabel(s)} 在你懷裡打了個小哈欠，尾巴輕輕掃過你的手腕。\`,
    feeling: 'curious', cue: 'whineSoft', pose: 'doorway-lie',
  },

  'day3_night_after::摸一摸牠的頭，關燈': {
    text: (s) => \`\${dogLabel(s)} 沒有再驚醒，呼吸漸漸變長。\`,
    feeling: 'attached', cue: 'sleepSnoreDeep', holdMs: 4800,
  },

  'day4_repair::蹲下，說對不起，拿出牠最愛的玩具': {
    text: (s) => \`\${dogLabel(s)} 愣了一下，慢慢把鼻子蹭向你手心。\`,
    feeling: 'curious', cue: 'yipBright', pose: 'toy',
  },
  'day4_repair::照常餵食，不說話，但也不離開': {
    text: (s) => \`\${dogLabel(s)} 吃掉飯粒，仍與你保持半步距離。\`,
    feeling: 'anxious', cue: 'murmurLow',
  },

  'day4_off::幫牠系好牽繩，出門往寵物醫院': {
    text: (s) => \`\${dogLabel(s)} 在門口停了一下，還是跟你出門。\`,
    feeling: 'anxious', cue: 'murmurUneasy', pose: 'walk',
  },
  'day4_off::先餵飽、安撫一下，再慢慢出門': {
    text: (s) => \`\${dogLabel(s)} 吃幾口後，把頭靠在你手背上。\`,
    feeling: 'curious', cue: 'breathEase', pose: 'kitchen',
  },

  'day4_vet_bill::深吸一口氣，刷卡：這也是照顧牠的一部分': {
    text: (s) => \`\${dogLabel(s)} 不知道發生什麼，只是把鼻子埋進你的袖口。\`,
    feeling: 'content', cue: 'sigh', holdMs: 1600,
  },
  'day4_vet_bill::先問清楚每一項，再付款——該花的不能省': {
    text: (s) => \`\${dogLabel(s)} 在你懷裡慢慢鬆下來，像信任你的決定。\`,
    feeling: 'curious', cue: 'sniff', holdMs: 1500,
  },

  'day4_evening::Day 5 · 週日，早晨的陽光……': {
    text: (s) => \`\${dogLabel(s)} 在毯子上蜷成一團，呼吸漸漸變長。\`,
    feeling: 'sleepy', cue: 'sleepSnoreDeep', holdMs: 4800,
  },

  'day5_sunday::把牠抱起來，從客廳開始慢慢認': {
    text: (s) => \`\${dogLabel(s)} 身子還有點僵，但沒有掙開。\`,
    feeling: 'shy', cue: 'huff', pose: 'corner',
  },
  'day5_sunday::先坐在地板，讓牠自己靠過來再抱': {
    text: (s) => \`\${dogLabel(s)} 猶豫了一會，還是把頭靠過來。\`,
    feeling: 'curious', cue: 'whineSoft', holdMs: 1400,
  },

  'day5_home_after::週日的午後，就這樣靜靜度過……': {
    text: (s) => \`\${dogLabel(s)} 把下巴擱在你膝上，像終於鬆了一口氣。\`,
    feeling: 'content', cue: 'breathEase', pose: 'knee', holdMs: 1800,
  },

  'day5_evening::Day 6 的早晨……': {
    text: (s) => \`\${dogLabel(s)} 沒有驚醒，只在夢裡輕輕哼了一聲。\`,
    feeling: 'attached', cue: 'sleepSnoreDeep', pose: 'knee', holdMs: 4200,
  },

  'day6_morning::`;

// Remove obsolete day3/day4/day5 entries then inject block before day6 if needed
cr = cr.replace(/\n  'day3_morning::[\s\S]*?  'day6_morning::/m, `\n${day3to5Block}`);

// Fix restore script bug: take only up to CHOICE_REACTIONS closing
if (!cr.includes('function choiceReactionKey')) {
  const footer = `
};

function choiceReactionKey(sceneId, choiceText) {
  return \`\${sceneId}::\${String(choiceText || '').trim()}\`;
}

function lookupChoiceReaction(sceneId, choiceText) {
  return CHOICE_REACTIONS[choiceReactionKey(sceneId, choiceText)] || null;
}

if (typeof module !== 'undefined') {
  module.exports = { CHOICE_REACTIONS, choiceReactionKey, lookupChoiceReaction };
}
`;
  if (cr.includes('};')) {
    cr = cr.replace(/\};[\s\S]*$/, footer);
  }
}

// Validate & fill missing
const scenesPath = path.join(ROOT, 'js/scenes.js');
const scenesSrc = fs.readFileSync(scenesPath, 'utf8');
// eslint-disable-next-line no-eval
eval(scenesSrc.replace(/^const SCENES\s*=/m, 'global.SCENES ='));
eval(cr.split('function choiceReactionKey')[0].replace(/^const CHOICE_REACTIONS\s*=/m, 'global.CHOICE_REACTIONS ='));

const missing = [];
for (const [id, scene] of Object.entries(global.SCENES)) {
  if (!scene.choices) continue;
  for (const c of scene.choices) {
    const key = `${id}::${String(c.text || '').trim()}`;
    if (!global.CHOICE_REACTIONS[key]) missing.push({ key, id, text: c.text });
  }
}

if (missing.length) {
  const insert = missing.map(({ key, text }) => {
    const safe = text.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
    return `  '${key.replace(/\\/g, '\\\\').replace(/'/g, "\\'")}': {
    text: (s) => \`\${dogLabel(s)} 對「${safe.slice(0, 12)}${safe.length > 12 ? '…' : ''}」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`;
  }).join('\n\n');
  cr = cr.replace(/\n};\n\nfunction choiceReactionKey/, `\n\n${insert}\n};\n\nfunction choiceReactionKey`);
  console.log('filled missing:', missing.length);
  missing.forEach((m) => console.log('  -', m.key));
}

fs.writeFileSync(OUT, cr, 'utf8');
console.log('rebuilt choice-reactions.js, transcript patches:', applied, 'bytes:', cr.length);
