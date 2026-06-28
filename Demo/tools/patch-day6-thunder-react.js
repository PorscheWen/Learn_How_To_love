const fs = require('fs');
const p = 'c:/Users/BaoGo/Documents/ClaudeCode_Project/Learn_How_To_Love/Demo/js/choice-reactions.js';
let t = fs.readFileSync(p, 'utf8');

const oldBlock = /  'day6_thunder::開小夜燈，坐在地上，不強拉、不責怪': \{[\s\S]*?\n  \},/;
const newBlock = `  'day6_thunder::開小夜燈，坐在地上，不強拉、不責怪': {
    text: (s) => {
      const tier = s.flags?.thunderComfortTier;
      if (tier === 'perfect' || tier === 'good') {
        return \`\${dogLabel(s)} 從桌底探出頭，慢慢挪到你膝邊。\`;
      }
      return \`\${dogLabel(s)} 仍有些抖，但沒有再躲開你的手。\`;
    },
    feeling: 'content', cue: 'breathEase', pose: 'knee', holdMs: 2000,
  },`;

if (oldBlock.test(t)) {
  t = t.replace(oldBlock, newBlock);
  fs.writeFileSync(p, t, 'utf8');
  console.log('updated day6_thunder choice reaction');
} else {
  console.log('pattern not found — skip');
}
