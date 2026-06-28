const fs = require('fs');
const path = require('path');

const OUT = path.join(__dirname, '../js/choice-reactions.js');
let t = fs.readFileSync(OUT, 'utf8');

if (t.includes('day4_vet_reception::')) {
  console.log('already patched');
  process.exit(0);
}

const add = `
  'day4_vet_reception::照實填：剛帶回家幾天，還在適應、偶爾會叫': {
    text: (s) => \`\${dogLabel(s)} 在你懷裡輕輕哼了一聲，像被說中了什麼。\`,
    feeling: 'shy', cue: 'whineSoft', holdMs: 1400,
  },
  'day4_vet_reception::簡短填完重點，先輕聲安撫懷裡的牠': {
    text: (s) => \`\${dogLabel(s)} 的呼吸慢了一點，耳朵還貼著你的手臂。\`,
    feeling: 'anxious', cue: 'breathEase', pose: 'vet-carry',
  },

  'day4_vet_intake::坦白說：會擔心我出門，半夜有時還會叫': {
    text: (s) => \`\${dogLabel(s)} 把臉藏進你袖口，但身子往你懷裡靠了靠。\`,
    feeling: 'attached', cue: 'whineSoft', pose: 'vet-carry', holdMs: 1600,
  },
  'day4_vet_intake::主要想了解疫苗，其他還在觀察': {
    text: (s) => \`\${dogLabel(s)} 的耳朵動了一下，像在聽你說話。\`,
    feeling: 'curious', cue: 'sniff', pose: 'vet-carry',
  },
  'day4_vet_intake::請醫生依表單和檢查再判斷，我配合回答': {
    text: (s) => \`\${dogLabel(s)} 沒有掙開，鼻子在你腕上輕輕蹭了一下。\`,
    feeling: 'content', cue: 'sigh', pose: 'vet-carry',
  },
`;

t = t.replace(/\n};\n\nfunction choiceReactionKey/, `${add}\n};\n\nfunction choiceReactionKey`);
fs.writeFileSync(OUT, t, 'utf8');
console.log('patched day4 vet reactions');
