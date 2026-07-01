/**
 * 每個選項 → 專屬狗狗反應（行為文案 + feeling + cue + 可選 pose）
 * key: `${sceneId}::${choice.text}`
 */
const CHOICE_REACTIONS = {
  'prologue_rain::用毛巾輕輕包住，抱上計程車': {
    text: (s) => `${dogLabel(s)} 在你懷裡抖了一下，沒有掙扎。`,
    feeling: 'anxious', cue: 'softWhimper',
  },

  'prologue_home::深吸一口氣，手忙腳亂找毛巾和吹風機': {
    text: (s) => `${dogLabel(s)} 跟著你轉圈，尾巴夾緊，不知道你要做什麼。`,
    feeling: 'anxious', cue: 'whimperScared',
  },

  'prologue_dry::吹風機調到低檔，先讓牠聞聞風': {
    text: (s) => `${dogLabel(s)} 嗅了嗅風，身子還緊，但沒有再掙。`,
    feeling: 'shy', cue: 'sniffQuick',
  },
  'prologue_dry::一手按穩、一手吹，越弄越亂也沒停': {
    text: (s) => `${dogLabel(s)} 被毛巾裹著，只露出一雙濕漉漉的眼睛。`,
    feeling: 'anxious', cue: 'whineSoft',
  },
  'prologue_dry::放棄吹風機，只用毛巾慢慢擦到半乾': {
    text: (s) => `${dogLabel(s)} 在毛巾裡慢慢鬆了一點，像終於不那麼冷。`,
    feeling: 'curious', cue: 'breathEase',
  },

  'prologue_night::走到三步外，輕聲說：「我在，沒事了。」': {
    text: (s) => `${dogLabel(s)} 的哀鳴短了一拍，又低低地哼了一聲。`,
    feeling: 'shy', cue: 'whineSoft', holdMs: 1800,
  },
  'prologue_night::開小夜燈，坐在地上，不強抱，等聲音慢下來': {
    text: (s) => `${dogLabel(s)} 的呼吸漸漸和你同步，哀鳴一聲比一聲輕。`,
    feeling: 'content', cue: 'sleepBreath', holdMs: 2000,
  },
  'prologue_night::困得發煩，還是壓低聲音陪在遠處': {
    text: (s) => `${dogLabel(s)} 仍偶爾哼一下，但沒有再撕心裂肺地叫。`,
    feeling: 'anxious', cue: 'whimperQuiet', holdMs: 1600,
  },

  'prologue_dawn::撐到起床……': {
    text: (s) => `${dogLabel(s)} 在紙箱邊睡著了，呼吸比夜裡穩一點。`,
    feeling: 'sleepy', cue: 'sleepSnoreDeep', holdMs: 4800,
  },

  'day2_leave::回覆主管：「謝謝，明天會補上進度。」': {
    text: (s) => `${dogLabel(s)} 不知道你在忙什麼，只是安靜地待在紙箱邊。`,
    feeling: 'anxious', cue: 'breathEase',
  },
  'day2_leave::打電話跟主管說：昨天帶回一隻狗，今天需要在家安頓一下': {
    text: (s) => `${dogLabel(s)} 的耳朵動了一下，像聽見你聲音裡的緊。`,
    feeling: 'curious', cue: 'huffSoft',
  },

  'day2_petshop_after::「還沒想好……可以現在取嗎？」': {
    text: () => '（店員把紙筆推過來，等你想一個名字。）',
    feeling: 'curious', cue: 'breathEase', holdMs: 1200,
  },

  'day2_return::先換好水，從第一件小事開始學著照顧牠': {
    text: (s) => `${dogLabel(s)} 的鼻子貼向新食盆，又迅速縮回去。`,
    feeling: 'curious', cue: 'sniffDeep',
  },

  'day2_morning::換好水，輕聲說早，不靠近': {
    text: (s) => `${dogLabel(s)} 的耳朵動了一下，沒有抬頭，但沒有再縮。`,
    feeling: 'curious', cue: 'sniff',
  },
  'day2_morning::先不打擾，讓牠自己決定什麼時候動': {
    text: (s) => `${dogLabel(s)} 從爪子後面探出半個鼻子，確認你還在。`,
    feeling: 'shy', cue: 'softWhimper',
  },
  'day2_morning::伸手想確認：你還在、我也還在': {
    text: (s) => `${dogLabel(s)} 整個身子一縮，把臉藏起來。`,
    feeling: 'hurt', cue: 'whimper',
  },

  'day2_wait::點頭，仍保持距離，把早餐放在廚房門口': {
    text: (s) => `${dogLabel(s)} 慢慢往廚房方向挪了一步。`,
    feeling: 'curious', cue: 'sniff',
  },

  'day2_hurt::深呼吸，先去準備早餐': {
    text: (s) => `${dogLabel(s)} 的視線仍偏向別處，但沒有再退。`,
    feeling: 'anxious', cue: 'softWhimper',
  },

  'day2_kitchen::退到客廳，留給牠空間': {
    text: (s) => `${dogLabel(s)} 等你看不見了，才小心地靠近碗。`,
    feeling: 'curious', cue: 'sniff',
  },
  'day2_kitchen::蹲在門邊，不越線，等': {
    text: (s) => `${dogLabel(s)} 嗅了嗅你的氣味，還是沒有舔。`,
    feeling: 'shy', cue: 'softWhimper',
  },
  'day2_kitchen::「快吃啊。」把碗推近': {
    text: (s) => `${dogLabel(s)} 往後退半步，碗邊只少了一小口。`,
    feeling: 'anxious', cue: 'huff',
  },

  'day2_midday::午後，光線斜進客廳……': {
    text: (s) => `${dogLabel(s)} 在光斑邊趴了一會，像終於敢把肚子貼地。`,
    feeling: 'content', cue: 'sigh', holdMs: 1400,
  },

  'day2_afternoon::用平常的語氣說：「沒事，我在。」': {
    text: (s) => `${dogLabel(s)} 看你一眼，肩膀慢慢放下來。`,
    feeling: 'curious', cue: 'huff',
  },
  'day2_afternoon::把牠抱到膝上，想讓牠別怕': {
    text: (s) => `${dogLabel(s)} 身體還是緊的，但沒有掙扎。`,
    feeling: 'anxious', cue: 'whimper',
  },
  'day2_afternoon::一起安靜坐著，等聲音過去': {
    text: (s) => `${dogLabel(s)} 在你腳邊蜷起來，呼吸和你同步。`,
    feeling: 'content', cue: 'sigh',
  },

  'day2_evening::Day 3 的早晨……': {
    text: (s) => `${dogLabel(s)} 比昨夜靠近了半步，像記住了這個房間。`,
    feeling: 'sleepy', cue: 'sigh', holdMs: 1500,
  },


  'day3_breakfast_rush::匆忙倒好飼料，來不及等牠吃完就出門': {
    text: (s) => `${dogLabel(s)} 還在舔碗邊，門已經關上了。`,
    feeling: 'anxious', cue: 'whimperQuiet',
  },
  'day3_breakfast_rush::邊綁鞋帶邊推碗靠近：「乖乖的，我很快回來。」': {
    text: (s) => `${dogLabel(s)} 抬頭看你，尾巴輕輕動了一下。`,
    feeling: 'shy', cue: 'whineSoft',
  },
  'day3_breakfast_rush::硬是多留五分鐘，看牠舔了一口才走': {
    text: (s) => `${dogLabel(s)} 舔完那一口，還追著你的腳步到門口。`,
    feeling: 'curious', cue: 'sniffQuick',
  },

  'day3_homecoming::蹲下來，什麼都不說，先讓牠聞聞你': {
    text: (s) => `${dogLabel(s)} 的鼻子在你手背上蹭了蹭，整個身子慢慢鬆下來。`,
    feeling: 'attached', cue: 'breathEase', pose: 'doorway-lie', holdMs: 2000,
  },
  'day3_homecoming::輕聲說：「對不起，讓你等了。」': {
    text: (s) => `${dogLabel(s)} 把頭靠過來，像終於等到這句話。`,
    feeling: 'content', cue: 'sigh', pose: 'doorway-lie',
  },
  'day3_homecoming::看見家裡還算整齊，鬆了口氣，把牠抱緊一點': {
    text: (s) => `${dogLabel(s)} 在你懷裡打了個小哈欠，尾巴輕輕掃過你的手腕。`,
    feeling: 'curious', cue: 'whineSoft', pose: 'doorway-lie',
  },

  'day3_night_after::摸一摸牠的頭，關燈': {
    text: (s) => `${dogLabel(s)} 沒有再驚醒，呼吸漸漸變長。`,
    feeling: 'attached', cue: 'sleepSnoreDeep', holdMs: 4800,
  },

  'day4_repair::蹲下，說對不起，拿出牠最愛的玩具': {
    text: (s) => `${dogLabel(s)} 愣了一下，慢慢把鼻子蹭向你手心。`,
    feeling: 'curious', cue: 'yipBright', pose: 'toy',
  },
  'day4_repair::照常餵食，不說話，但也不離開': {
    text: (s) => `${dogLabel(s)} 吃掉飯粒，仍與你保持半步距離。`,
    feeling: 'anxious', cue: 'murmurLow',
  },

  'day4_off::幫牠系好牽繩，出門往寵物醫院': {
    text: (s) => `${dogLabel(s)} 在門口停了一下，還是跟你出門。`,
    feeling: 'anxious', cue: 'murmurUneasy', pose: 'walk',
  },
  'day4_off::先餵飽、安撫一下，再慢慢出門': {
    text: (s) => `${dogLabel(s)} 吃幾口後，把頭靠在你手背上。`,
    feeling: 'curious', cue: 'breathEase', pose: 'kitchen',
  },

  'day4_vet_bill::深吸一口氣，刷卡：這也是照顧牠的一部分': {
    text: (s) => `${dogLabel(s)} 不知道發生什麼，只是把鼻子埋進你的袖口。`,
    feeling: 'content', cue: 'sigh', holdMs: 1600,
  },
  'day4_vet_bill::先問清楚每一項，再付款——該花的不能省': {
    text: (s) => `${dogLabel(s)} 在你懷裡慢慢鬆下來，像信任你的決定。`,
    feeling: 'curious', cue: 'sniff', holdMs: 1500,
  },

  'day4_evening::Day 5 · 週日，早晨的陽光……': {
    text: (s) => `${dogLabel(s)} 在毯子上蜷成一團，呼吸漸漸變長。`,
    feeling: 'sleepy', cue: 'sleepSnoreDeep', holdMs: 4800,
  },

  'day5_sunday::把牠抱起來，從客廳開始慢慢認': {
    text: (s) => `${dogLabel(s)} 身子還有點僵，但沒有掙開。`,
    feeling: 'shy', cue: 'huff', pose: 'corner',
  },
  'day5_sunday::先坐在地板，讓牠自己靠過來再抱': {
    text: (s) => `${dogLabel(s)} 猶豫了一會，還是把頭靠過來。`,
    feeling: 'curious', cue: 'whineSoft', holdMs: 1400,
  },

  'day5_home_after::週日的午後，就這樣靜靜度過……': {
    text: (s) => `${dogLabel(s)} 把下巴擱在你膝上，像終於鬆了一口氣。`,
    feeling: 'content', cue: 'breathEase', pose: 'knee', holdMs: 1800,
  },

  'day5_evening::Day 6 的早晨……': {
    text: (s) => `${dogLabel(s)} 沒有驚醒，只在夢裡輕輕哼了一聲。`,
    feeling: 'attached', cue: 'sleepSnoreDeep', pose: 'knee', holdMs: 4200,
  },

  'day6_morning::關上門，搭車去公司……': {
    text: (s) => `${dogLabel(s)} 在門內輕輕哼了一聲，像知道你要走了。`,
    feeling: 'anxious', cue: 'whineSoft',
  },

  'day6_check::……': {
    text: (s) => `${dogLabel(s)} 在窗邊打盹，耳朵隨遠處的風聲輕輕動。`,
    feeling: 'content', cue: 'sleepSnore', holdMs: 2000,
  },

  'day6_quiet::Day 7……': {
    text: (s) => `${dogLabel(s)} 在沙發腳邊打盹，呼吸一起一伏。`,
    feeling: 'sleepy', cue: 'sigh', pose: 'home', holdMs: 1100,
  },

  'day6_thunder::開小夜燈，坐在地上，不強拉、不責怪': {
    text: (s) => {
      const tier = s.flags?.thunderComfortTier;
      if (tier === 'perfect' || tier === 'good') {
        return `${dogLabel(s)} 從桌底探出頭，慢慢挪到你膝邊。`;
      }
      return `${dogLabel(s)} 仍有些抖，但沒有再躲開你的手。`;
    },
    feeling: 'content', cue: 'breathEase', pose: 'knee', holdMs: 2000,
  },
  'day6_thunder::「沒什麼好怕的！」把牠從桌下拉出來': {
    text: (s) => `${dogLabel(s)} 夾緊尾巴，整個身子發抖。`,
    feeling: 'hurt', cue: 'whimper',
  },

  'day6_thunder_after::Day 7……': {
    text: (s) => `${dogLabel(s)} 從桌底慢慢挪出來，停在你膝邊。`,
    feeling: 'content', cue: 'sigh', pose: 'knee', holdMs: 1100,
  },

  'day7_morning::傍晚，你比平常更晚回家……': {
    text: (s) => `${dogLabel(s)} 在門口張望，聽見鑰匙聲就豎起耳朵。`,
    feeling: 'curious', cue: 'huff', pose: 'doorway-wait',
  },

  'day7_evening::進門，什麼也不說，直接坐在地板上': {
    text: (s) => `${dogLabel(s)} 沒有舔你滿臉，只是走過來，把頭靠在你膝上。`,
    feeling: 'attached', cue: 'sigh', pose: 'sad-day',
  },


  'day2_empty::深吸一口氣——得請假出去買': {
    text: (s) => `${dogLabel(s)} 餓得在碗邊轉圈，尾巴無力地垂著。`,
    feeling: 'hungry', cue: 'sniffDeep', holdMs: 1400,
  },

  'day2_rush::推開寵物店的門……': {
    text: () => '（風鈴響了一下，店裡飼料和木屑的氣味撲過來。）',
    feeling: 'anxious', cue: 'breathEase', holdMs: 1200,
  },


  'day3_morning::輕聲喚牠的名字，在遠處坐下，等': {
    text: (s) => `${dogLabel(s)} 的耳朵動了一下，慢慢朝你挪過來。`,
    feeling: 'curious', cue: 'sniffQuick',
  },

  'day3_morning::心裡著急，提高音量：「過來！」': {
    text: (s) => `${dogLabel(s)} 整個身子一縮，退回了紙箱邊。`,
    feeling: 'hurt', cue: 'whimperScared',
  },

  'day3_morning::保持距離，用眼神和牠說：我在這': {
    text: (s) => `${dogLabel(s)} 從爪子後面探出半個鼻子，確認你還在。`,
    feeling: 'shy', cue: 'murmurLow',
  },

  'day3_morning::看時鐘，先衝去廚房準備早餐': {
    text: (s) => `${dogLabel(s)} 還沒準備好，就被你的腳步聲嚇了一跳。`,
    feeling: 'hungry', cue: 'sniffDeep',
  },

  'day3_hurt::深呼吸，先去拿水盆和毛巾': {
    text: (s) => `${dogLabel(s)} 仍縮在角落，耳朵卻朝你的方向動了一下。`,
    feeling: 'anxious', cue: 'murmurUneasy',
  },

  'day3_curious::伸出手，掌心朝上，不拉、不拽': {
    text: (s) => `${dogLabel(s)} 嗅了嗅你的掌心，沒有立刻舔，但沒有躲。`,
    feeling: 'curious', cue: 'sniff',
  },

  'day3_leave_home::搭車去公司，心卻一直留在身後那扇門……': {
    text: (s) => `${dogLabel(s)} 不知道你去了哪，只知道門又關上了。`,
    feeling: 'anxious', cue: 'whimperQuiet',
  },

  'day3_work_worry::傳訊息跟主管：「家裡有事，能提早離開嗎？」': {
    text: () => '（螢幕亮了一下——你等回覆的每一秒都很長。）',
    feeling: 'anxious', cue: 'murmurLow',
  },

  'day3_work_worry::硬撐到十點，還是忍不住請假': {
    text: () => '（會議裡你點著頭，心卻早就飛回那扇門。）',
    feeling: 'anxious', cue: 'huff',
  },

  'day3_work_worry::試著專心，但心越來越沉——還是決定先回家': {
    text: () => '（你合上筆電，比任何一次下班都急。）',
    feeling: 'anxious', cue: 'breathEase',
  },

  'day3_leave_early::轉角看見自家那棟樓……': {
    text: (s) => `${dogLabel(s)} 還不知道，你已經在轉角了。`,
    feeling: 'excited', cue: 'yipExcited',
  },

  'day3_afternoon::趁著天還亮，帶牠去尿墊旁練習一下': {
    text: (s) => `${dogLabel(s)} 在尿墊邊嗅了嗅，像在找「對的地方」。`,
    feeling: 'curious', cue: 'sniffDeep', pose: 'potty',
  },

  'day3_afternoon::天色漸漸暗下來……': {
    text: (s) => `${dogLabel(s)} 在客廳邊緣打盹，呼吸漸漸變長。`,
    feeling: 'sleepy', cue: 'sleepBreath', holdMs: 3800,
  },

  'day3_night::不罵。清理完，陪牠坐在尿墊旁': {
    text: (s) => `${dogLabel(s)} 把頭輕輕靠在你膝上，沒有聲音。`,
    feeling: 'attached', cue: 'whineSoft', pose: 'knee', holdMs: 1800,
  },

  'day3_night::嘆氣，默默清理，回房關上門': {
    text: (s) => `${dogLabel(s)} 獨自縮在角落，聽見門關上的聲音。`,
    feeling: 'hurt', cue: 'whimperQuiet',
  },

  'day3_night::吼了出來，把牠關進浴室': {
    text: (s) => `${dogLabel(s)} 在門後發抖，身子蜷成一團。`,
    feeling: 'angry', cue: 'whimperScared',
  },

  'day4_vet_go::推開寵物醫院的門……': {
    text: (s) => `${dogLabel(s)} 在你懷裡縮得更小，鼻子還貼著你的頸邊。`,
    feeling: 'anxious', cue: 'sniffQuick', pose: 'vet-carry',
  },

  'day7_moment::……': {
    text: (s) => `${dogLabel(s)} 呼吸和你同步，像第三夜一樣輕。`,
    feeling: 'attached', cue: 'sleepBreath', pose: 'knee', holdMs: 2000,
  },
  'day4_vet_reception::照實填：剛帶回家幾天，還在適應、偶爾會叫': {
    text: (s) => `${dogLabel(s)} 在你懷裡輕輕哼了一聲，鼻子仍貼著你，像在聞。`,
    feeling: 'shy', cue: 'sniff', holdMs: 1400,
  },
  'day4_vet_reception::簡短填完重點，先輕聲安撫懷裡的牠': {
    text: (s) => `${dogLabel(s)} 的呼吸慢了一點，在陌生氣味裡只往你身上靠。`,
    feeling: 'anxious', cue: 'breathEase', pose: 'vet-carry',
  },

  'day4_vet_intake::坦白說：會擔心我出門，半夜有時還會叫': {
    text: (s) => `${dogLabel(s)} 把臉藏進你袖口，但身子往你懷裡靠了靠。`,
    feeling: 'attached', cue: 'whineSoft', pose: 'vet-carry', holdMs: 1600,
  },
  'day4_vet_intake::主要想了解疫苗，其他還在觀察': {
    text: (s) => `${dogLabel(s)} 的耳朵動了一下，像在聽你說話。`,
    feeling: 'curious', cue: 'sniff', pose: 'vet-carry',
  },
  'day4_vet_intake::請醫生依表單和檢查再判斷，我配合回答': {
    text: (s) => `${dogLabel(s)} 沒有掙開，鼻子在你腕上輕輕蹭了一下。`,
    feeling: 'content', cue: 'sigh', pose: 'vet-carry',
  },

};

function choiceReactionKey(sceneId, choiceText) {
  return `${sceneId}::${String(choiceText || '').trim()}`;
}

function lookupChoiceReaction(sceneId, choiceText) {
  return CHOICE_REACTIONS[choiceReactionKey(sceneId, choiceText)] || null;
}

if (typeof module !== 'undefined') {
  module.exports = { CHOICE_REACTIONS, choiceReactionKey, lookupChoiceReaction };
}
