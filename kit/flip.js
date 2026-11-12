// Flip-house sets: a fixer-upper that renovates itself (set(k): 0 = rundown, 1 = freshly flipped), a SOLD rider, a dumpster.
import * as THREE from 'three';

const std = (color, rough = 0.7, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: rough, ...extra });
const sh = (m) => { m.castShadow = true; m.receiveShadow = true; return m; };
const box = (w, h, d, mat) => sh(new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat));
const C = (h) => new THREE.Color(h);
function textTex(text, bg, fg, w = 512, h = 160, size = 110) { const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); g.fillStyle = bg; g.fillRect(0, 0, w, h); g.fillStyle = fg; g.font = `900 ${size}px Inter, Arial, sans-serif`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(text, w / 2, h / 2 + 6); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }

/** a 5 x 3 x 4 m house (front at z = +2) that blends from rundown to renovated */
export function fixer({ w = 5, h = 3, d = 4 } = {}) {
  const g = new THREE.Group(), parts = [];
  const add = (m) => (g.add(m), parts.push(m), m);
  const wallM = std('#9A9284', 0.95), roofM = std('#5E5650', 0.9), doorM = std('#5B4A3A', 0.8), trimM = std('#8C857A', 0.9);
  const winM = new THREE.MeshStandardMaterial({ color: '#2A2E33', emissive: '#FFC870', emissiveIntensity: 0, roughness: 0.2 });
  const body = add(box(w, h, d, wallM)); body.position.y = h / 2;
  const shape = new THREE.Shape(); shape.moveTo(-w / 2 - 0.3, 0); shape.lineTo(w / 2 + 0.3, 0); shape.lineTo(0, 1.7); shape.closePath();
  const rf = add(sh(new THREE.Mesh(new THREE.ExtrudeGeometry(shape, { depth: d + 0.5, bevelEnabled: true, bevelSize: 0.05, bevelThickness: 0.05, bevelSegments: 2 }), roofM))); rf.position.set(0, h, -d / 2 - 0.25);
  const ch = add(box(0.5, 1.2, 0.5, std('#7A6A60', 0.9))); ch.position.set(w * 0.25, h + 1.1, -0.6);
  const dr = add(box(0.95, 1.9, 0.08, doorM)); dr.position.set(-0.9, 0.95, d / 2 + 0.03);
  const boards = [], wins = [];
  for (const [x, y] of [[0.9, 1.6], [2.0, 1.6], [-2.0, 1.6]]) {
    const wn = add(box(0.8, 0.85, 0.06, winM)); wn.position.set(x, y, d / 2 + 0.03); wins.push(wn);
    const fr = add(box(0.95, 0.08, 0.1, trimM)); fr.position.set(x, y - 0.47, d / 2 + 0.05);
    for (const a of [0.5, -0.45]) { const b = add(box(1.05, 0.14, 0.05, std('#A07B4F', 0.95))); b.position.set(x, y + (a > 0 ? 0.12 : -0.15), d / 2 + 0.09); b.rotation.z = a; boards.push(b); }
  }
  const step = add(box(1.6, 0.18, 0.7, std('#A9A398', 0.9))); step.position.set(-0.9, 0.09, d / 2 + 0.35);
  // overgrown weeds + junk in the yard
  const weeds = new THREE.Group(); g.add(weeds); const wm = std('#6E7F3A', 0.95);
  for (let i = 0; i < 26; i++) { const r = 0.25 + ((i * 37) % 10) / 30; const b = sh(new THREE.Mesh(new THREE.SphereGeometry(r, 10, 8), wm)); b.scale.y = 0.7; b.position.set(-3.2 + ((i * 53) % 64) / 10, r * 0.4, 2.4 + ((i * 29) % 22) / 10); weeds.add(b); }
  const tire = sh(new THREE.Mesh(new THREE.TorusGeometry(0.32, 0.12, 10, 20), std('#1E1E1E', 0.8))); tire.rotation.x = Math.PI / 2; tire.position.set(1.8, 0.12, 3.1); weeds.add(tire);
  // the renovated look
  const OLD = { wall: C('#9A9284'), roof: C('#5E5650'), door: C('#5B4A3A'), trim: C('#8C857A') }, NEW = { wall: C('#F4EEE4'), roof: C('#2F4A63'), door: C('#C9472F'), trim: C('#FFFFFF') };
  const planters = new THREE.Group(); g.add(planters);
  for (const x of [-2.1, 0.3]) { const p = box(0.6, 0.45, 0.6, std('#E8E2D6', 0.7)); p.position.set(x, 0.22, 2.6); planters.add(p); const f = sh(new THREE.Mesh(new THREE.SphereGeometry(0.36, 14, 10), std('#4E8F46', 0.7))); f.position.set(x, 0.7, 2.6); planters.add(f); }
  return { group: g, parts, wins, boards, weeds, planters,
    set(k) { this.parts2({ wall: k, roof: k, door: k, win: k, yard: k }); },
    /** renovate parts separately, each 0..1: wall (paint), roof, door + trim, win (windows + boards), yard (weeds → planters) */
    parts2({ wall = 0, roof = 0, door = 0, win = 0, yard = 0 } = {}) {
      wallM.color.copy(OLD.wall).lerp(NEW.wall, wall); roofM.color.copy(OLD.roof).lerp(NEW.roof, roof); doorM.color.copy(OLD.door).lerp(NEW.door, door); trimM.color.copy(OLD.trim).lerp(NEW.trim, door);
      wallM.roughness = 0.95 - 0.15 * wall; winM.color.copy(C('#2A2E33')).lerp(C('#FFE7B0'), win); winM.emissiveIntensity = 0.55 * win;
      const kb = THREE.MathUtils.clamp(1 - win * 1.6, 0, 1); boards.forEach((b) => { b.visible = kb > 0.01; b.scale.setScalar(Math.max(0.001, kb)); });
      const kw = THREE.MathUtils.clamp(1 - yard * 1.4, 0, 1); weeds.visible = kw > 0.01; weeds.scale.set(1, Math.max(0.001, kw), 1);
      const kp = THREE.MathUtils.clamp(yard * 1.5 - 0.5, 0, 1); planters.visible = kp > 0.01; planters.scale.setScalar(Math.max(0.001, kp));
    } };
}

/** a SOLD rider plank that sits on top of the street's FOR SALE board */
export function soldRider(board) {
  const m = new THREE.MeshStandardMaterial({ map: textTex('SOLD', '#FFFFFF', '#D62839'), roughness: 0.5 });
  const r = sh(new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.32, 0.06), [std('#fff'), std('#fff'), std('#fff'), std('#fff'), m, std('#fff')]));
  r.position.copy(board.position).add(new THREE.Vector3(0, 0.5, 0.02)); board.parent.add(r); return r;
}

/** red coin material for "costs" stacks */
export const redCoin = () => new THREE.MeshStandardMaterial({ color: '#E0483A', metalness: 0.6, roughness: 0.35, emissive: '#4A0A05', emissiveIntensity: 0.3 });
