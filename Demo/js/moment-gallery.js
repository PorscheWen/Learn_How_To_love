/**
 * 時刻快照 — 每個場景自動截圖，存入 IndexedDB，於腳印集瀏覽
 */
const MomentGallery = (function () {
  const DB_NAME = 'lhtl_demo_moments';
  const DB_VERSION = 1;
  const STORE = 'captures';
  const CAPTURE_W = 960;
  const CAPTURE_H = 540;

  const LOCATION_BG = {
    prologue_rain: 'assets/bg/bg-prologue-rain.png',
    living_corner: 'assets/bg/bg-living-corner.png',
    living_room: 'assets/bg/bg-living-room.png',
    living_sunday: 'assets/bg/bg-living-room.png',
    living_warm: 'assets/bg/bg-living-warm.png',
    kitchen: 'assets/bg/bg-kitchen.png',
    kitchen_morning: 'assets/bg/bg-kitchen.png',
    office: 'assets/bg/bg-living-room.png',
    balcony: 'assets/demo-balcony-puppy.png',
    bathroom_night: 'assets/bg/bg-bedroom-night.png',
    bedroom_night: 'assets/bg/bg-bedroom-night.png',
    pet_shop: 'assets/bg/bg-pet-shop.png',
    pet_vet: 'assets/bg/bg-pet-vet.png',
    hallway: 'assets/bg/bg-living-corner.png',
    doorway: 'assets/bg/bg-entrance-night.png',
    entrance_night: 'assets/bg/bg-entrance-night.png',
    stairwell: 'assets/bg/bg-stairwell.png',
    street: 'assets/bg/bg-street.png',
    park: 'assets/bg/bg-park.png',
    street_sunset: 'assets/bg/bg-street-sunset.png',
    living_storm: 'assets/bg/bg-living-storm.png',
    window_rain: 'assets/bg/bg-window-rain.png',
    epilogue_home: 'assets/bg/bg-living-warm.png',
  };

  let dbPromise = null;

  function openDb() {
    if (dbPromise) return dbPromise;
    dbPromise = new Promise((resolve, reject) => {
      if (!window.indexedDB) {
        reject(new Error('IndexedDB unavailable'));
        return;
      }
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onerror = () => reject(req.error);
      req.onsuccess = () => resolve(req.result);
      req.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains(STORE)) {
          const store = db.createObjectStore(STORE, { keyPath: 'id' });
          store.createIndex('sessionId', 'sessionId', { unique: false });
          store.createIndex('capturedAt', 'capturedAt', { unique: false });
        }
      };
    });
    return dbPromise;
  }

  function loadImage(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => resolve(img);
      img.onerror = () => reject(new Error(`image load failed: ${src}`));
      img.src = src;
    });
  }

  function drawCover(ctx, img, w, h) {
    const ir = img.width / img.height;
    const cr = w / h;
    let sw;
    let sh;
    let sx = 0;
    let sy = 0;
    if (ir > cr) {
      sh = img.height;
      sw = sh * cr;
      sx = (img.width - sw) / 2;
    } else {
      sw = img.width;
      sh = sw / cr;
      sy = (img.height - sh) * 0.22;
    }
    ctx.drawImage(img, sx, sy, sw, sh, 0, 0, w, h);
  }

  function momentCaption(scene, state) {
    const locMeta = typeof LOCATIONS !== 'undefined' ? LOCATIONS[scene.location] : null;
    const locLabel = locMeta?.label || scene.location || '';
    const name = typeof dogLabel === 'function' ? dogLabel(state) : '牠';
    return `Day ${scene.day} · ${locLabel} · ${name}`;
  }

  async function composeCapture(scene, state) {
    const canvas = document.createElement('canvas');
    canvas.width = CAPTURE_W;
    canvas.height = CAPTURE_H;
    const ctx = canvas.getContext('2d');
    const loc = scene.location || 'living_room';
    const bgUrl = LOCATION_BG[loc] || LOCATION_BG.living_room;

    ctx.fillStyle = '#1a1512';
    ctx.fillRect(0, 0, CAPTURE_W, CAPTURE_H);

    try {
      const bg = await loadImage(bgUrl);
      drawCover(ctx, bg, CAPTURE_W, CAPTURE_H);
    } catch (_) {
      /* gradient fallback */
      const g = ctx.createLinearGradient(0, 0, 0, CAPTURE_H);
      g.addColorStop(0, '#3d3528');
      g.addColorStop(1, '#1a1512');
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, CAPTURE_W, CAPTURE_H);
    }

    if (loc === 'office') {
      ctx.fillStyle = 'rgba(30, 37, 48, 0.38)';
      ctx.fillRect(0, 0, CAPTURE_W, CAPTURE_H);
    }

    const vignette = ctx.createLinearGradient(0, 0, 0, CAPTURE_H);
    vignette.addColorStop(0, 'rgba(26, 22, 20, 0.08)');
    vignette.addColorStop(0.45, 'rgba(26, 22, 20, 0)');
    vignette.addColorStop(0.78, 'rgba(26, 22, 20, 0.22)');
    vignette.addColorStop(1, 'rgba(26, 22, 20, 0.45)');
    ctx.fillStyle = vignette;
    ctx.fillRect(0, 0, CAPTURE_W, CAPTURE_H);

    const dogEl = document.getElementById('dog-img');
    const stageHidden = document.getElementById('dog-stage')?.classList.contains('is-hidden');
    const hideDog = stageHidden || loc === 'office' || loc === 'pet_shop' || loc === 'balcony' || scene?.hideDog;

    if (!hideDog && dogEl?.src) {
      try {
        const dog = await loadImage(dogEl.src);
        const maxW = CAPTURE_W * 0.46;
        const maxH = CAPTURE_H * 0.44;
        const scale = Math.min(maxW / dog.width, maxH / dog.height, 1.2);
        const dw = dog.width * scale;
        const dh = dog.height * scale;
        const dx = (CAPTURE_W - dw) / 2;
        const dy = CAPTURE_H * 0.5 - dh;
        ctx.save();
        ctx.shadowColor = 'rgba(0, 0, 0, 0.4)';
        ctx.shadowBlur = 24;
        ctx.shadowOffsetY = 12;
        ctx.drawImage(dog, dx, dy, dw, dh);
        ctx.restore();
      } catch (_) {}
    }

    const smellEl = document.getElementById('smell-text');
    const smell = smellEl?.textContent?.trim() || state.smell || '';
    if (smell) {
      ctx.fillStyle = 'rgba(26, 22, 20, 0.62)';
      ctx.fillRect(0, 0, CAPTURE_W, 40);
      ctx.fillStyle = 'rgba(255, 248, 240, 0.92)';
      ctx.font = '500 15px "Noto Sans TC", sans-serif';
      const short = smell.length > 36 ? `${smell.slice(0, 35)}…` : smell;
      ctx.fillText(`氣味 · ${short}`, 14, 26);
    }

    const caption = momentCaption(scene, state);
    ctx.font = '500 13px "Noto Sans TC", sans-serif';
    const tw = ctx.measureText(caption).width;
    ctx.fillStyle = 'rgba(26, 22, 20, 0.7)';
    ctx.fillRect(CAPTURE_W - tw - 28, CAPTURE_H - 36, tw + 20, 28);
    ctx.fillStyle = '#f5ebe0';
    ctx.fillText(caption, CAPTURE_W - tw - 18, CAPTURE_H - 16);

    return {
      dataUrl: canvas.toDataURL('image/jpeg', 0.82),
      caption,
    };
  }

  async function captureAndStore(sessionId, scene, state) {
    if (!sessionId || !scene?.id || scene.isEpilogue || scene.noMomentCapture) return false;
    try {
      const { dataUrl, caption } = await composeCapture(scene, state);
      const db = await openDb();
      const record = {
        id: `${sessionId}:${scene.id}`,
        sessionId,
        sceneId: scene.id,
        day: scene.day,
        location: scene.location,
        caption,
        dataUrl,
        capturedAt: Date.now(),
      };
      await new Promise((resolve, reject) => {
        const tx = db.transaction(STORE, 'readwrite');
        tx.objectStore(STORE).put(record);
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
      });
      return true;
    } catch (err) {
      console.warn('[MomentGallery]', err);
      return false;
    }
  }

  async function listForSession(sessionId) {
    if (!sessionId) return [];
    try {
      const db = await openDb();
      const all = await new Promise((resolve, reject) => {
        const tx = db.transaction(STORE, 'readonly');
        const req = tx.objectStore(STORE).index('sessionId').getAll(sessionId);
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => reject(req.error);
      });
      return all.sort((a, b) => a.capturedAt - b.capturedAt);
    } catch (_) {
      return [];
    }
  }

  async function getById(id) {
    try {
      const db = await openDb();
      return await new Promise((resolve, reject) => {
        const tx = db.transaction(STORE, 'readonly');
        const req = tx.objectStore(STORE).get(id);
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => reject(req.error);
      });
    } catch (_) {
      return null;
    }
  }

  async function clearSession(sessionId) {
    if (!sessionId) return;
    try {
      const db = await openDb();
      const items = await listForSession(sessionId);
      await new Promise((resolve, reject) => {
        const tx = db.transaction(STORE, 'readwrite');
        const store = tx.objectStore(STORE);
        items.forEach((item) => store.delete(item.id));
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
      });
    } catch (_) {}
  }

  function waitForDogImage() {
    return new Promise((resolve) => {
      const img = document.getElementById('dog-img');
      if (!img || img.complete) {
        resolve();
        return;
      }
      const done = () => resolve();
      img.addEventListener('load', done, { once: true });
      img.addEventListener('error', done, { once: true });
      setTimeout(done, 800);
    });
  }

  function scheduleCapture(sessionId, scene, state, onStored) {
    if (!sessionId || !scene?.id || scene.isEpilogue || scene.noMomentCapture) return;
    requestAnimationFrame(() => {
      requestAnimationFrame(async () => {
        await waitForDogImage();
        const ok = await captureAndStore(sessionId, scene, state);
        if (ok && typeof onStored === 'function') onStored(scene.id);
      });
    });
  }

  return {
    captureAndStore,
    listForSession,
    getById,
    clearSession,
    scheduleCapture,
    momentCaption,
  };
})();

if (typeof module !== 'undefined') module.exports = { MomentGallery };
