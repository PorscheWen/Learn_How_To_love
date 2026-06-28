const TEXT_SPEED_KEY = 'lhtl_text_speed_v1';

/** 文字速度：基礎間隔 ms；句讀額外停頓 */
const TEXT_SPEED_PRESETS = {
  slow:    { id: 'slow',    label: '緩',   base: 82, pauseMajor: 680, pauseMinor: 300, subMult: 1.28 },
  gentle:  { id: 'gentle',  label: '舒',   base: 52, pauseMajor: 440, pauseMinor: 200, subMult: 1.15 },
  normal:  { id: 'normal',  label: '常',   base: 34, pauseMajor: 280, pauseMinor: 120, subMult: 1.05 },
  fast:    { id: 'fast',    label: '快',   base: 20, pauseMajor: 120, pauseMinor: 50,  subMult: 0.92 },
  instant: { id: 'instant', label: '即時', base: 0,  pauseMajor: 0,   pauseMinor: 0,   subMult: 1, instant: true },
};

const DEFAULT_TEXT_SPEED = 'slow';

function getTextSpeedId() {
  const saved = localStorage.getItem(TEXT_SPEED_KEY);
  return TEXT_SPEED_PRESETS[saved] ? saved : DEFAULT_TEXT_SPEED;
}

function setTextSpeedId(id) {
  if (TEXT_SPEED_PRESETS[id]) {
    localStorage.setItem(TEXT_SPEED_KEY, id);
  }
}

function getTextSpeedPreset() {
  return TEXT_SPEED_PRESETS[getTextSpeedId()];
}

function delayForChar(ch, preset, multiplier = 1) {
  if (preset.instant) return 0;
  let d = preset.base * multiplier;
  if ('。！？…—'.includes(ch)) d += preset.pauseMajor;
  else if ('，、；：'.includes(ch)) d += preset.pauseMinor;
  else if (ch === '\n' || ch === ' ') d += preset.pauseMinor * 0.5;
  return d;
}

/** Remove period after Day N; wrap Day N in markup for bold styling */
function formatDayLabels(plain) {
  const stripped = String(plain ?? '').replace(/Day\s+(\d+)[。．]/g, 'Day $1');
  return stripped.replace(/Day\s+(\d+)/g, '<strong class="day-tag">Day $1</strong>');
}

if (typeof module !== 'undefined') {
  module.exports = {
    TEXT_SPEED_KEY, TEXT_SPEED_PRESETS, DEFAULT_TEXT_SPEED,
    getTextSpeedId, setTextSpeedId, getTextSpeedPreset, delayForChar, formatDayLabels,
  };
}
