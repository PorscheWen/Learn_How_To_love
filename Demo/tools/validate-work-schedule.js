/**
 * 審查 Demo 場景文案是否與主人班表衝突
 * 週一～五 08:00–17:00 上班；週六日放假；請假需明示
 */
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const scenesSrc = fs.readFileSync(path.join(root, 'js/scenes.js'), 'utf8');
const systemsSrc = fs.readFileSync(path.join(root, 'js/systems.js'), 'utf8');

eval(systemsSrc.replace(/^const FLOW_VERSION/m, 'const FLOW_VERSION'));
eval(scenesSrc.replace(/^const SCENES\s*=/m, 'global.SCENES ='));

const WORKDAY_DAYS = [3, 6, 7];
const OFF_DAYS = [4, 5];
const LEAVE_DAYS = [2];

const AT_HOME_MIDDDAY_PATTERNS = [
  /泡了杯茶/,
  /書頁翻得很慢/,
  /鬧鐘還沒響/,
  /週末的午後/,
  /週末吐司/,
  /懶洋洋/,
];
const WORK_PATTERNS = [/得上班/, /八點前出門/, /打卡/];
const OFF_PATTERNS = [/不用上班/, /休息日/, /週六/, /週日/];

const issues = [];

for (const [id, scene] of Object.entries(global.SCENES)) {
  const day = scene.day;
  if (!day) continue;
  const cal = getDemoDayCalendar(day);
  const text = [
    typeof scene.text === 'function' ? scene.text({ flags: {}, memories: [] }) : scene.text,
    typeof scene.sub === 'function' ? scene.sub({ flags: {}, memories: [] }) : scene.sub,
  ].join('\n');

  if (WORKDAY_DAYS.includes(day)) {
    AT_HOME_MIDDDAY_PATTERNS.forEach((re) => {
      if (re.test(text) && scene.location !== 'office' && id !== 'day6_check' && id !== 'day6_quiet' && id !== 'day6_thunder_after') {
        issues.push(`[Day${day} 上班日] ${id}: 可能寫成白天在家 — 匹配 ${re}`);
      }
    });
  }

  if (OFF_DAYS.includes(day)) {
    WORK_PATTERNS.forEach((re) => {
      if (!re.test(text)) return;
      if (/沒有打卡|不用打卡|不必打卡|無須打卡/.test(text)) return;
      issues.push(`[Day${day} 週末] ${id}: 不應出現上班語意 — 匹配 ${re}`);
    });
  }

  if (cal && cal.atWork && scene.location === 'living_sunday' && !isOwnerOnLeave({}, day)) {
    issues.push(`[Day${day}] ${id}: 上班日不應使用 living_sunday 地點`);
  }
}

if (issues.length) {
  console.log('WORK SCHEDULE ISSUES:');
  issues.forEach((line) => console.log(' -', line));
  process.exit(1);
}
console.log('OK: work schedule spot-check passed');
