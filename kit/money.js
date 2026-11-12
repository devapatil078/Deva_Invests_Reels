// Money-world sets for Deep Dive 3D (real estate / business topics). Same soft, sunlit look as the kitchen.
//   street(E)  sunlit suburban street + hero house      xrayHouse(E)  the house as cyan glass, filled with YOU / BANK
//   house(o)   a reusable house group                     coins(n)      gold coin stack       lever()   seesaw + fulcrum
import * as THREE from 'three';
import { lightRig } from './engine.js';
import { xrayMaterial } from './sets.js';

const std = (color, rough = 0.7, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: rough, ...extra });
const sh = (m) => { m.castShadow = true; m.receiveShadow = true; return m; };
const box = (w, h, d, mat) => sh(new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat));
function gradTex(top, bot) { const c = document.createElement('canvas'); c.width = 4; c.height = 256; const g = c.getContext('2d'); const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, top); gr.addColorStop(1, bot); g.fillStyle = gr; g.fillRect(0, 0, 4, 256); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }

/** a house: body 5 x 3 x 4 m, gable roof, door, windows. Front face at z = +2 (local). */
export function house({ wall = '#F2E6D3', roof = '#B5523B', trim = '#FFFFFF', door = '#3F6E8C', w = 5, h = 3, d = 4 } = {}) {
  const g = new THREE.Group(), parts = [], add = (m) => (g.add(m), parts.push(m), m);
  const body = add(box(w, h, d, std(wall, 0.85))); body.position.y = h / 2;
  const shape = new THREE.Shape(); shape.moveTo(-w / 2 - 0.3, 0); shape.lineTo(w / 2 + 0.3, 0); shape.lineTo(0, 1.7); shape.closePath();
  const rg = new THREE.ExtrudeGeometry(shape, { depth: d + 0.5, bevelEnabled: true, bevelSize: 0.05, bevelThickness: 0.05, bevelSegments: 2 });
  const rf = add(sh(new THREE.Mesh(rg, std(roof, 0.6)))); rf.position.set(0, h, -d / 2 - 0.25);
  const ch = add(box(0.5, 1.2, 0.5, std('#9C5A48', 0.8))); ch.position.set(w * 0.25, h + 1.1, -0.6);
  const dr = add(box(0.95, 1.9, 0.08, std(door, 0.45))); dr.position.set(-0.9, 0.95, d / 2 + 0.03);
  const win = new THREE.MeshStandardMaterial({ color: '#FFE7B0', emissive: '#FFC870', emissiveIntensity: 0.55, roughness: 0.2 });
  for (const [x, y] of [[0.9, 1.6], [2.0, 1.6], [-2.0, 1.6]]) {
    const wn = add(box(0.8, 0.85, 0.06, win)); wn.position.set(x, y, d / 2 + 0.03);
    const fr = add(box(0.95, 0.08, 0.1, std(trim, 0.4))); fr.position.set(x, y - 0.47, d / 2 + 0.05);
  }
  const step = add(box(1.6, 0.18, 0.7, std('#C9C2B5', 0.9))); step.position.set(-0.9, 0.09, d / 2 + 0.35);
  return { group: g, parts, setMaterial(m) { parts.forEach((p) => { p.userData.mat ??= p.material; p.material = m || p.userData.mat; p.castShadow = !m; }); } };
}

function tree(x, z, s = 1) {
  const g = new THREE.Group();
  const tr = box(0.22 * s, 1.4 * s, 0.22 * s, std('#7A5638', 0.9)); tr.position.y = 0.7 * s; g.add(tr);
  const leaf = std('#5E9A50', 0.75);
  for (const [dx, dy, dz, r] of [[0, 2.0, 0, 1.0], [0.55, 1.7, 0.2, 0.7], [-0.5, 1.75, -0.1, 0.72], [0.1, 2.5, 0.1, 0.65]]) {
    const b = sh(new THREE.Mesh(new THREE.SphereGeometry(r * s, 20, 14), leaf)); b.position.set(dx * s, dy * s, dz * s); g.add(b);
  }
  g.position.set(x, 0, z); return g;
}

