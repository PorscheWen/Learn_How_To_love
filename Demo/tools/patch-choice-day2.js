const fs = require('fs');
const p = require('path').join(__dirname, '../js/choice-reactions.js');
let cr = fs.readFileSync(p, 'utf8');

cr = cr.replace(
  `'prologue_dawn::熬到天亮……': {
    text: (s) => \`\${dogLabel(s)} 在紙箱邊睡著了，呼吸比夜裡穩一點。\`,
    feeling: 'sleepy', cue: 'sleepBreathDeep', holdMs: 1500,
  },

  'day2_leave::`,
  `'prologue_dawn::撐到起床……': {
    text: (s) => \`\${dogLabel(s)} 在紙箱邊動了動，還不知道今天會發生什麼。\`,
    feeling: 'sleepy', cue: 'sleepBreathDeep', holdMs: 1600,
  },

  'day2_empty::深吸一口氣——得請假出去買': {
    text: (s) => \`\${dogLabel(s)} 望著空碗，輕輕嗅了一下。\`,
    feeling: 'hungry', cue: 'sniffDeep', holdMs: 1400,
  },

  'day2_leave::`
);

cr = cr.replace(
  /  'day2_petshop::[\s\S]*?  'day2_petshop_after::/,
  `  'day2_rush::推開寵物店的門……': {
    text: () => '（風鈴響了一下，店裡飼料和木屑的氣味撲過來。）',
    feeling: 'anxious', cue: 'breathEase', holdMs: 1200,
  },

  'day2_petshop_after::`
);

fs.writeFileSync(p, cr, 'utf8');
console.log('choice-reactions day2 flow patched');
