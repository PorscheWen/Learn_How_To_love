const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
eval(fs.readFileSync(path.join(root, 'js/scenes.js'), 'utf8').replace(/^const SCENES\s*=/m, 'global.SCENES ='));
eval(fs.readFileSync(path.join(root, 'js/choice-reactions.js'), 'utf8').split('function choiceReactionKey')[0].replace(/^const CHOICE_REACTIONS\s*=/m, 'global.CHOICE_REACTIONS ='));
const missing = [];
for (const [id, scene] of Object.entries(global.SCENES)) {
  if (!scene.choices) continue;
  for (const c of scene.choices) {
    const key = `${id}::${String(c.text || '').trim()}`;
    if (!global.CHOICE_REACTIONS[key]) missing.push(key);
  }
}
console.log(missing.length ? missing.join('\n') : 'OK: all choices mapped');
