const fs = require('fs');
const p = 'c:/Users/BaoGo/Documents/ClaudeCode_Project/Learn_How_To_Love/Demo/js/choice-reactions.js';
let t = fs.readFileSync(p, 'utf8');

const patches = [
  [
    /  'day4_vet_go::推開寵物醫院的門……': \{[\s\S]*?\n  \},/,
    `  'day4_vet_go::推開寵物醫院的門……': {
    text: (s) => \`\${dogLabel(s)} 在你懷裡縮得更小，鼻子還貼著你的頸邊。\`,
    feeling: 'anxious', cue: 'sniffQuick', pose: 'vet-carry',
  },`,
  ],
  [
    /  'day4_vet_reception::照實填：剛帶回家幾天，還在適應、偶爾會叫': \{[\s\S]*?\n  \},/,
    `  'day4_vet_reception::照實填：剛帶回家幾天，還在適應、偶爾會叫': {
    text: (s) => \`\${dogLabel(s)} 在你懷裡輕輕哼了一聲，鼻子仍貼著你，像在聞。\`,
    feeling: 'shy', cue: 'sniff', holdMs: 1400,
  },`,
  ],
  [
    /  'day4_vet_reception::簡短填完重點，先輕聲安撫懷裡的牠': \{[\s\S]*?\n  \},/,
    `  'day4_vet_reception::簡短填完重點，先輕聲安撫懷裡的牠': {
    text: (s) => \`\${dogLabel(s)} 的呼吸慢了一點，在陌生氣味裡只往你身上靠。\`,
    feeling: 'anxious', cue: 'breathEase', pose: 'vet-carry',
  },`,
  ],
];

patches.forEach(([re, block]) => {
  if (re.test(t)) t = t.replace(re, block);
});

fs.writeFileSync(p, t, 'utf8');
console.log('patched vet scent choice reactions');
