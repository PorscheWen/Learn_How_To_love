/**
 * Rebuild scenes.js: prologue_rain + day1/day2 block + replay patches.
 */
const fs = require('fs');
const path = require('path');

const transcript = 'C:/Users/BaoGo/.cursor/projects/c-Users-BaoGo-Documents-ClaudeCode-Project/agent-transcripts/f2384e48-d3e2-4864-a12b-9a5b9e520f5a/f2384e48-d3e2-4864-a12b-9a5b9e520f5a.jsonl';
const out = path.join(__dirname, '../js/scenes.js');
const dayBlock = fs.readFileSync(path.join(__dirname, 'big-patch.txt'), 'utf8');

const prologueRain = `  prologue_rain: {
    id: 'prologue_rain',
    day: 1,
    location: 'prologue_rain',
    music: 'melancholy',
    weather: 'rain',
    feeling: 'anxious',
    dogPose: 'rain',
    smell: '濕紙箱、雨水、微弱體溫',
    text: () => '傍晚，雨沒有要停的樣子。\\n巷口那個紙箱輕輕動了一下——\\n你蹲下去，對上一雙濕漉漉、還在發抖的眼睛。\\n\\n牠很小，毛貼著骨頭，像一整團被雨打溼的暖色。\\n你用自己的外套先裹住，才發現牠沒有叫，只是很輕、很輕地靠過來。',
    sub: 'Day 1。你帶牠回家。\\n那時候，你們都還不知道，這叫作「開始」。\\n但雨聲裡，已經多了一個呼吸。',
    onEnter: (s) => { addMemory(s, 'prologue_rain'); },
    choices: [
      {
        text: '用毛巾輕輕包住，抱上計程車',
        effect: (s) => { applyTrust(s, 5); applyBondProgress(s, 10); },
        next: 'prologue_home',
      },
    ],
  },

`;

let dayBlockFixed = dayBlock
  .replace(/\$\{s\.dogName \|\| '牠'\}/g, '${dogLabel(s)}')
  .replace(/\$\{s\.dogName\}/g, '${dogLabel(s)}');

// naming flow: petshop_after -> naming -> return
dayBlockFixed = dayBlockFixed.replace(
  `    text: (s) => {
      const gentle = s.flags.dryGentle;
      return \`店員把東西裝進紙箱，邊整理邊說：\\n\\n「幼犬第一晚叫，太正常了。\\n換環境誰不怕？別罵，別硬抱。\\n你穩，牠才穩。」\\n\\n\${gentle ? '她又看你一眼：「吹乾有慢慢來吧？很好。」\\n' : ''}「食盆放固定位置，尿墊先鋪在牠常待的角落。\\n餓了會吃，怕了會叫——\\n你要做的，是讓 \${dogLabel(s)} 知道：你會回來。」\\n\\n你抱著紙箱走出店門，\\n心裡仍虛，但沒有剛才那麼空。\`;
    },
    sub: '紙箱有點沉。\\n你第一次覺得，\\n「負責任」是有重量的。',
    choices: [
      { text: '提著東西回家……', effect: () => {}, next: 'day2_return' },
    ],
  },

  day2_return:`,
  `    text: (s) => {
      const gentle = s.flags.dryGentle;
      return \`店員把東西裝進紙箱，邊整理邊說：\\n\\n「幼犬第一晚叫，太正常了。\\n換環境誰不怕？別罵，別硬抱。\\n你穩，牠才穩。」\\n\\n\${gentle ? '她又看你一眼：「吹乾有慢慢來吧？很好。」\\n' : ''}「食盆放固定位置，尿墊先鋪在牠常待的角落。\\n餓了會吃，怕了會叫——\\n你要做的，是讓牠知道：你會回來。」\\n\\n紙箱裝滿了。\\n她拍一拍袋口，忽然問：\\n「對了——牠叫什麼名字？」\`;
    },
    sub: '你愣了一下。\\n昨天只顧著帶牠回家，\\n還沒想過這件事。',
    choices: [
      { text: '「還沒想好……可以現在取嗎？」', effect: () => {}, next: 'day2_naming' },
    ],
  },

  day2_naming: {
    id: 'day2_naming',
    day: 2,
    location: 'pet_shop',
    music: 'warm',
    feeling: 'curious',
    smellAdd: '店員的咖啡味、紙箱購物袋',
    namePrompt: true,
    text: () => \`店員笑了，把收銀機旁的小紙條推過來。\\n\\n「當然可以啊。\\n名字不用完美，\\n只要是你願意叫牠的那一個。」\\n\\n你盯著紙箱發呆——\\n腦子裡閃過很多字，\\n最後留下一個你覺得\\n念起來會比較溫柔的。\`,
    sub: '替牠取名字。\\n這可能是你們之間，\\n第一個被記住的事。',
    next: 'day2_return',
  },

  day2_return:`
);

