/** Visual scene locations — CSS class + label + default music hint */
const LOCATIONS = {
  prologue_rain:   { label: '雨天 · 紙箱旁',      icon: '🌧️' },
  living_corner:   { label: '客廳 · 紙箱角落',    icon: '🏠' },
  living_room:     { label: '客廳',              icon: '🛋️' },
  kitchen:         { label: '廚房',              icon: '🍳' },
  balcony:         { label: '陽台',              icon: '☀️' },
  bathroom_night:  { label: '浴室 · 第一夜',        icon: '🛁' },
  bedroom_night:   { label: '臥室 · 夜裡',        icon: '🛏️' },
  pet_shop:        { label: '寵物店',              icon: '🐾' },
  pet_vet:         { label: '寵物醫院',            icon: '🏥' },
  hallway:         { label: '玄關',              icon: '🚪' },
  kitchen_morning: { label: '廚房 · 早晨',        icon: '☕' },
  doorway:         { label: '門口',              icon: '👟' },
  stairwell:       { label: '樓梯間',            icon: '🪜' },
  street:          { label: '街道',              icon: '🌳' },
  park:            { label: '小公園',            icon: '🌲' },
  office:          { label: '公司 · 工位',        icon: '💼' },
  street_sunset:   { label: '回家路 · 夕陽',      icon: '🌅' },
  living_sunday:   { label: '客廳 · 週末午後',    icon: '📖' },
  living_storm:    { label: '客廳 · 雷雨',        icon: '⛈️' },
  window_rain:     { label: '窗邊 · 雨後',        icon: '🌦️' },
  entrance_night:  { label: '門口 · 傍晚',        icon: '🌆' },
  living_warm:     { label: '客廳 · 暖光',        icon: '💡' },
  epilogue_home:   { label: '我們的家',           icon: '🏡' },
};

if (typeof module !== 'undefined') module.exports = { LOCATIONS };
