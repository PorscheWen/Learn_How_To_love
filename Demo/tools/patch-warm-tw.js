const fs = require('fs');
const path = require('path');

const scenes = path.join(__dirname, '../js/scenes.js');
let s = fs.readFileSync(scenes, 'utf8');

s = s.replace(
  '你點頭。\n\n她指著貨架：\n「幼犬啊，不是買最貴的——\n是買對的。糧要幼犬專用，\n尿墊、淺碗、小毯，\n一件都不能拿錯。」\n\n你記下來，\n像記一張會考試的清單。',
  '你點頭，心裡還是虛虛的。\n\n她指著貨架，語氣放輕：\n「幼犬啊，不是買最貴的——\n是買對的。糧要幼犬專用，\n尿墊、淺碗、小毯，\n一件都不能拿錯。」\n\n你記下來，\n像記一張明天就要交的小考題目。'
);

s = s.replace(
  "sub: '貨架上什麼都有。\\n你得在這裡，\\n替牠挑對第一套「家」的東西。',",
  "sub: '貨架上什麼都有。\\n你得在這裡，\\n替牠挑對第一套「家」的東西——\\n心裡還慌，但總算有人可以問。',"
);
s = s.replace(
  "sub: '貨架上什麼都有。\\n你得在這裡，\\n替牠挑對第一套「家」的東西。',",
  "sub: '貨架上什麼都有。\\n你得在這裡，\\n替牠挑對第一套「家」的東西——\\n心裡還慌，但總算有人可以問。',"
);

fs.writeFileSync(scenes, s, 'utf8');

const cr = path.join(__dirname, '../js/choice-reactions.js');
let c = fs.readFileSync(cr, 'utf8');
c = c.replace(
  "'day2_leave::打電話簡單說明：昨天帶回一隻狗，需要一天安頓'",
  "'day2_leave::打電話跟主管說：昨天帶回一隻狗，今天需要在家安頓一下'"
);
fs.writeFileSync(cr, c, 'utf8');

const sys = path.join(__dirname, '../js/systems.js');
let sysContent = fs.readFileSync(sys, 'utf8');
sysContent = sysContent.replace(
  "follow_foot: { title: '第一次跟腳', desc: '回家路上，牠走在你腳邊。' }",
  "follow_foot: { title: '第一次跟腳', desc: '回家路上，牠走在你腳邊，一步也不願離太遠。' }"
);
fs.writeFileSync(sys, sysContent, 'utf8');

console.log('warm-tw patches applied');
