/**
 * Rebuild scenes.js from transcript fragments + big-patch + naming flow.
 */
const fs = require('fs');
const path = require('path');

const transcript = path.join(
  process.env.USERPROFILE || '',
  '.cursor/projects/c-Users-BaoGo-Documents-ClaudeCode-Project/agent-transcripts/f2384e48-d3e2-4864-a12b-9a5b9e520f5a/f2384e48-d3e2-4864-a12b-9a5b9e520f5a.jsonl'
);
const out = path.join(__dirname, '../js/scenes.js');
const dayBlock = fs.readFileSync(path.join(__dirname, 'big-patch.txt'), 'utf8');
const patch38 = fs.readFileSync(path.join(__dirname, 'patch38.txt'), 'utf8');
const seedOld = fs.readFileSync(path.join(__dirname, 'scenes-seed.txt'), 'utf8');

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

function dogLabelPass(s) {
  return s
    .replace(/\$\{s\.dogName \|\| '牠'\}/g, '${dogLabel(s)}')
    .replace(/\$\{s\.dogName\}/g, '${dogLabel(s)}');
}

let head = dogLabelPass(dayBlock);

// naming flow: petshop_after -> naming -> return
head = head.replace(
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

head = head.replace(
  `    text: (s) => \`玄關鑰匙轉動的聲音，\\n\${dogLabel(s)} 的耳朵立刻豎起來。\\n\\n你提著購物袋進門，\\n牠沒有衝過來，只是從紙箱邊探頭——\\n鼻子瘋狂地嗅：\\n這些袋子裡，有沒有「好事」的味道。\\n\\n你把尿墊鋪好、食盆擺正，\\n動作仍有些手忙腳亂，\\n但比昨夜在浴室裡，穩了一點。\`,`,
  `    text: (s) => \`玄關鑰匙轉動的聲音，\\n\${dogLabel(s)} 的耳朵立刻豎起來。\\n\\n你提著購物袋進門，\\n在門口低聲念了一次牠的名字——\\n還不太習慣，但舌頭記住了。\\n\\n牠沒有衝過來，只是從紙箱邊探頭，\\n鼻子瘋狂地嗅：這些袋子裡，有沒有「好事」的味道。\\n\\n你把尿墊鋪好、食盆擺正，\\n動作仍有些手忙腳亂，\\n但比昨夜在浴室裡，穩了一點。\`,`
);

// trim day2_morning stub from head
head = head.replace(/\n\n  day2_morning: \{\s*$/, '');

// day2 block from patch38 (skip prologue_home tail in patch38)
const day2Block = patch38.replace(/^\s*choices:[\s\S]*?day2_morning: \{\s*/, '  day2_morning: {');
const day2Trimmed = day2Block.replace(/\n\n  day3_morning: \{\s*$/, '');

// updated day2_morning intro for post-shop flow
const day2Updated = day2Trimmed.replace(
  `    text: (s) => \`Day 2，早晨。\\n雨停了，\${dogLabel(s)} 還在紙箱旁——\\n位置幾乎和昨夜一樣，像一夜沒有真正睡著。\`,`,
  `    text: (s) => \`請假在家的這個早晨。\\n窗玻璃還凝著昨夜的霧，光透進來，很軟。\\n\\n\${dogLabel(s)} 還在紙箱旁——\\n但食盆、尿墊、新毯都已經就位。\\n\\n你換了更乾淨的水，也習慣了乾淨的手。\\n水碗輕碰地板的聲音，讓牠耳朵動了一下。\`,`
).replace(
  `    smellAdd: '雨停後的潮氣',`,
  `    smellAdd: '雨停後的潮氣、新買的飼料',`
).replace(
  `    sub: '你比牠更早醒。\\n房間很安靜，安靜到能聽見自己的猶豫。',`,
  `    sub: '店員說的話還在耳邊：\\n「照顧不是衝動一次，\\n而是每天——準備好，再靠近。」',`
);

// day3+ from older seed (good UTF-8)
const day3Idx = seedOld.indexOf('  day3_morning: {');
const tailEnd = seedOld.lastIndexOf('};');
const day3Tail = seedOld.slice(day3Idx, tailEnd).trim();

let content = `/**
 * Scene graph — refined narrative copy
 */
const SCENES = {
${prologueRain}${head},

${dogLabelPass(day2Updated)},

${dogLabelPass(day3Tail)}
};

if (typeof module !== 'undefined') module.exports = { SCENES };
`;

// replay patches from transcript
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

let applied = 0;
for (const p of patches) {
  const { old_string, new_string, replace_all } = p;
  if (!old_string || new_string === undefined) continue;
  if (old_string.length < 15) continue;
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

content = dogLabelPass(content);

fs.writeFileSync(out, content, 'utf8');
console.log('Wrote scenes.js, patches applied:', applied);

try {
  require('child_process').execSync(`node --check "${out}"`, { stdio: 'pipe' });
  console.log('Syntax OK');
} catch (e) {
  console.error('Syntax fail:', e.stderr?.toString());
  process.exit(1);
}
