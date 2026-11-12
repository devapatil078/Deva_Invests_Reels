// Main-street sets for Deep Dive 3D: a row of 15 small shops that can close one by one, and a glowing survival chart.
import * as THREE from 'three';
import { lightRig } from './engine.js';
import { xrayMaterial } from './sets.js';

const std = (color, rough = 0.7, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: rough, ...extra });
const sh = (m) => { m.castShadow = true; m.receiveShadow = true; return m; };
const box = (w, h, d, mat) => sh(new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat));
function gradTex(top, bot) { const c = document.createElement('canvas'); c.width = 4; c.height = 256; const g = c.getContext('2d'); const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, top); gr.addColorStop(1, bot); g.fillStyle = gr; g.fillRect(0, 0, 4, 256); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }
function textTex(text, bg, fg, w = 512, h = 128, size = 72) { const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); g.fillStyle = bg; g.fillRect(0, 0, w, h); g.fillStyle = fg; g.font = `900 ${size}px Inter, Arial, sans-serif`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(text, w / 2, h / 2 + 4); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }
function stripeTex(a, b) { const c = document.createElement('canvas'); c.width = 256; c.height = 16; const g = c.getContext('2d'); for (let i = 0; i < 8; i++) { g.fillStyle = i % 2 ? b : a; g.fillRect(i * 32, 0, 32, 16); } const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }

const NAMES = ['NOODLE', 'PAGE ONE', 'GLOW NAILS', 'FRESH CUT', 'FIT LAB', 'SLICE', 'PAWS', 'BEAN BAR', 'VINYL', 'TINY TOYS', 'BLOOM', 'TACO TOWN', 'SPIN', 'THE CRAFT', 'PIXEL FIX'];
const COLS = [['#E9D7BF', '#D62839'], ['#CFE1E8', '#2F6FB5'], ['#F1D9DF', '#C04A7A'], ['#E5E0D2', '#3E7D4F'], ['#D9DDE6', '#F08A24'], ['#EFE3C8', '#B5523B'], ['#DDE8D6', '#6E8F5A'], ['#F2E6D3', '#1F7A6E'], ['#E4DAEC', '#6B4E9B'], ['#F5E3CF', '#E0A21B'], ['#E8E1D8', '#C2456B'], ['#F0DCC0', '#D9572B'], ['#DCE3EA', '#3F6E8C'], ['#E7DFD0', '#7A5638'], ['#D8E4E8', '#1D8CC4']];
const BRICK = ['#B8664E', '#9C6B55', '#C08A6A', '#8E5A4A', '#A87A62'];

