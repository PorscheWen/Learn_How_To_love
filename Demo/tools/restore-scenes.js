/**
 * Rebuild scenes.js by replaying StrReplace patches from agent transcript.
 */
const fs = require('fs');
const path = require('path');

const transcriptPath = process.argv[2];
const outPath = process.argv[3] || path.join(__dirname, '../js/scenes.js');

const lines = fs.readFileSync(transcriptPath, 'utf8').split(/\n/);
const patches = [];
for (const line of lines) {
  try {
    const o = JSON.parse(line);
    for (const c of o.message?.content || []) {
      if (c.name === 'StrReplace' && c.input?.path?.includes('scenes.js')) {
        patches.push(c.input);
      }
    }
  } catch (_) {}
}

// Start from earliest large block if we can find a Write, else use first successful patch chain
let content = null;
for (const p of patches) {
  if (p.new_string && p.new_string.includes('const SCENES = {')) {
    content = p.new_string;
  }
}

if (!content) {
  // seed: read a known-good excerpt file or minimal
  console.error('No full SCENES block in patches. Patches count:', patches.length);
  process.exit(1);
}

let applied = 0;
for (const p of patches) {
  if (!p.old_string || !p.new_string) continue;
  if (p.replace_all) {
    if (content.includes(p.old_string)) {
      content = content.split(p.old_string).join(p.new_string);
      applied++;
    }
  } else if (content.includes(p.old_string)) {
    content = content.replace(p.old_string, p.new_string);
    applied++;
  }
}

fs.writeFileSync(outPath, content, 'utf8');
console.log('Applied', applied, 'of', patches.length, 'patches. Wrote', outPath);

SCRIPT