/** sunlit suburban street; the hero house sits at the origin with its front at z = 2 */
export function street(E, { sign = true } = {}) {
  const scene = new THREE.Scene(); scene.environment = E.envMap; scene.environmentIntensity = 0.35;
  scene.background = gradTex('#8FC3EA', '#F4E6CF'); scene.fog = new THREE.Fog('#EADFCB', 30, 75);
  const grass = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), std('#86B96F', 0.95)); grass.rotation.x = -Math.PI / 2; grass.receiveShadow = true; scene.add(grass);
  const road = new THREE.Mesh(new THREE.PlaneGeometry(80, 5), std('#55585F', 0.9)); road.rotation.x = -Math.PI / 2; road.position.set(0, 0.01, 9); road.receiveShadow = true; scene.add(road);
  const walk = new THREE.Mesh(new THREE.PlaneGeometry(80, 1.4), std('#D9D2C4', 0.9)); walk.rotation.x = -Math.PI / 2; walk.position.set(0, 0.015, 5.8); walk.receiveShadow = true; scene.add(walk);
  const path = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 3.4), std('#D9D2C4', 0.9)); path.rotation.x = -Math.PI / 2; path.position.set(-0.9, 0.02, 3.8); scene.add(path);
  const H = house(); scene.add(H.group);
  const n1 = house({ wall: '#DCE7EE', roof: '#4E6E8E', door: '#B5523B' }); n1.group.position.set(-9, 0, -1); scene.add(n1.group);
  const n2 = house({ wall: '#EFE0C2', roof: '#6E8F5A', door: '#7A4E8C' }); n2.group.position.set(9, 0, -1); scene.add(n2.group);
  for (const [x, z, s] of [[-4.6, 3.2, 0.9], [4.8, 2.6, 1.1], [-13, 3, 1.2], [13, 2.5, 1.0], [0, -6, 1.3]]) scene.add(tree(x, z, s));
  const fence = std('#FFFFFF', 0.5);
  for (let i = 0; i < 22; i++) { const x = -6.5 + i * 0.6; if (x > -1.6 && x < -0.2) continue; const p = box(0.1, 0.8, 0.06, fence); p.position.set(x, 0.4, 5.0); scene.add(p); }
  const rail = box(13, 0.08, 0.05, fence); rail.position.set(0, 0.62, 5.0); scene.add(rail);
  let board = null;
  if (sign) { const post = box(0.1, 1.6, 0.1, std('#FFFFFF', 0.5)); post.position.set(2.6, 0.8, 4.3); scene.add(post);
    const c = document.createElement('canvas'); c.width = 512; c.height = 300; const g = c.getContext('2d'); g.fillStyle = '#D62839'; g.fillRect(0, 0, 512, 300); g.fillStyle = '#fff'; g.font = '900 96px Inter'; g.textAlign = 'center'; g.fillText('FOR', 256, 130); g.fillText('SALE', 256, 240);
    const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
    board = sh(new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.65, 0.05), [std('#D62839'), std('#D62839'), std('#D62839'), std('#D62839'), new THREE.MeshStandardMaterial({ map: tx, roughness: 0.5 }), std('#D62839')])); board.position.set(2.6, 1.35, 4.33); scene.add(board); }
  const L = lightRig(scene, { key: '#FFD9AE', keyI: 3.6, keyPos: [8, 9, 7], target: [0, 1, 1], rimCol: '#CFE0FF', rimI: 1.0, hemiI: 0.95, sky: '#DDEEFF', ground: '#6E8F5A', shadowBox: 10 });
  const fill = new THREE.DirectionalLight('#FFF1E2', 0.7); fill.position.set(-6, 5, 8); scene.add(fill);
  return { scene, house: H, lights: L, board, fill,
    /** mood 0 = sunny day, 1 = cold dusk (prices falling) */
    mood(k) { const day = new THREE.Color('#FFD9AE'), dusk = new THREE.Color('#9FB4D8'); L.key.color.copy(day).lerp(dusk, k); L.key.intensity = 3.6 - 1.8 * k; fill.intensity = 0.7 - 0.3 * k;
      scene.background = k > 0.5 ? (this._dusk ??= gradTex('#2E3A5C', '#8A6E78')) : (this._day ??= gradTex('#8FC3EA', '#F4E6CF')); } };
}