/** one shop: 3.8 m wide, shop floor + one upper storey. setOpen(k): 1 = lit and open, 0 = dark with the shutter down */
export function shop(i) {
  const g = new THREE.Group(), [wall, acc] = COLS[i % COLS.length], W = 3.8;
  const upper = box(W, 3.0, 3.0, std(BRICK[i % BRICK.length], 0.9)); upper.position.set(0, 4.7, -1.5); g.add(upper);
  for (const x of [-0.9, 0.9]) { const w = box(0.9, 1.3, 0.05, std('#2B3240', 0.25, { metalness: 0.2 })); w.position.set(x, 4.8, 0.03); g.add(w); const s = box(1.05, 0.1, 0.15, std('#EDEDED', 0.5)); s.position.set(x, 4.1, 0.06); g.add(s); }
  const cap = box(W + 0.1, 0.25, 3.2, std('#5A4A42', 0.8)); cap.position.set(0, 6.3, -1.5); g.add(cap);
  const base = box(W, 3.2, 3.0, std(wall, 0.85)); base.position.set(0, 1.6, -1.5); g.add(base);
  const signMat = new THREE.MeshStandardMaterial({ map: textTex(NAMES[i % NAMES.length], acc, '#FFFFFF'), roughness: 0.5, emissive: '#FFFFFF', emissiveIntensity: 0.0, emissiveMap: null });
  const sign = sh(new THREE.Mesh(new THREE.BoxGeometry(3.3, 0.6, 0.1), [std(acc), std(acc), std(acc), std(acc), signMat, std(acc)])); sign.position.set(0, 2.85, 0.06); g.add(sign);
  const glass = new THREE.MeshStandardMaterial({ color: '#FFB85C', emissive: '#FF9F3A', emissiveIntensity: 0.8, roughness: 0.15 });
  const win = box(2.2, 1.7, 0.05, glass); win.position.set(0.55, 1.35, 0.03); g.add(win);
  const door = box(0.85, 2.1, 0.05, glass); door.position.set(-1.25, 1.05, 0.03); g.add(door);
  const frame = std('#2B2B2E', 0.5);
  for (const [x, y, w, h] of [[0.55, 2.22, 2.3, 0.08], [0.55, 0.48, 2.3, 0.08], [-1.25, 2.13, 0.95, 0.08]]) { const f = box(w, h, 0.08, frame); f.position.set(x, y, 0.06); g.add(f); }
  const sm = new THREE.MeshStandardMaterial({ map: stripeTex(acc, '#FFFFFF'), roughness: 0.8, side: THREE.DoubleSide });
  const awn = sh(new THREE.Mesh(new THREE.PlaneGeometry(3.6, 1.1), sm)); awn.position.set(0, 2.35, 0.5); awn.rotation.x = -1.0; g.add(awn);
  const shutter = box(3.5, 2.2, 0.06, std('#3A3D44', 0.55, { metalness: 0.4 })); shutter.position.set(0, 1.2, 0.12); g.add(shutter);
  const openTag = sh(new THREE.Mesh(new THREE.PlaneGeometry(0.55, 0.22), new THREE.MeshBasicMaterial({ map: textTex('OPEN', '#D62839', '#FFFFFF', 256, 100, 64) }))); openTag.position.set(-1.25, 1.45, 0.07); g.add(openTag);
  const closedTag = sh(new THREE.Mesh(new THREE.PlaneGeometry(1.6, 0.5), new THREE.MeshBasicMaterial({ map: textTex('CLOSED', '#1B1B1F', '#FFFFFF', 400, 125, 80) }))); closedTag.position.set(0, 1.5, 0.16); g.add(closedTag);
  g.position.x = 0;
  return { group: g, glass, sign, shutter, openTag, closedTag,
    setOpen(k) { glass.emissiveIntensity = 0.8 * k;
      glass.color.copy(new THREE.Color('#1E2128').lerp(new THREE.Color('#FFB85C'), k)); signMat.color.copy(new THREE.Color('#3A3A3A').lerp(new THREE.Color('#FFFFFF'), k));
      const down = 1 - k; shutter.scale.y = Math.max(0.001, down); shutter.position.y = 2.3 - 1.1 * down; shutter.visible = down > 0.01;
      openTag.visible = k > 0.5; closedTag.visible = down > 0.85; } };
}

