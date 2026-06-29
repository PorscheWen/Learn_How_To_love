/**
 * Scene graph — refined narrative copy
 */
const SCENES = {
  prologue_rain: {
    id: 'prologue_rain',
    day: 1,
    location: 'prologue_rain',
    music: 'melancholy',
    weather: 'rain',
    feeling: 'anxious',
    dogPose: 'rain',
    smell: '濕紙箱、雨水、微弱體溫',
    text: () => '傍晚，雨沒有要停的樣子。\n巷口那個紙箱輕輕動了一下——\n你蹲下去，對上一雙濕漉漉、還在發抖的眼睛。\n\n牠很小，毛貼著骨頭，像一整團被雨打溼的暖色。\n你用自己的外套先裹住，才發現牠沒有叫，只是很輕、很輕地靠過來。',
    sub: 'Day 1，你帶牠回家。\n那時候，你們都還不知道，這叫作「開始」。\n雨聲裡，卻已經多了一個小小呼吸——\n輕得幾乎聽不見，卻讓你捨不得走。',
    onEnter: (s) => { addMemory(s, 'prologue_rain'); },
    choices: [
      {
        text: '用毛巾輕輕包住，抱上計程車',
        effect: (s) => { applyTrust(s, 5); applyBondProgress(s, 10); },
        next: 'prologue_home',
      },
    ],
  },

  prologue_home: {
    id: 'prologue_home',
    day: 1,
    location: 'living_corner',
    music: 'night',
    feeling: 'anxious',
    dogPose: 'rain',
    smell: '新毯子、你的外套、仍帶雨氣的毛',
    text: (s) => `計程車在樓下停穩，你抱著 ${dogLabel(s)} 衝進電梯。\n\n門關上的瞬間，才發現牠從頭到腳都在滴水——\n毛巾、吹風機、溫水，你腦子裡亂成一團。\n\n${dogLabel(s)} 縮在你腳邊，\n小爪子把地磚印出一串濕痕。`,
    sub: '第一夜才剛開始。\n你還不知道該先做哪一步，\n心裡有點慌——\n但你知道，不能讓牠就這樣濕著過夜。',
    choices: [
      {
        text: '深吸一口氣，手忙腳亂找毛巾和吹風機',
        effect: (s) => { applyBondProgress(s, 5); },
        next: 'prologue_dry',
      },
    ],
  },

  prologue_dry: {
    id: 'prologue_dry',
    day: 1,
    location: 'bathroom_night',
    music: 'night',
    feeling: 'anxious',
    dogPose: 'wet',
    smell: '吹風機熱風、濕毛、你的洗手乳',
    text: (s) => `浴室鏡子蒙了一層霧。\n\n你一手按住 ${dogLabel(s)}，一手舉吹風機——\n牠一驚，掙了一下，毛巾滑到地上。\n你差點踩到，心跳快了一拍。\n\n「對不起、對不起……」\n你說得比平時更輕，\n像在跟一個也嚇壞了的小生命道歉。`,
    sub: '沒有誰教過你這個。\n你只能一邊試，一邊怕弄疼牠。',
    choices: [
      {
        text: '吹風機調到低檔，先讓牠聞聞風',
        effect: (s) => {
          applyTrust(s, 10);
          applyBondProgress(s, 12);
          s.flags.dryGentle = true;
          setFeeling(s, 'shy');
        },
        next: 'prologue_night',
      },
      {
        text: '一手按穩、一手吹，越弄越亂也沒停',
        effect: (s) => {
          applyTrust(s, 5);
          applyBondProgress(s, 8);
          setFeeling(s, 'anxious');
        },
        next: 'prologue_night',
      },
      {
        text: '放棄吹風機，只用毛巾慢慢擦到半乾',
        effect: (s) => {
          applyTrust(s, 8);
          applyBondProgress(s, 10);
          s.flags.dryGentle = true;
          setFeeling(s, 'curious');
        },
        next: 'prologue_night',
      },
    ],
  },

  prologue_night: {
    id: 'prologue_night',
    day: 1,
    location: 'bedroom_night',
    music: 'night',
    feeling: 'anxious',
    dogPose: 'corner',
    smell: '半乾的毛、小夜燈、深夜的安靜',
    text: (s) => `折騰完，${dogLabel(s)} 縮在紙箱邊。\n毛還有一點潮，但不再滴水。\n\n你開了小夜燈，在三步之外坐下——\n不靠近，也不離開。\n\n半夜，你還是醒了。\n\n低低的哀鳴從客廳傳來，\n一聲、停一下、又一聲——\n像把「怕」從喉嚨裡一點一點擠出來。`,
    sub: '你困得眼皮發酸，\n心裡卻也明白：\n這不是任性，是牠還沒學會——\n這裡，是可以安心睡的地方。',
    onEnter: (s) => { addMemory(s, 'first_night'); },
    choices: [
      {
        text: '走到三步外，輕聲說：「我在，沒事了。」',
        effect: (s) => {
          applyTrust(s, 10);
          applyBondProgress(s, 15);
          s.flags.firstNightCalm = true;
          s.flags.day2CalmSound = true;
          setFeeling(s, 'shy');
        },
        next: 'prologue_dawn',
      },
      {
        text: '開小夜燈，坐在地上，不強抱，等聲音慢下來',
        effect: (s) => {
          applyTrust(s, 12);
          applyBondProgress(s, 18);
          s.flags.firstNightCalm = true;
          s.flags.day2CalmSound = true;
          setFeeling(s, 'content');
        },
        next: 'prologue_dawn',
      },
      {
        text: '困得發煩，還是壓低聲音陪在遠處',
        effect: (s) => {
          applyTrust(s, 6);
          applyBondProgress(s, 10);
          setFeeling(s, 'anxious');
        },
        next: 'prologue_dawn',
      },
    ],
  },

  prologue_dawn: {
    id: 'prologue_dawn',
    day: 1,
    location: 'living_corner',
    music: 'calm',
    feeling: 'sleepy',
    dogPose: 'corner',
    smellAdd: '天亮前的薄光、終於乾了的毛',
    text: (s) => `天快亮時，哀鳴終於停了。\n\n${dogLabel(s)} 趴在紙箱邊，呼吸淺淺的，\n像耗盡了所有力氣。\n\n你也沒睡好——\n但看見牠還在，心裡還是鬆了一點。\n\n鬧鐘再響，就是 Day 2 了。\n你按掉鈴聲，還沒完全醒，\n就隱約覺得：今天有什麼不對。`,
    sub: '第一夜過去了。\n你們誰都還不完美，\n但總算一起撐到了天亮。',
    choices: [
      { text: '撐到起床……', effect: () => {}, next: 'day2_empty' },
    ],
  },

  day2_empty: {
    id: 'day2_empty',
    day: 2,
    location: 'kitchen',
    music: 'warm',
    feeling: 'anxious',
    hideDog: true,
    noDogAudio: true,
    smellAdd: '空食盆、清晨的急',
    text: (s) => `Day 2，早晨。\n\n${dogLabel(s)} 在紙箱邊動了動耳朵——\n你走去廚房，食盆是空的。\n\n櫃子裡沒有飼料。\n你昨天只想到帶牠回家，\n沒想到「明天」也需要一片乾糧。\n\n空碗輕輕晃了一下，\n發出很小、很空的聲音。`,
    sub: '心裡忽然一緊。\n養牠，不只是帶回家那麼浪漫——\n你得先讓這個小傢伙，有東西可以填飽肚子。',
    breathMs: 2800,
    textMult: 1.65,
    choices: [
      {
        text: '深吸一口氣——得請假出去買',
        effect: (s) => {
          applyBondProgress(s, 5);
          setFeeling(s, 'anxious');
        },
        next: 'day2_leave',
      },
    ],
  },

  day2_leave: {
    id: 'day2_leave',
    day: 2,
    location: 'living_room',
    music: 'warm',
    feeling: 'anxious',
    dogPose: 'corner',
    smellAdd: '清晨、未接來電、你的猶豫',
    text: (s) => `你捧著手機，\n在主管的名字上停很久。\n\n${dogLabel(s)} 不知道你在忙什麼，\n只是安靜地待在紙箱邊，\n偶爾抬眼看你一下。\n\n「家裡有急事……需要請一天假。」\n打完這行字，又刪掉重打。\n\n最後還是傳出去。\n螢幕顯示「已讀」時，\n你比帶 ${dogLabel(s)} 回家那夜還緊張。`,
    sub: '請假這件事，說出口才發現有點難為情。\n但空碗不會等你開完會。',
    breathMs: 2600,
    textMult: 1.55,
    choices: [
      {
        text: '回覆主管：「謝謝，明天會補上進度。」',
        effect: (s) => { applyBondProgress(s, 5); },
        next: 'day2_rush',
      },
      {
        text: '打電話跟主管說：昨天帶回一隻狗，今天需要在家安頓一下',
        effect: (s) => {
          applyTrust(s, 3);
          applyBondProgress(s, 8);
        },
        next: 'day2_rush',
      },
    ],
  },

  day2_rush: {
    id: 'day2_rush',
    day: 2,
    location: 'street',
    music: 'warm',
    feeling: 'anxious',
    smellAdd: '街風、匆忙的腳步',
    noDogAudio: true,
    text: () => `假請下來了。\n\n你衝出門，風把襯衫吹亂——\n腦子裡只剩一個念頭：買齊。\n\n寵物店在兩條街外。\n玻璃門後，貨架排得像救命的清單。\n\n你走得很快。\n不是趕交件期限，\n是趕著填飽那個空碗。`,
    sub: '手機震了一下——\n主管回：「好，先好好照顧小傢伙。」\n你來不及回，人已經在店門口了。',
    breathMs: 2600,
    textMult: 1.5,
    choices: [
      { text: '推開寵物店的門……', effect: () => {}, next: 'day2_petshop' },
    ],
  },

  day2_petshop: {
    id: 'day2_petshop',
    day: 2,
    location: 'pet_shop',
    music: 'warm',
    feeling: 'curious',
    smell: '飼料、木屑、新玩具的塑膠味',
    sceneArt: 'petshop-clerk',
    sceneArtAlt: '寵物店店員在貨架前笑著招呼',
    text: () => `寵物店門口風鈴響了一下。\n\n店員是個戴圍裙的大姐，\n看見你空手進來、一臉慌，就笑了：\n「第一次養？昨天帶回家的？」\n\n你點頭，心裡還是虛虛的。\n\n她指著貨架，語氣放輕：\n「幼犬啊，不是買最貴的——\n是買對的。糧要幼犬專用，\n尿墊、淺碗、小毯，\n一件都不能拿錯。」\n\n你記下來，\n像記一張明天就要交的小考題目。`,
    sub: '貨架上什麼都有。\n你得在這裡，\n替牠挑對第一套「家」的東西——\n心裡還慌，但總算有人可以問。',
    breathMs: 2800,
    textMult: 1.6,
    onEnter: (s) => { addMemory(s, 'day2_petshop'); },
    minigame: 'shop',
    next: 'day2_petshop_after',
  },

  day2_petshop_after: {
    id: 'day2_petshop_after',
    day: 2,
    location: 'pet_shop',
    music: 'warm',
    feeling: 'content',
    smellAdd: '店員的咖啡味、紙箱購物袋',
    sceneArt: 'petshop-checkout',
    sceneArtAlt: '店員在櫃台結帳',
    text: (s) => {
      const gentle = s.flags.dryGentle;
      const tier = s.flags.shopTier;
      let pickLine = '';
      if (tier === 'perfect' || tier === 'good') {
        pickLine = '她又看你一眼：「挑得不錯，幼犬要用的都有。」\n';
      } else if (tier === 'partial') {
        pickLine = '她幫你補了兩樣：「還差這個——幼犬不能省。」\n';
      } else if (tier === 'miss') {
        pickLine = '她替你換了兩樣：「這幾樣幼犬不能用，我幫你改。」\n';
      }
      return `結帳。\n\n店員把東西裝進紙箱，邊整理邊說：\n\n「幼犬第一晚叫，太正常了。\n換環境誰不怕？別罵，別硬抱。\n你穩，牠才穩。」\n\n${gentle ? '她又看你一眼：「吹乾有慢慢來吧？很好。」\n' : ''}${pickLine}「食盆放固定位置，尿墊先鋪在牠常待的角落。\n餓了會吃，怕了會叫——\n你要做的，是讓牠知道：你會回來。」\n\n紙箱裝滿了。\n她拍一拍袋口，忽然問：\n「對了——牠叫什麼名字？」`;
    },
    sub: '你愣了一下。\n昨天只顧著帶牠回家，\n還沒想過這件事。',
    breathMs: 2600,
    textMult: 1.5,
    choices: [
      { text: '「還沒想好……可以現在取嗎？」', effect: () => {}, next: 'day2_naming' },
    ],
  },

  day2_naming: {
    id: 'day2_naming',
    day: 2,
    location: 'pet_shop',
    music: 'warm',
    feeling: 'curious',
    smellAdd: '店員的咖啡味、紙箱購物袋',
    noSceneArt: true,
    namePrompt: true,
    text: () => `店員笑了，把收銀機旁的小紙條推過來。\n\n「當然可以啊。\n名字不用完美，\n只要是你願意叫牠的那一個就好。」\n\n你盯著紙箱發呆——\n腦子裡閃過很多字，\n最後留下一個你覺得\n念起來會比較溫柔的。`,
    sub: '替牠取名字吧。\n這專屬於你們之間，\n第一個記憶。',
    next: 'day2_gender',
  },

  day2_gender: {
    id: 'day2_gender',
    day: 2,
    location: 'pet_shop',
    music: 'warm',
    feeling: 'curious',
    smellAdd: '店員的咖啡味、紙箱購物袋',
    noSceneArt: true,
    genderPrompt: true,
    text: (s) => `店員把名字寫在便條上，\n又抬眼問：\n「對了，${dogLabel(s)} 是弟弟還是妹妹？」\n\n你停了一下，\n照著你心裡最自然的感覺回了一句。`,
    sub: '店員握著筆，等你回一句最自然的答案。',
    next: 'day2_return',
  },

  day2_return: {
    id: 'day2_return',
    day: 2,
    location: 'hallway',
    music: 'warm',
    feeling: 'curious',
    dogPose: 'corner',
    smellAdd: ['新買的飼料', '尿墊', '店員寫的便條'],
    text: (s) => {
      const clerkReply = s.dogGender === 'male'
        ? '店員點點頭笑了一下：「弟弟啊，很機靈，會很有自己脾氣的小傢伙。」\n\n'
        : s.dogGender === 'female'
          ? '店員點點頭笑了一下：「妹妹喔，很可愛，會是個黏人的小可愛。」\n\n'
          : '';
      return `${clerkReply}玄關鑰匙轉動的聲音，\n${dogLabel(s)} 的耳朵立刻豎起來。\n\n你提著購物袋進門，\n在門口低聲念了一次${dogLabel(s)}的名字——\n還不太習慣，但舌頭記住了。\n\n${dogPronoun(s)}沒有衝過來，只是從紙箱邊探頭，\n鼻子瘋狂地嗅：這些袋子裡，有沒有「好事」的味道。\n\n你把尿墊鋪好、食盆擺正，\n動作仍有些手忙腳亂，\n但比昨夜在浴室裡，穩了一點。`;
    },
    sub: (s) => applyDogPronouns('店員的話還在耳邊：\n「你穩，牠才穩。」\n你吸一口氣，心裡想著：\n今天，就從小地方開始，學著好好照顧這個小生命。', s),
    choices: [
      { text: '先換好水，從第一件小事開始學著照顧牠', effect: () => {}, next: 'day2_morning' },
    ],
  },

  day2_morning: {
    id: 'day2_morning',
    day: 2,
    location: 'living_corner',
    music: 'warm',
    feeling: 'anxious',
    dogPose: 'corner',
    smellAdd: '雨停後的潮氣、新買的飼料',
    text: (s) => `請假在家的這個早晨。\n窗玻璃還凝著昨夜的霧，光透進來，很軟。\n\n${dogLabel(s)} 還在紙箱旁——\n但食盆、尿墊、新毯都已經就位。\n\n你換了更乾淨的水，也習慣了乾淨的手。\n水碗輕碰地板的聲音，讓牠耳朵動了一下。`,
    sub: '店員說的話還在耳邊：\n「照顧不是衝動一次，\n而是每天——準備好，再靠近。」',
    choices: [
      {
        text: '換好水，輕聲說早，不靠近',
        effect: (s) => {
          applyTrust(s, 8);
          applyBondProgress(s, 12);
        },
        next: 'day2_kitchen',
      },
      {
        text: '先不打擾，讓牠自己決定什麼時候動',
        effect: (s) => {
          applyTrust(s, 4);
          applyBondProgress(s, 8);
          setFeeling(s, 'shy');
        },
        next: 'day2_wait',
      },
      {
        text: '伸手想確認：你還在、我也還在',
        effect: (s) => {
          applyTrust(s, -5);
          applyBondProgress(s, 5);
          setFeeling(s, 'hurt');
        },
        next: 'day2_hurt',
      },
    ],
  },

  day2_wait: {
    id: 'day2_wait',
    day: 2,
    location: 'living_corner',
    music: 'calm',
    feeling: 'shy',
    dogPose: 'corner',
    smellAdd: '時間緩慢流動的氣味',
    text: (s) => `你等了很久。\n${dogLabel(s)} 終於離開紙箱邊緣半步——\n又停住，像在問：這樣可以嗎？`,
    choices: [
      {
        text: '點頭，仍保持距離，把早餐放在廚房門口',
        effect: (s) => {
          applyTrust(s, 10);
          applyBondProgress(s, 15);
          setFeeling(s, 'curious');
        },
        next: 'day2_kitchen',
      },
    ],
  },

  day2_hurt: {
    id: 'day2_hurt',
    day: 2,
    location: 'living_corner',
    music: 'tense',
    feeling: 'hurt',
    dogPose: 'corner',
    smell: '太快的靠近——像一陣不該有的風',
    text: (s) => `${dogLabel(s)} 縮回去，比昨夜更深。\n你收回手，心裡有點酸——\n不是牠不領情，是你還沒學會牠需要的節奏。`,
    sub: 'Day 2 還早。\n還來得及換一種方式。',
    choices: [
      {
        text: '深呼吸，先去準備早餐',
        effect: (s) => {
          applyTrust(s, 8);
          applyBondProgress(s, 12);
          setFeeling(s, 'anxious');
        },
        next: 'day2_kitchen',
      },
    ],
  },

  day2_kitchen: {
    id: 'day2_kitchen',
    day: 2,
    location: 'kitchen',
    music: 'warm',
    feeling: 'hungry',
    dogPose: 'kitchen',
    smellAdd: '溫熱的飼料、仍帶距離的空氣',
    text: (s) => `廚房。\n你把碗放在地上，${dogLabel(s)} 在門口張望——\n嗅到了，卻還不敢一個人走進去。`,
    choices: [
      {
        text: '退到客廳，留給牠空間',
        effect: (s) => {
          applyTrust(s, 12);
          applyBondProgress(s, 18);
          addMemory(s, 'day2_first_meal');
          setFeeling(s, 'curious');
        },
        next: 'day2_midday',
      },
      {
        text: '蹲在門邊，不越線，等',
        effect: (s) => {
          applyTrust(s, 10);
          applyBondProgress(s, 15);
          setFeeling(s, 'shy');
        },
        next: 'day2_midday',
      },
      {
        text: '「快吃啊。」把碗推近',
        effect: (s) => {
          applyTrust(s, -3);
          applyBondProgress(s, 6);
          setFeeling(s, 'anxious');
        },
        next: 'day2_midday',
      },
    ],
  },

  day2_midday: {
    id: 'day2_midday',
    day: 2,
    location: 'living_room',
    music: 'calm',
    feeling: 'curious',
    dogPose: 'home',
    smellAdd: ['洗過的碗', '午前陽光', '一點點飼料香'],
    text: (s) => `過了一會兒，你從客廳偷偷看過去。\n\n碗邊少了一圈——${dogLabel(s)} 真的吃過了。\n也許只幾口，也許還在試，\n但空氣裡多了一種很淡的「願意」。\n\n牠舔了舔嘴，又迅速回到能隨時撤退的位置。\n像在說：我看到了，我試了，我還在確認。`,
    sub: '你沒有過去誇。\n有些進步，需要在安靜裡自己長大。',
    choices: [
      { text: '午後，光線斜進客廳……', effect: () => {}, next: 'day2_afternoon' },
    ],
  },

  day2_afternoon: {
    id: 'day2_afternoon',
    day: 2,
    location: 'living_room',
    music: 'calm',
    feeling: 'alert',
    dogPose: 'window',
    smellAdd: ['樓上腳步', '電鈴餘響', '你的呼吸'],
    text: (s) => `Day 2，午後。\n樓上傳來腳步，${dogLabel(s)} 的耳朵豎起來——\n第一時間不是看門，而是看你。`,
    sub: '牠在學你的反應。\n這也算一種信任的起點。',
    choices: [
      {
        text: '用平常的語氣說：「沒事，我在。」',
        effect: (s) => {
          applyTrust(s, 10);
          applyBondProgress(s, 15);
          s.flags.day2CalmSound = true;
          setFeeling(s, 'curious');
        },
        next: 'day2_evening',
      },
      {
        text: '把牠抱到膝上，想讓牠別怕',
        effect: (s) => {
          applyTrust(s, -2);
          applyBondProgress(s, 8);
          setFeeling(s, 'anxious');
        },
        next: 'day2_evening',
      },
      {
        text: '一起安靜坐著，等聲音過去',
        effect: (s) => {
          applyTrust(s, 8);
          applyBondProgress(s, 18);
          s.flags.day2CalmSound = true;
          setFeeling(s, 'content');
        },
        next: 'day2_evening',
      },
    ],
  },

  day2_evening: {
    id: 'day2_evening',
    day: 2,
    location: 'living_corner',
    music: 'night',
    feeling: 'sleepy',
    dogPose: 'home',
    smellAdd: '第二天入夜、稍微熟悉的房間',
    text: (s) => `Day 2 入夜。\n${dogLabel(s)} 比昨夜靠近了半步——\n不算信任，但總算開始記得：這裡會有下一餐、下一個早晨。`,
    sub: '還很遠。\n但 Day 2 過去了。',
    choices: [
      { text: 'Day 3 的早晨……', effect: () => {}, next: 'day3_morning' },
    ],
  },

  day3_morning: {
    id: 'day3_morning',
    day: 3,
    location: 'living_corner',
    music: 'warm',
    feeling: 'anxious',
    dogPose: 'corner',
    smell: '鬧鐘、舊紙箱、仍陌生的房間',
    text: (s) => `Day 3，早晨。\n鬧鐘響得比平時急——今天得上班。\n\n${dogLabel(s)} 還蜷在紙箱旁，\n好像那裡才是安全邊界。\n\n你第一次要留牠獨自在這個家，\n說起來只是幾個小時，\n心裡卻像懸在半空。`,
    sub: '你還不知道怎麼愛。\n牠也還不知道，\n你會不會回來。',
    choices: [
      {
        text: '輕聲喚牠的名字，在遠處坐下，等',
        effect: (s) => {
          applyTrust(s, 12);
          applyBondProgress(s, 25);
          setFeeling(s, 'curious');
        },
        next: 'day3_curious',
      },
      {
        text: '心裡著急，提高音量：「過來！」',
        effect: (s) => {
          applyTrust(s, -15);
          s.flags.yelledOnce = true;
          setFeeling(s, 'hurt');
        },
        next: 'day3_hurt',
      },
      {
        text: '保持距離，用眼神和牠說：我在這',
        effect: (s) => {
          applyTrust(s, 10);
          applyBondProgress(s, 20);
          setFeeling(s, 'shy');
        },
        next: 'day3_curious',
      },
      {
        text: '看時鐘，先衝去廚房準備早餐',
        effect: (s) => {
          applyTrust(s, 8);
          applyBondProgress(s, 15);
          setFeeling(s, 'hungry');
        },
        next: 'day3_breakfast_rush',
      },
    ],
  },

  day3_hurt: {
    id: 'day3_hurt',
    day: 3,
    location: 'living_corner',
    music: 'tense',
    feeling: 'hurt',
    smell: '你的怒氣——太尖、太刺鼻',
    text: (s) => `${dogLabel(s)} 往角落縮得更深。\n你站在原地，忽然明白：愛不是把聲音放大。\n有些距離，是自己推開的。`,
    sub: '還來得及。\n信任碎了，也可以一片一片拼回來。',
    choices: [
      {
        text: '深呼吸，先去拿水盆和毛巾',
        effect: (s) => {
          applyTrust(s, 10);
          applyBondProgress(s, 20);
          setFeeling(s, 'anxious');
        },
        next: 'day3_breakfast_rush',
      },
    ],
  },

  day3_curious: {
    id: 'day3_curious',
    day: 3,
    location: 'living_room',
    music: 'warm',
    feeling: 'curious',
    smell: '洗過的地板、你的拖鞋、遠處的早餐',
    text: (s) => `${dogLabel(s)} 的耳朵豎了一下。\n鼻子朝你的方向動了動，又停住——\n像在丈量：可以再靠近一點嗎？\n\n時鐘在背後滴答，\n你還是得先餵飽牠，才能出門。`,
    choices: [
      {
        text: '伸出手，掌心朝上，不拉、不拽',
        effect: (s) => {
          applyTrust(s, 10);
          applyBondProgress(s, 20);
        },
        next: 'day3_breakfast_rush',
      },
    ],
  },

  day3_breakfast_rush: {
    id: 'day3_breakfast_rush',
    day: 3,
    location: 'kitchen',
    music: 'warm',
    feeling: 'hungry',
    dogPose: 'kitchen',
    smell: '溫熱的飼料、手機上的打卡提醒、來不及喝完的咖啡',
    text: (s) => `廚房裡手忙腳亂。\n你量飼料、換水、確認尿墊——\n每一項都想做好，\n時間卻像被人往後拖。\n\n${dogLabel(s)} 跟到門框就不走了，\n只敢遠遠嗅碗邊的氣味。\n你蹲下去，心裡發虛：\n「對不起，今天只能先這樣。」`,
    sub: '匆忙不是不愛，\n是第一次學著在「生活」和「責任」之間找平衡。',
    choices: [
      {
        text: '匆忙倒好飼料，來不及等牠吃完就出門',
        effect: (s) => {
          applyTrust(s, 4);
          applyBondProgress(s, 8);
          s.flags.day3RushedFeed = true;
        },
        next: 'day3_leave_home',
      },
      {
        text: '邊綁鞋帶邊推碗靠近：「乖乖的，我很快回來。」',
        effect: (s) => {
          applyTrust(s, 8);
          applyBondProgress(s, 12);
          setFeeling(s, 'shy');
        },
        next: 'day3_leave_home',
      },
      {
        text: '硬是多留五分鐘，看牠舔了一口才走',
        effect: (s) => {
          applyTrust(s, 12);
          applyBondProgress(s, 18);
          setFeeling(s, 'curious');
        },
        next: 'day3_leave_home',
      },
    ],
  },

  day3_leave_home: {
    id: 'day3_leave_home',
    day: 3,
    location: 'hallway',
    music: 'tense',
    feeling: 'anxious',
    dogPose: 'doorway-wait',
    smell: '關上的門、你的外套、牠留在裡面的呼吸',
    text: (s) => `玄關。\n你換好鞋，手放在門把上，\n回頭最後看一眼。\n\n${dogLabel(s)} 站在客廳邊緣，\n沒有追，也沒有叫——\n只是看著你，\n像把整個世界縮成這一道門。\n\n門咔噠一聲關上。\n安靜得過分。`,
    sub: '你以為只是去上班。\n對牠來說，\n可能是第一次被留在陌生的家裡。',
    choices: [
      { text: '搭車去公司，心卻一直留在身後那扇門……', effect: () => {}, next: 'day3_work_worry' },
    ],
  },

  day3_work_worry: {
    id: 'day3_work_worry',
    day: 3,
    location: 'office',
    music: 'tense',
    feeling: 'anxious',
    smell: '印表機、冷氣、螢幕藍光——都蓋不住你的擔心',
    text: (s) => `公司。\n會議簡報才翻到第三頁，\n你的腦子已經飛回家。\n\n牠會不會把沙發咬壞？\n會不會躲著發抖，\n以為你不要牠了？\n碗裡還有飼料嗎——\n還是早就餓著了？\n\n${dogLabel(s)} 的臉閃過眼前，\n你什麼也看不進去。`,
    sub: '不是你不夠專心，\n是愛還沒學會安靜地等。\n它會先變成慌。',
    choices: [
      {
        text: '傳訊息跟主管：「家裡有事，能提早離開嗎？」',
        effect: (s) => {
          applyBondProgress(s, 10);
          s.flags.day3AskedLeave = true;
          s.flags.day3LeftEarly = true;
        },
        next: 'day3_leave_early',
      },
      {
        text: '硬撐到十點，還是忍不住請假',
        effect: (s) => {
          applyBondProgress(s, 8);
          s.flags.day3LeftEarly = true;
        },
        next: 'day3_leave_early',
      },
      {
        text: '試著專心，但心越來越沉——還是決定先回家',
        effect: (s) => {
          applyBondProgress(s, 5);
          s.flags.day3LeftEarly = true;
        },
        next: 'day3_leave_early',
      },
    ],
  },

  day3_leave_early: {
    id: 'day3_leave_early',
    day: 3,
    location: 'street_sunset',
    music: 'hopeful',
    feeling: 'anxious',
    smell: '提早的午後、捷運人潮、你愈來愈急的腳步',
    text: (s) => {
      const asked = s.flags.day3AskedLeave;
      const lead = asked
        ? '主管回得很快：「好，先顧家。」\n你道了聲謝，心裡還是虛虛的——\n但腳步已經往車站跑。'
        : '你沒等多餘的解釋，\n收好東西就離開。\n電梯往下，\n胃裡那團擔心卻越來越大。';
      return `${lead}\n\n回家路上，\n你數著站名，\n數著如果 ${dogLabel(s)} 餓了多久、\n怕了多久。`;
    },
    sub: '提早下班不是偷懶，\n是你終於承認：\n有些等待，你沒辦法假裝沒看見。',
    choices: [
      { text: '轉角看見自家那棟樓……', effect: () => {}, next: 'day3_homecoming' },
    ],
  },

  day3_homecoming: {
    id: 'day3_homecoming',
    day: 3,
    location: 'doorway',
    music: 'warm',
    feeling: 'shy',
    dogPose: 'doorway-lie',
    smell: '開門的氣流、熟悉的飼料味、一點點安心',
    text: (s) => `鑰匙還在鎖孔裡，\n你就聽見裡面有動靜。\n\n門一開——\n${dogLabel(s)} 趴在玄關地磚上，\n耳朵朝門的方向豎著，\n一聽見你的腳步，整個身子都彈起來。\n\n沒有咬壞什麼，\n也沒有亂翻。\n只是等。\n等得那麼久，\n久到你心口一酸。`,
    sub: '【Memory】門口的等待',
    onEnter: (s) => { addMemory(s, 'door_wait'); s.flags.day3Reunion = true; },
    choices: [
      {
        text: '蹲下來，什麼都不說，先讓牠聞聞你',
        effect: (s) => {
          applyTrust(s, 15);
          applyBondProgress(s, 30);
          setFeeling(s, 'attached');
        },
        next: 'day3_afternoon',
      },
      {
        text: '輕聲說：「對不起，讓你等了。」',
        effect: (s) => {
          applyTrust(s, 12);
          applyBondProgress(s, 25);
          setFeeling(s, 'content');
        },
        next: 'day3_afternoon',
      },
      {
        text: '看見家裡還算整齊，鬆了口氣，把牠抱緊一點',
        effect: (s) => {
          applyTrust(s, 10);
          applyBondProgress(s, 22);
          setFeeling(s, 'curious');
        },
        next: 'day3_afternoon',
      },
    ],
  },

  day3_afternoon: {
    id: 'day3_afternoon',
    day: 3,
    location: 'living_room',
    music: 'calm',
    feeling: 'content',
    dogPose: 'home',
    smell: '提早回家的午後、電風扇、漸漸熟悉的地磚',
    text: (s) => `提早回來的午後，\n時間忽然變得很長。\n\n你補了一餐，換了水，\n${dogLabel(s)} 這次跟到碗邊，\n舔得比早晨安心。\n\n牠開始記得：\n哪裡是門、哪裡是窩、\n哪裡是你常坐的位置——\n還有，門開的時候，\n你會走進來。`,
    sub: '這一天，\n你學會了：\n愛有時候是提早回家。',
    choices: [
      { text: '趁著天還亮，帶牠去尿墊旁練習一下', effect: () => {}, next: 'day3_potty_intro' },
      { text: '天色漸漸暗下來……', effect: (s) => { setFeeling(s, 'sleepy'); }, next: 'day3_night' },
    ],
  },

  day3_potty_intro: {
    id: 'day3_potty_intro',
    day: 3,
    location: 'living_room',
    music: 'warm',
    feeling: 'curious',
    dogPose: 'potty',
    smell: '尿墊、皂香、你的耐心',
    text: () => '如廁這件事，很少一次就對。\n\n今天不用趕，\n你可以在對的瞬間，輕輕引導——\n像說一個只有你們懂的暗號。\n不責怪，不著急，\n只是反覆、溫柔地，把「對的地方」指給牠看。',
    sub: '這不是訓練成績，是信任練習。\n你們都在學：怎麼不傷害彼此的情緒。',
    minigame: 'potty',
    next: 'day3_night',
  },

  day3_night: {
    id: 'day3_night',
    day: 3,
    location: 'bathroom_night',
    music: 'night',
    feeling: 'anxious',
    dogPose: 'night-accident',
    smell: '意外、你的疲憊、牠的驚慌',
    text: (s) => `深夜，你從夢裡驚醒。\n白天那份慌還沒散盡，\n客廳又傳來一點氣味——\n${dogLabel(s)} 留了不該留的「禮物」。\n\n心往下沉。\n你知道，這一夜會記很久。`,
    sub: '怎麼做，比做錯了什麼更重要。',
    choices: [
      {
        text: '不罵。清理完，陪牠坐在尿墊旁',
        effect: (s) => {
          applyTrust(s, 18);
          applyBondProgress(s, 35);
          s.flags.pottyNightKind = true;
          addMemory(s, 'potty_night');
          addMemory(s, 'knee');
          setFeeling(s, 'content');
        },
        next: 'day3_night_after',
      },
      {
        text: '嘆氣，默默清理，回房關上門',
        effect: (s) => {
          applyTrust(s, -8);
          applyBondProgress(s, 5);
          setFeeling(s, 'hurt');
        },
        next: 'day4_repair',
      },
      {
        text: '吼了出來，把牠關進浴室',
        effect: (s) => {
          applyTrust(s, -20);
          s.flags.yelledOnce = true;
          setFeeling(s, 'hurt');
        },
        next: 'day4_repair',
      },
    ],
  },

  day3_night_after: {
    id: 'day3_night_after',
    day: 3,
    location: 'bedroom_night',
    music: 'tender',
    feeling: 'content',
    dogPose: 'knee',
    smell: '清潔劑散去後，只剩你的體溫',
    text: (s) => `${dogLabel(s)} 把頭輕輕放在你膝上。\n沒有聲音，沒有撒嬌——\n只是靠著，像終於確認：你不會在這時候離開。`,
    sub: '【Memory】尿墊之夜　·　【Moment】靠膝',
    choices: [
      { text: '摸一摸牠的頭，關燈', effect: () => {}, next: 'day4_off' },
    ],
  },

  day4_repair: {
    id: 'day4_repair',
    day: 4,
    location: 'hallway',
    music: 'tense',
    feeling: 'hurt',
    dogPose: 'repair',
    smell: '隔夜的沉默、未散的疏離',
    text: (s) => `Day 4 · 週六，早晨。\n${dogLabel(s)} 在玄關張望，腳步往前半步，又退回去。\n${dogPronoun(s)}還在這裡——只是不確定，你還在不在。\n\n還好，今天是週末，不用上班。`,
    sub: '後果不是懲罰，是提醒：你還來得及補。',
    choices: [
      {
        text: '蹲下，說對不起，拿出牠最愛的玩具',
        effect: (s) => {
          applyTrust(s, 15);
          applyBondProgress(s, 25);
          setFeeling(s, 'curious');
        },
        next: 'day4_off',
      },
      {
        text: '照常餵食，不說話，但也不離開',
        effect: (s) => {
          applyTrust(s, 5);
          applyBondProgress(s, 10);
          setFeeling(s, 'anxious');
        },
        next: 'day4_off',
      },
    ],
  },

  day4_off: {
    id: 'day4_off',
    day: 4,
    location: 'living_sunday',
    music: 'calm',
    feeling: 'content',
    dogPose: 'home',
    smell: '週六早晨、沒有鬧鐘、慢慢熱起來的陽光',
    text: (s) => `Day 4 · 週六。\n\n鬧鐘沒響——\n今天是休息日，不用上班。\n\n${dogLabel(s)} 在客廳輕輕走動，\n像確認這個沒有「關門聲」的早晨是不是真的。\n\n你滑開手機，\n看見預約的寵物醫院提醒：\n「幼犬健康檢查 · 疫苗諮詢」。\n\n該出門了。`,
    sub: '週末不是偷懶，\n是把該負的責任，\n也排進生活裡。',
    choices: [
      {
        text: '幫牠系好牽繩，出門往寵物醫院',
        effect: (s) => {
          applyBondProgress(s, 8);
          setFeeling(s, 'anxious');
        },
        next: 'day4_vet_go',
      },
      {
        text: '先餵飽、安撫一下，再慢慢出門',
        effect: (s) => {
          applyTrust(s, 6);
          applyBondProgress(s, 10);
          setFeeling(s, 'curious');
        },
        next: 'day4_vet_go',
      },
    ],
  },

  day4_vet_go: {
    id: 'day4_vet_go',
    day: 4,
    location: 'street',
    music: 'warm',
    feeling: 'anxious',
    dogPose: 'vet-walk',
    smell: '週末的街風、車聲比平日少、你的心跳',
    text: (s) => `週六的街上，人比平日少。\n\n${dogLabel(s)} 走在你腳邊，\n每一步都小、都慢——\n外面的世界對 ${dogPronoun(s)} 還太亮、太響。\n\n你彎腰，把 ${dogPronoun(s)} 抱起來。\n\n${dogPronoun(s)} 把鼻子埋進你的外套——\n像在這陌生的街頭，\n先找一個還認得的味道。\n\n「沒關係，\n今天只是去讓醫生看看。」`,
    sub: '你發現自己說話的語氣，\n比對主管請假時還溫柔。',
    choices: [
      { text: '推開寵物醫院的門……', effect: () => {}, next: 'day4_vet_reception' },
    ],
  },

  day4_vet_reception: {
    id: 'day4_vet_reception',
    day: 4,
    location: 'pet_vet',
    music: 'calm',
    feeling: 'anxious',
    dogPose: 'vet-carry',
    sceneArt: 'vet-reception',
    sceneArtAlt: '櫃檯人員遞上初診表，請你填寫基本資料',
    smell: '消毒水、印表機、櫃檯後方零食罐',
    text: (s) => `櫃檯遞上初診表，\n紙張還帶著印表機的溫度。\n\n${dogLabel(s)} 在你懷裡一僵，\n你把 ${dogPronoun(s)} 抱得更穩一點。\n\n櫃檯的人抬頭，語氣很平常：\n「第一次來？\n先填這份——\n名字、大概帶回家幾天、\n最近吃睡有沒有異常。」\n\n你接過筆，\n一筆一畫寫下去。\n滿屋子都是陌生的氣味——\n消毒水、別的動物的味道、你從沒聞過的零食罐。\n\n${dogLabel(s)} 的鼻子在你頸邊嗅了又嗅，\n像在這陌生的環境裡，\n尋找唯一熟悉的味道。`,
    sub: '你發現自己寫字比平常慢——\n怕填錯，也怕漏掉什麼該說的；\n而懷裡那個小鼻子還在聞，\n好像只要味道還在，這裡就不完全陌生。',
    choices: [
      {
        text: '照實填：剛帶回家幾天，還在適應、偶爾會叫',
        effect: (s) => {
          applyTrust(s, 4);
          s.flags.vetFormDetail = 'honest';
        },
        next: 'day4_vet_intake',
      },
      {
        text: '簡短填完重點，先輕聲安撫懷裡的牠',
        effect: (s) => {
          applyTrust(s, 6);
          s.flags.vetFormDetail = 'brief';
        },
        next: 'day4_vet_intake',
      },
    ],
  },

  day4_vet_intake: {
    id: 'day4_vet_intake',
    day: 4,
    location: 'pet_vet',
    music: 'calm',
    feeling: 'shy',
    dogPose: 'vet-carry',
    hideDog: true,
    sceneArt: 'vet-doctor',
    sceneArtAlt: '醫師翻閱初診表，詢問近況',
    smell: '棉花、聽診器、一點點寵物零食味',
    text: (s) => {
      const formNote = s.flags.vetFormDetail === 'honest'
        ? '醫師看了表上的幾行字，點點頭：\n「有寫到還在適應，這很好。」\n\n'
        : '醫師看了表，語氣仍穩：\n「沒關係，我們邊問邊補。」\n\n';
      return `診間門關上，外面安靜了一點。\n\n醫師依表單詢問：\n吃、睡、排便，\n有沒有讓你特別擔心的事。\n\n${formNote}醫師戴好聽診器，先看向你：\n「${dogLabel(s)} 最近食慾怎麼樣？\n睡覺會不會驚醒？\n排便正常嗎？\n有沒有特別擔心的地方？」\n\n${dogLabel(s)} 把臉埋進你袖口——\n找到了。\n在這滿是棉花和聽診器的診間裡，\n只有這道味道，${dogPronoun(s)} 還認得。`;
    },
    sub: '你發現，被認真問這些事，\n比想像中更需要鼓起勇氣。',
    choices: [
      {
        text: '坦白說：會擔心我出門，半夜有時還會叫',
        effect: (s) => {
          applyTrust(s, 8);
          applyBondProgress(s, 10);
          s.flags.vetIntakeTier = 'open';
          setFeeling(s, 'anxious');
        },
        next: 'day4_vet',
      },
      {
        text: '主要想了解疫苗，其他還在觀察',
        effect: (s) => {
          applyTrust(s, 5);
          applyBondProgress(s, 8);
          s.flags.vetIntakeTier = 'focus';
          setFeeling(s, 'curious');
        },
        next: 'day4_vet',
      },
      {
        text: '請醫生依表單和檢查再判斷，我配合回答',
        effect: (s) => {
          applyTrust(s, 6);
          applyBondProgress(s, 12);
          s.flags.vetIntakeTier = 'trust';
          setFeeling(s, 'content');
        },
        next: 'day4_vet',
      },
    ],
  },

  day4_vet: {
    id: 'day4_vet',
    day: 4,
    location: 'pet_vet',
    music: 'calm',
    feeling: 'anxious',
    dogPose: 'vet-carry',
    hideDog: true,
    sceneArt: 'vet-doctor',
    sceneArtAlt: '獸醫戴著聽診器，開始健康檢查',
    smell: '消毒水、棉花、一點點寵物零食味',
    text: (s) => {
      const lead = s.flags.vetIntakeTier === 'open'
        ? '醫師應了一聲：「分離焦慮很常見，我們慢慢來。」\n\n'
        : s.flags.vetIntakeTier === 'focus'
          ? '醫師說：「疫苗會排，其他我們邊觀察邊調整。」\n\n'
          : '醫師點頭：「好，那我們一項一項看。」\n\n';
      return `${lead}量體重、聽心肺——\n聽診器貼上去時，${dogLabel(s)} 的身子還緊，\n但你在，${dogPronoun(s)} 沒有叫。\n\n醫師翻閱初診表，又問了幾題日常狀況：\n食慾、睡眠、排便、疫苗紀錄與種類……\n你照實回答。\n\n${dogLabel(s)} 的耳朵動了一下，\n鼻子又埋進你的袖口——\n像剛才在櫃檯前那樣，\n在陌生裡，只認這一道熟悉的氣味。`;
    },
    sub: '問診一題一題來——\n照著這幾天的真實狀況回答就好。',
    minigame: 'vet',
    next: 'day4_vet_bill',
  },

  day4_vet_bill: {
    id: 'day4_vet_bill',
    day: 4,
    location: 'pet_vet',
    music: 'calm',
    feeling: 'curious',
    dogPose: 'vet-carry',
    hideDog: true,
    sceneArt: 'vet-bill',
    sceneArtAlt: '櫃台人員協助結帳與說明費用',
    smell: '印表機、紙張、剛才的檢查表',
    text: (s) => {
      const tier = s.flags.vetTier;
      const extra = tier === 'perfect' || tier === 'good'
        ? '醫師補充：「下一劑記得準時回來，\n時間表我寫在單子上了。」\n\n'
        : '櫃台人員幫你標出重點：「這幾項是幼犬一定要的，\n其他可以下次再補。」\n\n';
      return `結帳。\n\n${extra}櫃台螢幕上的數字，\n讓你愣了一下——\n\n健康檢查、疫苗、寄生蟲篩檢……\n加起來，比你想像中貴不少。\n\n你看了 ${dogLabel(s)} 一眼。\n${dogPronoun(s)} 還窩在你臂彎，\n不知道這串數字代表什麼，\n只知道你在這裡。`;
    },
    sub: '心裡驚了一下，\n但你也明白：\n這不是衝動的價格，\n是接下來好幾年的責任。',
    choices: [
      {
        text: '深吸一口氣，刷卡：這也是照顧牠的一部分',
        effect: (s) => {
          applyTrust(s, 10);
          applyBondProgress(s, 18);
          s.flags.vetBillAcknowledged = true;
          addMemory(s, 'vet_visit');
          setFeeling(s, 'content');
        },
        next: 'day4_evening',
      },
      {
        text: '先問清楚每一項，再付款——該花的不能省',
        effect: (s) => {
          applyTrust(s, 8);
          applyBondProgress(s, 15);
          s.flags.vetBillAcknowledged = true;
          addMemory(s, 'vet_visit');
          setFeeling(s, 'curious');
        },
        next: 'day4_evening',
      },
    ],
  },

  day4_evening: {
    id: 'day4_evening',
    day: 4,
    location: 'living_corner',
    music: 'night',
    feeling: 'sleepy',
    dogPose: 'home',
    smellAdd: ['週六入夜', '檢查單上的字', '慢慢變熟悉的你'],
    text: (s) => `Day 4 · 週六入夜。\n\n你把檢查單折好，夾在記事本裡。\n下一針的日期，\n用螢幕提醒設好了。\n\n${dogLabel(s)} 在毯子上轉了兩圈，\n選了一個能同時看見你和門的位置睡下。\n\n今天沒有上班，\n但好像比上班還累——\n也許是因為，\n你第一次替另一個生命，\n付了一筆「認真」的帳。`,
    sub: '週六過去了。\n明天還是週日，\n還不用出門。',
    choices: [
      { text: 'Day 5 · 週日，早晨的陽光……', effect: () => {}, next: 'day5_sunday' },
    ],
  },

  day5_sunday: {
    id: 'day5_sunday',
    day: 5,
    location: 'living_sunday',
    music: 'calm',
    feeling: 'content',
    dogPose: 'sunday-wake',
    smell: '週日早晨、咖啡、沒有鬧鐘',
    text: (s) => `Day 5 · 週日。\n\n還是休息日，不用上班。\n\n${dogLabel(s)} 在你腳邊醒來，\n比昨天多靠近了一點點——\n也許是昨天在醫院，\n整路都是你的懷抱。\n\n窗外很安靜。\n你忽然想到：\n${dogPronoun(s)} 還不認識這個家的每一個角落，\n每一種屬於你的氣味。`,
    sub: (s) => `外面可以晚一點再去。\n先把「家」變成 ${dogPronoun(s)} 也懂的地方。`,
    choices: [
      {
        text: '把牠抱起來，從客廳開始慢慢認',
        effect: (s) => {
          applyTrust(s, 8);
          applyBondProgress(s, 12);
          setFeeling(s, 'shy');
        },
        next: 'day5_home_intro',
      },
      {
        text: '先坐在地板，讓牠自己靠過來再抱',
        effect: (s) => {
          applyTrust(s, 12);
          applyBondProgress(s, 15);
          setFeeling(s, 'curious');
        },
        next: 'day5_home_intro',
      },
    ],
  },

  day5_home_intro: {
    id: 'day5_home_intro',
    day: 5,
    location: 'living_room',
    music: 'warm',
    feeling: 'shy',
    dogPose: 'held',
    smell: '你的外套、洗過的地板、熟悉的沙發',
    text: (s) => `你把 ${dogLabel(s)} 抱在懷裡。\n\n${dogPronoun(s)} 的身子還有點僵，\n但沒有掙開——\n鼻子在你頸邊輕輕嗅，\n像在確認：這個味道，是可以信任的。\n\n「我帶你認一認。」\n你小聲說，\n「這裡以後都是你的。」`,
    sub: (s) => `房間不大，\n但對 ${dogPronoun(s)} 來說，\n每一扇門後都是新世界。`,
    minigame: 'home',
    next: 'day5_home_after',
  },

  day5_home_after: {
    id: 'day5_home_after',
    day: 5,
    location: 'living_warm',
    music: 'warm',
    feeling: 'content',
    dogPose: 'home-settle',
    smellAdd: ['你的床單', '食盆的位置', '陽台的風'],
    text: (s) => {
      const tier = s.flags.homeExploreTier;
      if (tier === 'perfect' || tier === 'good') {
        return `繞完一圈，${dogLabel(s)} 在你懷裡鬆下來。\n\n${dogPronoun(s)} 記住了食盆在哪、\n你常坐的沙發在哪、\n連陽台的風從哪個縫隙吹進來。\n\n你把 ${dogPronoun(s)} 放在軟墊上，\n${dogPronoun(s)} 沒有立刻躲回紙箱——\n而是把下巴擱在你膝上，\n像說：這裡，好像真的可以。`;
      }
      if (tier === 'partial') {
        return `有些角落，${dogLabel(s)} 還不敢久留。\n\n但 ${dogPronoun(s)} 記住了食盆，\n也記住了你的床單味——\n那代表你會在這裡睡。\n\n信任不是一次認完全部，\n是一點一點，\n把「陌生」換成「熟悉」。`;
      }
      return `${dogLabel(s)} 還有些緊繃，\n只願意記住一兩個角落。\n\n你沒有急，\n只是把 ${dogPronoun(s)} 抱緊一點，\n讓 ${dogPronoun(s)} 聽見你的心跳。\n\n今天認得的雖然少，\n但 ${dogPronoun(s)} 願意靠著你——\n這本身就算進步。`;
    },
    sub: (s) => {
      const tier = s.flags.homeExploreTier;
      if (tier === 'perfect' || tier === 'good') return '【Memory】家的氣味地圖';
      return '家還在慢慢變成「你們的」。';
    },
    onEnter: (s) => {
      if (s.flags.homeExploreTier === 'perfect' || s.flags.homeExploreTier === 'good') {
        addMemory(s, 'home_scent');
      }
      if (s.bondProgress >= 60 || s.trust >= 42) {
        if (s.bondLevel < 2) { s.bondLevel = 2; s.bondProgress = Math.max(s.bondProgress, 100); }
      }
    },
    choices: [
      { text: '週日的午後，就這樣靜靜度過……', effect: (s) => { setFeeling(s, 'content'); }, next: 'day5_evening' },
    ],
  },

  day5_evening: {
    id: 'day5_evening',
    day: 5,
    location: 'living_corner',
    music: 'night',
    feeling: 'attached',
    dogPose: 'knee',
    smellAdd: ['週日入夜', '熟悉的房間', '你的體溫'],
    text: (s) => `Day 5 · 週日入夜。\n\n你關上筆電，把最後一盞小燈留著。\n\n${dogLabel(s)} 不再只睡紙箱邊——\n今天 ${dogPronoun(s)} 選了离你更近的位置，\n近到一伸手，\n就能摸到 ${dogPronoun(s)} 的背。\n\n週末兩天，沒有打卡、沒有會議，\n但你覺得比任何加班日都充實。\n\n你輕聲說：「明天見。」\n這次，${dogPronoun(s)} 沒有再驚醒。`,
    sub: '信任不是突然來的，\n是週六的醫院、\n週日的懷抱，\n一點一點堆起來的。',
    choices: [
      { text: 'Day 6 的早晨……', effect: () => {}, next: 'day6_morning' },
    ],
  },

  day6_morning: {
    id: 'day6_morning',
    day: 6,
    location: 'kitchen_morning',
    music: 'calm',
    feeling: 'content',
    dogPose: 'kitchen',
    smell: '星期一咖啡、洗淨的碗、要出門的緊',
    text: (s) => `Day 6 · 週一，早晨。\n\n鬧鐘響了——\n八點前要出門，又得上班。\n\n${dogLabel(s)} 卻用鼻子拱醒你，\n比鈴聲還早一秒。\n\n週末那股慢下來的鬆，\n在新一週的門口收斂了。\n\n你還是忍不住多摸了一下 ${dogPronoun(s)} 的頭，\n才關上門。`,
    choices: [
      { text: '關上門，搭車去公司……', effect: (s) => { applyBondProgress(s, 8); }, next: 'day6_check' },
    ],
  },

  day6_check: {
    id: 'day6_check',
    day: 6,
    location: 'living_room',
    music: 'calm',
    feeling: 'content',
    dogPose: 'window',
    smell: '傍晚的塵光、外頭的雲、回家的鑰匙',
    text: (s) => `Day 6 · 週一，傍晚。\n\n你五點離開公司——\n準時下班，但外頭的天色已暗了一半。\n\n鑰匙還帶著外面的冷，\n門一開，熟悉的氣味撲過來。\n\n${dogLabel(s)} 在玄關邊抬頭看你，\n尾巴輕輕動了一下。\n\n雲層壓下來，\n像有人把房間的聲音關小。`,
    sub: '週一的傍晚，\n適合等。\n等雲、等風、等下一個你們還不知道會發生什麼的瞬間。',
    onEnter: (s) => {
      s._thunderEligible = s.flags.pottyNightKind || s.flags.day2CalmSound || s.trust >= 40;
    },
    choices: [
      {
        text: '……',
        effect: () => {},
        next: (s) => (s._thunderEligible ? 'day6_thunder' : 'day6_quiet'),
      },
    ],
  },

  day6_quiet: {
    id: 'day6_quiet',
    day: 6,
    location: 'living_room',
    music: 'calm',
    feeling: 'content',
    dogPose: 'home',
    smell: '晒過的毯子、你的書、時間本身',
    text: (s) => `沒有雷。\n${dogLabel(s)} 在沙發腳邊打盹，呼吸一起一伏。\n普通的一天——後來你才知道，這種普通有多難得。`,
    choices: [
      { text: 'Day 7……', effect: (s) => { applyBondProgress(s, 10); }, next: 'day7_morning' },
    ],
  },

  day6_thunder: {
    id: 'day6_thunder',
    day: 6,
    location: 'living_storm',
    music: 'storm',
    feeling: 'alert',
    dogPose: 'thunder',
    minigame: 'thunder',
    smell: '臭氧、雨、鐵鏽、發抖的毛',
    text: (s) => `雷聲滚過來。\n${dogLabel(s)} 整個身子縮成一團，鑽進桌底——\n好像世界突然只剩下「怕」這一件事。`,
    sub: '遠方又一声雷——\n你靠近桌底，\n先聽見牠怕，再讓牠慢慢不怕。',
    choices: [
      {
        text: '開小夜燈，坐在地上，不強拉、不責怪',
        effect: (s) => {
          applyTrust(s, 15);
          applyBondProgress(s, 20);
          s.flags.afraidOfThunder = true;
          s.flags.thunderHandled = true;
          addMemory(s, 'thunder');
          setFeeling(s, 'content');
        },
        next: 'day6_thunder_after',
      },
      {
        text: '「沒什麼好怕的！」把牠從桌下拉出來',
        effect: (s) => {
          applyTrust(s, -10);
          s.flags.afraidOfThunder = true;
          setFeeling(s, 'hurt');
        },
        next: 'day7_morning',
      },
    ],
  },

  day6_thunder_after: {
    id: 'day6_thunder_after',
    day: 6,
    location: 'window_rain',
    music: 'tender',
    feeling: 'content',
    dogPose: 'knee',
    smell: '雨停後的泥土、你的膝蓋、安靜下來的心跳',
    text: (s) => {
      const tier = s.flags.thunderComfortTier;
      const name = dogLabel(s);
      if (tier === 'perfect') {
        return `雨停了。\n${name} 從桌底慢慢挪出來，整個身子貼在你膝邊。\n剛才每一聲雷，你都選對了方式——\n牠還是會怕雷，但今晚，已經不怕你了。`;
      }
      if (tier === 'good') {
        return `雨停了。\n${name} 從桌底挪出來，停在你膝邊。\n怕雷的聲音還在記憶裡，\n但顫抖停了——\n因為你在。`;
      }
      if (tier === 'miss' || tier === 'partial') {
        return `雨停了。\n${name} 還在桌底多待了一會，才探出頭。\n有些時刻你選錯了，但最後仍留下來。\n怕雷這件事，會記很久——\n包括，誰在旁邊。`;
      }
      return `雨停了。\n${name} 從桌底慢慢挪出來，停在你膝邊。\n怕雷這件事，會記很久——包括，誰在旁邊。`;
    },
    choices: [
      { text: 'Day 7……', effect: () => {}, next: 'day7_morning' },
    ],
  },

  day7_morning: {
    id: 'day7_morning',
    day: 7,
    location: 'kitchen_morning',
    music: 'warm',
    feeling: 'content',
    dogPose: 'kitchen',
    smell: '第七個早晨——像本來就該如此',
    text: (s) => `Day 7 · 週二，早晨。\n\n又得上班——\n八點前出門，已是習慣。\n\n${dogLabel(s)} 把食盆推到你腳邊，抬頭看你。\n不用語言，你也讀懂：該吃飯了，該出門了。`,
    choices: [
      { text: '傍晚，你比平常更晚回家……', effect: (s) => { applyBondProgress(s, 5); }, next: 'day7_evening' },
    ],
  },

  day7_evening: {
    id: 'day7_evening',
    day: 7,
    location: 'entrance_night',
    music: 'night',
    feeling: 'anxious',
    dogPose: 'doorway-wait',
    smell: '疲憊、未接的電話、門裡熟悉的氣味',
    text: () => '傍晚，你在門口站了一會。\n今天加班到比平常晚——\n鑰匙還在口袋裡，手卻抬不起來。\n今天很難——難到不想讓誰看見。',
    onEnter: (s) => { setFeeling(s, 'attached'); },
    choices: [
      {
        text: '進門，什麼也不說，直接坐在地板上',
        effect: (s) => {
          applyTrust(s, 10);
          applyBondProgress(s, 25);
          addMemory(s, 'sad_day');
        },
        next: 'day7_moment',
      },
    ],
  },

  day7_moment: {
    id: 'day7_moment',
    day: 7,
    location: 'living_warm',
    music: 'tender',
    feeling: 'attached',
    dogPose: 'sad-day',
    smell: '眼淚的鹹、暖光、毛髮的溫度',
    text: (s) => `${dogLabel(s)} 沒有舔你滿臉，也沒有吵。\n只是走過來，把頭靠在你膝上——\n和 Day 3 那夜一樣輕，一樣安靜。`,
    sub: '【Moment】你難過的那一天',
    choices: [
      { text: '……', effect: () => {}, next: 'epilogue' },
    ],
  },

  epilogue: {
    id: 'epilogue',
    day: 7,
    location: 'epilogue_home',
    music: 'tender',
    feeling: 'content',
    dogPose: 'home',
    smell: '一週後的家——開始像「我們的」',
    text: (s) => `七天。\n${dogLabel(s)} 還是會闖禍，你也還是會累。\n但你們慢慢學會一件事：\n愛不是一次做對，是一次次，選擇留下來。`,
    sub: '羈絆才剛開始寫。',
    isEpilogue: true,
  },
};

if (typeof module !== 'undefined') module.exports = { SCENES };