/** the hero house as cyan glass, filled like a jar: gold = your money (bottom), blue = the bank's (top) */
export function xrayHouse(E) {
  const scene = new THREE.Scene();
  scene.background = gradTex('#0B1A30', '#03070F');
  scene.add(new THREE.HemisphereLight('#9FD9FF', '#05080F', 0.6));
  const k = new THREE.DirectionalLight('#DDF4FF', 2.0); k.position.set(4, 6, 6); scene.add(k);
  const grid = new THREE.GridHelper(40, 60, '#1F6F88', '#123A4A'); grid.material.transparent = true; grid.material.opacity = 0.35; scene.add(grid);
  const H = house(), xm = xrayMaterial('#4FD1E8', 0.9); H.setMaterial(xm); scene.add(H.group);
  const glow = (col, i = 0.5) => new THREE.MeshStandardMaterial({ color: col, emissive: col, emissiveIntensity: i, roughness: 0.35, transparent: true, opacity: 0.9 });
  const you = new THREE.Mesh(new THREE.BoxGeometry(4.7, 1, 3.7), glow('#FFC53D')), bank = new THREE.Mesh(new THREE.BoxGeometry(4.7, 1, 3.7), glow('#2F6BFF', 0.6));
  H.group.add(you, bank);
  const GOLD = new THREE.Color('#FFC53D'), RED = new THREE.Color('#FF4A4A');
  return { scene, house: H, xmat: xm, you, bank,
    /** fill heights as fractions of the 2.9 m body: y = yours (bottom), b = bank's (top); red 0..1 tints yours red; glow boosts yours */
    fill(y, b, red = 0, glow = 0) { const HH = 2.9, hy = Math.max(0.001, HH * y), hb = Math.max(0.001, HH * b);
      you.scale.y = hy; you.position.y = 0.05 + hy / 2; bank.scale.y = hb; bank.position.y = 0.05 + hy + hb / 2;
      you.material.color.copy(GOLD).lerp(RED, red); you.material.emissive.copy(you.material.color); you.material.emissiveIntensity = 0.5 + glow;
      you.visible = y > 0.001; bank.visible = b > 0.001; } };
}

/** gold coin stack: returns { group, set(n) } (n coins visible, max 40) */
export function coins(max = 40) {
  const g = new THREE.Group(), mat = new THREE.MeshStandardMaterial({ color: '#E8B93A', metalness: 0.85, roughness: 0.28, emissive: '#5A3A00', emissiveIntensity: 0.25 });
  const geo = new THREE.CylinderGeometry(0.32, 0.32, 0.075, 40), list = [];
  for (let i = 0; i < max; i++) { const c = sh(new THREE.Mesh(geo, mat)); c.position.set(Math.sin(i * 1.7) * 0.02, 0.04 + i * 0.08, Math.cos(i * 1.3) * 0.02); c.rotation.y = i * 0.4; g.add(c); list.push(c); }
  return { group: g, mat, set(n) { list.forEach((c, i) => (c.visible = i < n)); } };
}

/** a giant lever: beam on a triangular fulcrum. tilt(deg) rotates the beam; .left / .right are anchor groups on each end */
export function lever() {
  const g = new THREE.Group();
  const fShape = new THREE.Shape(); fShape.moveTo(-0.9, 0); fShape.lineTo(0.9, 0); fShape.lineTo(0, 1.4); fShape.closePath();
  const fu = sh(new THREE.Mesh(new THREE.ExtrudeGeometry(fShape, { depth: 1.2, bevelEnabled: true, bevelSize: 0.06, bevelThickness: 0.06 }), std('#3F6E8C', 0.5)));
  fu.position.set(-2.0, 0, -0.6); g.add(fu);
  const pivot = new THREE.Group(); pivot.position.set(-2.0, 1.5, 0); g.add(pivot);
  const beam = box(11, 0.28, 1.0, std('#C98A4B', 0.55)); beam.position.x = 2.0; pivot.add(beam);
  const left = new THREE.Group(); left.position.set(-3.2, 0.14, 0); pivot.add(left);
  const right = new THREE.Group(); right.position.set(7.2, 0.14, 0); pivot.add(right);
  return { group: g, left, right, tilt(deg) { pivot.rotation.z = THREE.MathUtils.degToRad(deg); } };
}

/** a plain dark studio for the lever / coins (soft key light, floor that fades to black) */
export function studio(E) {
  const scene = new THREE.Scene(); scene.environment = E.envMap; scene.environmentIntensity = 0.3;
  scene.background = gradTex('#1B2236', '#07090F'); scene.fog = new THREE.Fog('#07090F', 14, 34);
  const fl = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), std('#1C2335', 0.6)); fl.rotation.x = -Math.PI / 2; fl.receiveShadow = true; scene.add(fl);
  const L = lightRig(scene, { key: '#FFE2C2', keyI: 3.4, keyPos: [5, 9, 6], target: [1, 1, 0], rimCol: '#7FB2FF', rimI: 2.4, hemiI: 0.5, sky: '#3A4A6A', ground: '#0A0C12', shadowBox: 9 });
  return { scene, lights: L };
}