dayBlockFixed = dayBlockFixed.replace(
  `    text: (s) => \`玄關鑰匙轉動的聲音，\\n\${dogLabel(s)} 的耳朵立刻豎起來。\\n\\n你提著購物袋進門，\\n牠沒有衝過來，只是從紙箱邊探頭——\\n鼻子瘋狂地嗅：\\n這些袋子裡，有沒有「好事」的味道。\\n\\n你把尿墊鋪好、食盆擺正，\\n動作仍有些手忙腳亂，\\n但比昨夜在浴室裡，穩了一點。\`,`,
  `    text: (s) => \`玄關鑰匙轉動的聲音，\\n\${dogLabel(s)} 的耳朵立刻豎起來。\\n\\n你提著購物袋進門，\\n在門口低聲念了一次牠的名字——\\n還不太習慣，但舌頭記住了。\\n\\n牠沒有衝過來，只是從紙箱邊探頭，\\n鼻子瘋狂地嗅：這些袋子裡，有沒有「好事」的味道。\\n\\n你把尿墊鋪好、食盆擺正，\\n動作仍有些手忙腳亂，\\n但比昨夜在浴室裡，穩了一點。\`,`
);

// Remove trailing "  day2_morning: {" from day block - we'll merge from tail file
const dayBlockTrimmed = dayBlockFixed.replace(/\n\n  day2_morning: \{\s*$/, '');

// Get tail starting day2_morning from last good patch in transcript
const lines = fs.readFileSync(transcript, 'utf8').split(/\n/);
const patches = [];
for (const line of lines) {
  try {
    const o = JSON.parse(line);
    for (const c of o.message?.content || []) {
      if (c.name === 'StrReplace' && c.input?.path?.includes('scenes.js')) {
        patches.push(c.input);
      }
    }
  } catch (_) {}
}

// Seed: header + prologue_rain + day block + placeholder day2_morning from old patch
let seed = `/**
 * Scene graph — refined narrative copy
 */
const SCENES = {
${prologueRain}${dayBlockTrimmed},

  day2_morning: PLACEHOLDER
};

if (typeof module !== 'undefined') module.exports = { SCENES };
`;

// Find a patch that contains full day2_morning through epilogue - largest new_string with day3_morning
let tail = '';
for (const p of patches) {
  const ns = p.new_string || '';
  if (ns.includes('day3_morning') && ns.includes('epilogue') && ns.length > tail.length) {
    tail = ns;
  }
}
if (!tail) {
  for (const p of patches) {
    const ns = p.new_string || '';
    if (ns.startsWith('  day2_morning:') && ns.length > tail.length) tail = ns;
  }
}

if (!tail) {
  // fallback: extract from patch with day2_morning text update
  for (const p of patches) {
    if (p.old_string?.includes('day2_morning') && p.new_string?.includes('day2_morning')) {
      // partial
    }
  }
  console.error('No tail found');
  process.exit(1);
}

// If tail is full SCENES tail from day2_morning to end
if (!tail.trim().startsWith('day2_morning') && !tail.trim().startsWith('  day2_morning')) {
  console.error('Unexpected tail start', tail.slice(0, 80));
}

if (!tail.trim().startsWith('  ')) tail = '  ' + tail;

seed = seed.replace('  day2_morning: PLACEHOLDER', tail.replace(/,\s*$/, ''));

let content = seed;
let applied = 0;
for (const p of patches) {
  const { old_string, new_string, replace_all } = p;
  if (!old_string || new_string === undefined) continue;
  if (old_string.length < 20) continue;
  if (replace_all) {
    if (content.includes(old_string)) {
      content = content.split(old_string).join(new_string);
      applied++;
    }
  } else if (content.includes(old_string)) {
    content = content.replace(old_string, new_string);
    applied++;
  }
}

// Final dogLabel pass
content = content
  .replace(/\$\{s\.dogName \|\| '牠'\}/g, '${dogLabel(s)}')
  .replace(/\$\{s\.dogName\}/g, '${dogLabel(s)}');

fs.writeFileSync(out, content, 'utf8');
console.log('Wrote scenes.js, patches applied:', applied);
try {
  require('child_process').execSync(`node --check "${out}"`, { stdio: 'pipe' });
  console.log('Syntax OK');
} catch (e) {
  console.error('Syntax fail', e.stderr?.toString());
  process.exit(1);
}