/** main street: 15 shops along x (index 7 at x = 0 is the hero's), sidewalk, road, lamps */
export function mainStreet(E) {
  const scene = new THREE.Scene(); scene.environment = E.envMap; scene.environmentIntensity = 0.35;
  scene.background = gradTex('#7FB0DE', '#F6D9B8'); scene.fog = new THREE.Fog('#EAD3BA', 60, 130);
  const gnd = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), std('#5A5D64', 0.9)); gnd.rotation.x = -Math.PI / 2; gnd.receiveShadow = true; scene.add(gnd);
  const walk = box(70, 0.15, 3.0, std('#CFC8BA', 0.9)); walk.position.set(0, 0.075, 1.5); scene.add(walk);
  const curb = box(70, 0.18, 0.2, std('#BDB5A6', 0.8)); curb.position.set(0, 0.09, 3.05); scene.add(curb);
  for (let i = 0; i < 18; i++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 0.18), std('#F2F2F2', 0.6)); m.rotation.x = -Math.PI / 2; m.position.set(-34 + i * 4, 0.01, 7.5); scene.add(m); }
  const shops = [];
  for (let i = 0; i < 15; i++) { const s = shop(i); s.group.position.x = (i - 7) * 4; scene.add(s.group); shops.push(s); }
  const lampM = std('#2B2B2E', 0.4, { metalness: 0.5 }), bulb = new THREE.MeshStandardMaterial({ color: '#FFF2CC', emissive: '#FFD58A', emissiveIntensity: 1.2 });
  for (let i = 0; i < 8; i++) { const x = (i - 3.5) * 8; const p = box(0.12, 4.2, 0.12, lampM); p.position.set(x, 2.1, 2.8); scene.add(p); const b = new THREE.Mesh(new THREE.SphereGeometry(0.22, 16, 12), bulb); b.position.set(x, 4.3, 2.8); scene.add(b); }
  const L = lightRig(scene, { key: '#FFCF9E', keyI: 2.0, keyPos: [14, 12, 14], target: [0, 1, 0], rimCol: '#CFE0FF', rimI: 0.8, hemiI: 0.55, sky: '#DDEEFF', ground: '#6A6058', shadowBox: 18 });
  const fill = new THREE.DirectionalLight('#FFF1E2', 0.6); fill.position.set(-8, 6, 12); scene.add(fill);
  return { scene, shops, lights: L, set(openList) { shops.forEach((s, i) => s.setOpen(openList[i])); } };
}

/** a glowing survival chart on a dark x-ray stage: bars[i].set(frac 0..1, grow 0..1, red 0..1 on the lost part) */
export function chart(E, n = 4) {
  const scene = new THREE.Scene(); scene.background = gradTex('#0B1A30', '#03070F');
  scene.add(new THREE.HemisphereLight('#9FD9FF', '#05080F', 0.6)); const k = new THREE.DirectionalLight('#DDF4FF', 1.6); k.position.set(4, 8, 8); scene.add(k);
  const grid = new THREE.GridHelper(60, 80, '#1F6F88', '#123A4A'); grid.material.transparent = true; grid.material.opacity = 0.35; scene.add(grid);
  const HMAX = 6, BW = 1.4, gap = 2.1, bars = [];
  for (let i = 0; i < n; i++) {
    const x = (i - (n - 1) / 2) * gap;
    const ghost = new THREE.Mesh(new THREE.BoxGeometry(BW, HMAX, BW), xrayMaterial('#4FD1E8', 0.7)); ghost.position.set(x, HMAX / 2, 0); scene.add(ghost);
    const fm = new THREE.MeshStandardMaterial({ color: '#4FD1E8', emissive: '#4FD1E8', emissiveIntensity: 0.55, roughness: 0.3, transparent: true, opacity: 0.92 });
    const fill = new THREE.Mesh(new THREE.BoxGeometry(BW * 0.92, 1, BW * 0.92), fm); scene.add(fill);
    const lm = new THREE.MeshStandardMaterial({ color: '#FF4A4A', emissive: '#FF4A4A', emissiveIntensity: 0.8, roughness: 0.3, transparent: true, opacity: 0.0 });
    const lost = new THREE.Mesh(new THREE.BoxGeometry(BW * 0.92, 1, BW * 0.92), lm); scene.add(lost);
    bars.push({ x, ghost, fill, lost, top: new THREE.Vector3(x, 0, 0),
      set(frac, grow = 1, red = 0) { const h = Math.max(0.001, HMAX * frac * grow); fill.scale.y = h; fill.position.set(x, h / 2, 0); this.top.set(x, h, 0);
        const lh = Math.max(0.001, HMAX * (1 - frac) * grow); lost.scale.y = lh; lost.position.set(x, h + lh / 2, 0); lm.opacity = 0.75 * red; lost.visible = red > 0.01; } });
  }
  return { scene, bars, HMAX };
}
