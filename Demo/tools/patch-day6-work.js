const fs = require('fs');
const p = 'c:/Users/BaoGo/Documents/ClaudeCode_Project/Learn_How_To_Love/Demo/js/choice-reactions.js';
let t = fs.readFileSync(p, 'utf8');

const oldKey = "'day6_morning::午後，雲慢慢厚了……'";
const newKey = "'day6_morning::關上門，搭車去公司……'";
const newBlock = `  ${newKey}: {
    text: (s) => \`\${dogLabel(s)} 在門內輕輕哼了一聲，像知道你要走了。\`,
    feeling: 'anxious', cue: 'whineSoft',
  },`;

if (t.includes(oldKey)) {
  t = t.replace(
    /  'day6_morning::午後，雲慢慢厚了……': \{[\s\S]*?\n  \},/,
    newBlock
  );
  fs.writeFileSync(p, t, 'utf8');
  console.log('updated day6_morning reaction key');
} else if (t.includes(newKey)) {
  console.log('day6_morning already updated');
} else {
  console.log('WARN: day6_morning key not found');
}
