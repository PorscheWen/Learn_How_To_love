/** 補齊 choice-reactions.js 佔位文案 */
const fs = require('fs');
const path = require('path');

const OUT = path.join(__dirname, '../js/choice-reactions.js');
let cr = fs.readFileSync(OUT, 'utf8');

const REPLACEMENTS = [
  [`  'day2_empty::深吸一口氣——得請假出去買': {
    text: (s) => \`\${dogLabel(s)} 對「深吸一口氣——得請假出去…」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day2_empty::深吸一口氣——得請假出去買': {
    text: (s) => \`\${dogLabel(s)} 餓得在碗邊轉圈，尾巴無力地垂著。\`,
    feeling: 'hungry', cue: 'sniffDeep', holdMs: 1400,
  },`],
  [`  'day2_rush::推開寵物店的門……': {
    text: (s) => \`\${dogLabel(s)} 對「推開寵物店的門……」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day2_rush::推開寵物店的門……': {
    text: () => '（風鈴響了一下，店裡飼料和木屑的氣味撲過來。）',
    feeling: 'anxious', cue: 'breathEase', holdMs: 1200,
  },`],
  [`  'day3_morning::輕聲喚牠的名字，在遠處坐下，等': {
    text: (s) => \`\${dogLabel(s)} 對「輕聲喚牠的名字，在遠處坐…」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_morning::輕聲喚牠的名字，在遠處坐下，等': {
    text: (s) => \`\${dogLabel(s)} 的耳朵動了一下，慢慢朝你挪過來。\`,
    feeling: 'curious', cue: 'sniffQuick',
  },`],
  [`  'day3_morning::心裡著急，提高音量：「過來！」': {
    text: (s) => \`\${dogLabel(s)} 對「心裡著急，提高音量：「過…」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_morning::心裡著急，提高音量：「過來！」': {
    text: (s) => \`\${dogLabel(s)} 整個身子一縮，退回了紙箱邊。\`,
    feeling: 'hurt', cue: 'whimperScared',
  },`],
  [`  'day3_morning::保持距離，用眼神和牠說：我在這': {
    text: (s) => \`\${dogLabel(s)} 對「保持距離，用眼神和牠說：…」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_morning::保持距離，用眼神和牠說：我在這': {
    text: (s) => \`\${dogLabel(s)} 從爪子後面探出半個鼻子，確認你還在。\`,
    feeling: 'shy', cue: 'murmurLow',
  },`],
  [`  'day3_morning::看時鐘，先衝去廚房準備早餐': {
    text: (s) => \`\${dogLabel(s)} 對「看時鐘，先衝去廚房準備早…」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_morning::看時鐘，先衝去廚房準備早餐': {
    text: (s) => \`\${dogLabel(s)} 還沒準備好，就被你的腳步聲嚇了一跳。\`,
    feeling: 'hungry', cue: 'sniffDeep',
  },`],
  [`  'day3_hurt::深呼吸，先去拿水盆和毛巾': {
    text: (s) => \`\${dogLabel(s)} 對「深呼吸，先去拿水盆和毛巾」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_hurt::深呼吸，先去拿水盆和毛巾': {
    text: (s) => \`\${dogLabel(s)} 仍縮在角落，不敢靠近。\`,
    feeling: 'anxious', cue: 'murmurUneasy',
  },`],
  [`  'day3_curious::伸出手，掌心朝上，不拉、不拽': {
    text: (s) => \`\${dogLabel(s)} 對「伸出手，掌心朝上，不拉、…」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_curious::伸出手，掌心朝上，不拉、不拽': {
    text: (s) => \`\${dogLabel(s)} 嗅了嗅你的掌心，沒有立刻舔，但沒有躲。\`,
    feeling: 'curious', cue: 'sniff',
  },`],
  [`  'day3_leave_home::搭車去公司，心卻一直留在身後那扇門……': {
    text: (s) => \`\${dogLabel(s)} 對「搭車去公司，心卻一直留在…」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_leave_home::搭車去公司，心卻一直留在身後那扇門……': {
    text: (s) => \`\${dogLabel(s)} 不知道你去了哪，只知道門又關上了。\`,
    feeling: 'anxious', cue: 'whimperQuiet',
  },`],
  [`  'day3_work_worry::傳訊息跟主管：「家裡有事，能提早離開嗎？」': {
    text: (s) => \`\${dogLabel(s)} 對「傳訊息跟主管：「家裡有事…」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_work_worry::傳訊息跟主管：「家裡有事，能提早離開嗎？」': {
    text: () => '（螢幕亮了一下——你等回覆的每一秒都很長。）',
    feeling: 'anxious', cue: 'murmurLow',
  },`],
  [`  'day3_work_worry::硬撐到十點，還是忍不住請假': {
    text: (s) => \`\${dogLabel(s)} 對「硬撐到十點，還是忍不住請…」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_work_worry::硬撐到十點，還是忍不住請假': {
    text: () => '（會議裡你點著頭，心卻早就飛回那扇門。）',
    feeling: 'anxious', cue: 'huff',
  },`],
  [`  'day3_work_worry::試著專心，但心越來越沉——還是決定先回家': {
    text: (s) => \`\${dogLabel(s)} 對「試著專心，但心越來越沉—…」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_work_worry::試著專心，但心越來越沉——還是決定先回家': {
    text: () => '（你合上筆電，比任何一次下班都急。）',
    feeling: 'anxious', cue: 'breathEase',
  },`],
  [`  'day3_leave_early::轉角看見自家那棟樓……': {
    text: (s) => \`\${dogLabel(s)} 對「轉角看見自家那棟樓……」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_leave_early::轉角看見自家那棟樓……': {
    text: (s) => \`\${dogLabel(s)} 還不知道，你已經在轉角了。\`,
    feeling: 'excited', cue: 'yipExcited',
  },`],
  [`  'day3_afternoon::趁著天還亮，帶牠去尿墊旁練習一下': {
    text: (s) => \`\${dogLabel(s)} 對「趁著天還亮，帶牠去尿墊旁…」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_afternoon::趁著天還亮，帶牠去尿墊旁練習一下': {
    text: (s) => \`\${dogLabel(s)} 在尿墊邊嗅了嗅，像在找「對的地方」。\`,
    feeling: 'curious', cue: 'sniffDeep', pose: 'potty',
  },`],
  [`  'day3_afternoon::天色漸漸暗下來……': {
    text: (s) => \`\${dogLabel(s)} 對「天色漸漸暗下來……」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_afternoon::天色漸漸暗下來……': {
    text: (s) => \`\${dogLabel(s)} 在客廳邊緣打盹，呼吸漸漸變長。\`,
    feeling: 'sleepy', cue: 'sleepBreath', holdMs: 3800,
  },`],
  [`  'day3_night::不罵。清理完，陪牠坐在尿墊旁': {
    text: (s) => \`\${dogLabel(s)} 對「不罵。清理完，陪牠坐在尿…」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_night::不罵。清理完，陪牠坐在尿墊旁': {
    text: (s) => \`\${dogLabel(s)} 把頭輕輕靠在你膝上，沒有聲音。\`,
    feeling: 'attached', cue: 'whineSoft', pose: 'knee', holdMs: 1800,
  },`],
  [`  'day3_night::嘆氣，默默清理，回房關上門': {
    text: (s) => \`\${dogLabel(s)} 對「嘆氣，默默清理，回房關上…」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_night::嘆氣，默默清理，回房關上門': {
    text: (s) => \`\${dogLabel(s)} 獨自縮在角落，聽見門關上的聲音。\`,
    feeling: 'hurt', cue: 'whimperQuiet',
  },`],
  [`  'day3_night::吼了出來，把牠關進浴室': {
    text: (s) => \`\${dogLabel(s)} 對「吼了出來，把牠關進浴室」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day3_night::吼了出來，把牠關進浴室': {
    text: (s) => \`\${dogLabel(s)} 在門後發抖，整個身子都蜷起來。\`,
    feeling: 'angry', cue: 'whimperScared',
  },`],
  [`  'day4_vet_go::推開寵物醫院的門……': {
    text: (s) => \`\${dogLabel(s)} 對「推開寵物醫院的門……」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day4_vet_go::推開寵物醫院的門……': {
    text: (s) => \`\${dogLabel(s)} 在你懷裡縮得更小，耳朵貼著你的胸口。\`,
    feeling: 'anxious', cue: 'murmurAnxious', pose: 'shy',
  },`],
  [`  'day6_check::……': {
    text: (s) => \`\${dogLabel(s)} 對「……」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day6_check::……': {
    text: (s) => \`\${dogLabel(s)} 在窗邊打盹，耳朵隨遠處的風聲輕輕動。\`,
    feeling: 'content', cue: 'sleepSnore', holdMs: 2000,
  },`],
  [`  'day7_moment::……': {
    text: (s) => \`\${dogLabel(s)} 對「……」有了反應。\`,
    feeling: 'curious', cue: 'huff',
  },`, `  'day7_moment::……': {
    text: (s) => \`\${dogLabel(s)} 呼吸和你同步，像 Day 3 那夜一樣輕。\`,
    feeling: 'attached', cue: 'sleepBreath', pose: 'knee', holdMs: 2000,
  },`],
];

let n = 0;
for (const [oldBlock, newBlock] of REPLACEMENTS) {
  if (cr.includes(oldBlock)) {
    cr = cr.replace(oldBlock, newBlock);
    n += 1;
  } else {
    console.warn('skip (pattern not found):', oldBlock.slice(0, 40));
  }
}

// 移除重複的 day2_morning 佔位（正確版已在上方）
cr = cr.replace(
  /\n  'day2_morning::先不打擾，讓牠自己決定什麼時候動': \{\n    text: \(s\) => `\$\{dogLabel\(s\)\} 對「[^`]+」有了反應。`,\n    feeling: 'curious', cue: 'huff',\n  \},/,
  ''
);

// 移除舊 key day7_moment::靜靜地…
cr = cr.replace(
  /\n  'day7_moment::靜靜地，讓這一刻留久一點': \{[\s\S]*?\n  \},/,
  ''
);

fs.writeFileSync(OUT, cr, 'utf8');
console.log('replaced', n, 'entries');
console.log('has placeholder', cr.includes('有了反應'));
