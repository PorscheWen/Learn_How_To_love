/**
 * Traditional Chinese (Taiwan) + common simplified fixes across Demo copy.
 */
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const targets = [
  'js/scenes.js',
  'js/choice-reactions.js',
  'js/story-agent.js',
  'js/minigame-reactions.js',
  'js/systems.js',
  'js/game.js',
  'index.html',
];

const pairs = [
  ['塑料', '塑膠'],
  ['写的', '寫的'],
  ['打扰', '打擾'],
  ['轻轻', '輕輕'],
  ['在问：', '在問：'],
  ['还在', '還在'],
  ['你会', '你會'],
  ['跟着', '跟著'],
  ['跟脚', '跟腳'],
  ['看见', '看見'],
  ['考试', '考試'],
  ['信息', '訊息'],
  ['deadline', '交件期限'],
  [' routine', ' 日常節奏'],
  ['固定 routine', '固定日常節奏'],
  ['安顿', '安頓'],
  ['便条', '便條'],
  ['吗？', '嗎？'],
  ['吗？', '嗎？'],
  ['你在吗', '你還在嗎'],
  ['你会等我吗', '你會等我嗎'],
];

let total = 0;
for (const rel of targets) {
  const fp = path.join(root, rel);
  if (!fs.existsSync(fp)) continue;
  let s = fs.readFileSync(fp, 'utf8');
  let n = 0;
  for (const [a, b] of pairs) {
    if (!s.includes(a)) continue;
    const parts = s.split(a);
    if (parts.length > 1) {
      n += parts.length - 1;
      s = parts.join(b);
    }
  }
  if (n) {
    fs.writeFileSync(fp, s, 'utf8');
    console.log(rel, n, 'replacements');
    total += n;
  }
}
console.log('Total:', total);
