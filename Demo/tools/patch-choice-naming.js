const fs = require('fs');
const p = require('path').join(__dirname, '../js/choice-reactions.js');
let cr = fs.readFileSync(p, 'utf8');

const re = /  'prologue_home::[^']+': \{[\s\S]*?\n  \},\n\n  'day2_morning::/;
if (!re.test(cr)) {
  console.error('Block not found');
  process.exit(1);
}

const insert = `  'prologue_home::深吸一口氣，手忙腳亂找毛巾和吹風機': {
    text: (s) => \`\${dogLabel(s)} 跟著你轉圈，尾巴夾緊，不知道你要做什麼。\`,
    feeling: 'anxious', cue: 'whimperScared',
  },

  'prologue_dry::吹風機調到低檔，先讓牠聞聞風': {
    text: (s) => \`\${dogLabel(s)} 嗅了嗅風，身子還緊，但沒有再掙。\`,
    feeling: 'shy', cue: 'sniffQuick',
  },
  'prologue_dry::一手按穩、一手吹，越弄越亂也沒停': {
    text: (s) => \`\${dogLabel(s)} 被毛巾裹著，只露出一雙濕漉漉的眼睛。\`,
    feeling: 'anxious', cue: 'whineSoft',
  },
  'prologue_dry::放棄吹風機，只用毛巾慢慢擦到半乾': {
    text: (s) => \`\${dogLabel(s)} 在毛巾裡慢慢鬆了一點，像終於不那麼冷。\`,
    feeling: 'curious', cue: 'breathEase',
  },

  'prologue_night::走到三步外，輕聲說：「我在，沒事了。」': {
    text: (s) => \`\${dogLabel(s)} 的哀鳴短了一拍，又低低地哼了一聲。\`,
    feeling: 'shy', cue: 'whineSoft', holdMs: 1800,
  },
  'prologue_night::開小夜燈，坐在地上，不強抱，等聲音慢下來': {
    text: (s) => \`\${dogLabel(s)} 的呼吸漸漸和你同步，哀鳴一聲比一聲輕。\`,
    feeling: 'content', cue: 'sleepBreath', holdMs: 2000,
  },
  'prologue_night::困得發煩，還是壓低聲音陪在遠處': {
    text: (s) => \`\${dogLabel(s)} 仍偶爾哼一下，但沒有再撕心裂肺地叫。\`,
    feeling: 'anxious', cue: 'whimperQuiet', holdMs: 1600,
  },

  'prologue_dawn::熬到天亮……': {
    text: (s) => \`\${dogLabel(s)} 在紙箱邊睡著了，呼吸比夜裡穩一點。\`,
    feeling: 'sleepy', cue: 'sleepBreathDeep', holdMs: 1500,
  },

  'day2_leave::回覆主管：「謝謝，明天會補上進度。」': {
    text: (s) => \`\${dogLabel(s)} 不知道你在忙什麼，只是安靜地待著。\`,
    feeling: 'anxious', cue: 'breathEase',
  },
  'day2_leave::打電話簡單說明：昨天帶回一隻狗，需要一天安顿': {
    text: (s) => \`\${dogLabel(s)} 的耳朵動了一下，像聽見你聲音裡的緊張。\`,
    feeling: 'curious', cue: 'huffSoft',
  },

  'day2_petshop::「第一晚整晚哀鳴……這樣正常嗎？」': {
    text: () => '（牠在家裡的紙箱邊，還不知道你正在為牠問這些。）',
    feeling: 'anxious', cue: 'whimperQuiet', holdMs: 1200,
  },
  'day2_petshop::「請幫我配齊：糧、碗、尿墊、小毯。」': {
    text: () => '（店員點點頭，開始幫你挑適合幼犬的東西。）',
    feeling: 'curious', cue: 'sniffQuick', holdMs: 1100,
  },
  'day2_petshop::小聲問：「我是不是太衝動了？」': {
    text: () => '（店員笑了：「衝動沒關係，後面肯學就好。」）',
    feeling: 'hurt', cue: 'breathEase', holdMs: 1300,
  },

  'day2_petshop_after::「還沒想好……可以現在取嗎？」': {
    text: () => '（店員把紙筆推過來，等你想一個名字。）',
    feeling: 'curious', cue: 'breathEase', holdMs: 1200,
  },

  'day2_return::換好水，開始這個請假的早晨': {
    text: (s) => \`\${dogLabel(s)} 的鼻子貼向新食盆，又迅速縮回去。\`,
    feeling: 'curious', cue: 'sniffDeep',
  },

  'day2_morning::`;

cr = cr.replace(re, insert);
fs.writeFileSync(p, cr, 'utf8');
console.log('patched choice-reactions naming keys');
