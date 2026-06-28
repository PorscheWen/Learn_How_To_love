/** Music attribution (CC-BY) — see assets/audio/CREDITS.md */
function showMusicCreditsDialog() {
  const dlg = document.getElementById('music-credits-dialog');
  if (dlg) dlg.showModal();
}

if (typeof module !== 'undefined') module.exports = { showMusicCreditsDialog };
