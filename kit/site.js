// Construction sets for Deep Dive 3D: a sunlit job site (timber frame, scaffold, tower crane, rain), a hard hat for a Human,
// and a giant dollar bill that splits into cost slabs and a thin gold 6-cent profit strip.
import * as THREE from 'three';
import { lightRig } from './engine.js';

const std = (color, rough = 0.7, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: rough, ...extra });
const sh = (m) => { m.castShadow = true; m.receiveShadow = true; return m; };
const box = (w, h, d, mat) => sh(new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat));
function gradTex(top, bot) { const c = document.createElement('canvas'); c.width = 4; c.height = 256; const g = c.getContext('2d'); const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, top); gr.addColorStop(1, bot); g.fillStyle = gr; g.fillRect(0, 0, 4, 256); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }

export function hardHat(human, color = '#FFC21A') {
  const m = std(color, 0.35), g = new THREE.Group();
  const dome = sh(new THREE.Mesh(new THREE.SphereGeometry(0.142, 28, 16, 0, Math.PI * 2, 0, Math.PI / 2), m)); dome.position.y = 0.2; g.add(dome);
  const brim = sh(new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.17, 0.018, 28), m)); brim.position.set(0, 0.2, 0.02); brim.scale.set(1, 1, 1.12); g.add(brim);
  const ridge = sh(new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.03, 0.26), m)); ridge.position.set(0, 0.335, 0); g.add(ridge);
  human.head.add(g); return g;
}

/** the job site. update(t, { craneYaw, rain 0..1, mood 0..1 }) */
export function jobSite(E) {
  const scene = new THREE.Scene(); scene.environment = E.envMap; scene.environmentIntensity = 0.35;
  const day = gradTex('#86BCE8', '#F3E2C8'), dusk = gradTex('#3A4560', '#7D7A80'); scene.background = day; scene.fog = new THREE.Fog('#E6D8C2', 45, 110);
  const dirt = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), std('#B89B78', 0.97)); dirt.rotation.x = -Math.PI / 2; dirt.receiveShadow = true; scene.add(dirt);
  const grass = new THREE.Mesh(new THREE.PlaneGeometry(200, 60), std('#86B96F', 0.95)); grass.rotation.x = -Math.PI / 2; grass.position.set(0, 0.005, -55); scene.add(grass);
  // timber frame house on a concrete slab
  const wood = std('#D9B27C', 0.8), conc = std('#B9B6AE', 0.9);
  const slab = box(9, 0.3, 7, conc); slab.position.set(0, 0.15, 0); scene.add(slab);
  const lerp = (a, b, k) => a + (b - a) * k;
  const wall = (x0, z0, x1, z1, y0) => { const L = Math.hypot(x1 - x0, z1 - z0), n = Math.round(L / 0.6), ang = Math.atan2(z1 - z0, x1 - x0);
    for (let i = 0; i <= n; i++) { const k = i / n, s = box(0.06, 2.6, 0.14, wood); s.position.set(lerp(x0, x1, k), y0 + 1.3, lerp(z0, z1, k)); s.rotation.y = -ang; scene.add(s); }
    for (const y of [y0 + 0.04, y0 + 2.62]) { const p = box(L, 0.08, 0.14, wood); p.position.set((x0 + x1) / 2, y, (z0 + z1) / 2); p.rotation.y = -ang; scene.add(p); } };
  for (const y0 of [0.3, 2.95]) { wall(-4.3, 3.3, 4.3, 3.3, y0); wall(-4.3, -3.3, 4.3, -3.3, y0); wall(-4.3, -3.3, -4.3, 3.3, y0); wall(4.3, -3.3, 4.3, 3.3, y0); }
  const deck = box(8.8, 0.12, 6.8, std('#C9A06A', 0.85)); deck.position.set(0, 2.95, 0); scene.add(deck);
  for (let i = 0; i < 6; i++) { const x = -4.2 + i * 1.68; const tr = new THREE.Group(); tr.position.set(x, 5.65, 0); scene.add(tr);
    for (const s of [-1, 1]) { const r = box(0.08, 0.14, 4.1, wood); r.position.set(0, 1.0, s * 1.75); r.rotation.x = s * 0.55; tr.add(r); }
    const tie = box(0.08, 0.12, 6.8, wood); tr.add(tie); }
  // scaffold on the right side
  const tube = std('#8E99A6', 0.4, { metalness: 0.6 }), plank = std('#C98A4B', 0.8);
  for (let i = 0; i < 4; i++) for (const x of [4.9, 5.9]) { const p = box(0.06, 6, 0.06, tube); p.position.set(x, 3, -2.6 + i * 1.75); scene.add(p); }
  for (const y of [2.0, 4.0, 5.9]) { const pl = box(1.1, 0.06, 5.6, plank); pl.position.set(5.4, y, 0); scene.add(pl); for (const x of [4.9, 5.9]) { const r = box(0.04, 0.04, 5.4, tube); r.position.set(x, y + 0.9, 0); scene.add(r); } }
  // tower crane
  const yel = std('#F2B705', 0.45, { metalness: 0.2 });
  const crane = new THREE.Group(); crane.position.set(-12, 0, -6); scene.add(crane);
  const base = box(3, 1, 3, conc); base.position.y = 0.5; crane.add(base);
  for (let i = 0; i < 12; i++) { const s = box(1.0, 1.5, 1.0, new THREE.MeshStandardMaterial({ color: '#F2B705', roughness: 0.45, wireframe: true })); s.position.y = 1.75 + i * 1.5; crane.add(s);
    for (const [x, z] of [[-0.5, -0.5], [0.5, -0.5], [-0.5, 0.5], [0.5, 0.5]]) { const c = box(0.1, 1.5, 0.1, yel); c.position.set(x, 1.75 + i * 1.5, z); crane.add(c); } }
  const top = new THREE.Group(); top.position.y = 19.2; crane.add(top);
  const jib = box(22, 0.7, 0.9, yel); jib.position.x = 9; top.add(jib); const cj = box(7, 0.7, 0.9, yel); cj.position.x = -4.5; top.add(cj);
  const cw = box(1.6, 1.4, 1.4, conc); cw.position.set(-7.4, -0.9, 0); top.add(cw); const cab = box(1.4, 1.3, 1.3, std('#FFFFFF', 0.4)); cab.position.set(0.9, -0.9, 0.9); top.add(cab);
  const apex = box(0.5, 3.5, 0.5, yel); apex.position.y = 1.9; top.add(apex);
  const trolley = new THREE.Group(); trolley.position.x = 13; top.add(trolley);
  const cable = box(0.04, 8, 0.04, std('#222', 0.5)); cable.position.y = -4.3; trolley.add(cable);
  const load = new THREE.Group(); load.position.y = -8.6; trolley.add(load);
  for (let i = 0; i < 4; i++) { const b = box(3.6, 0.22, 0.22, wood); b.position.set(0, -0.11 - (i % 2) * 0.22, -0.4 + Math.floor(i / 2) * 0.3 + (i % 2) * 0.15); load.add(b); }
  // props: cones, lumber pallets, dumpster, pickup
  const orange = std('#F26B1D', 0.6), white = std('#FFFFFF', 0.5);
  for (const [x, z] of [[-6, 6], [-3, 6.5], [0, 6.8], [3, 6.5], [6.5, 6]]) { const c = sh(new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.7, 20), orange)); c.position.set(x, 0.35, z); scene.add(c); const r = sh(new THREE.Mesh(new THREE.CylinderGeometry(0.135, 0.165, 0.1, 20), white)); r.position.set(x, 0.36, z); scene.add(r); }
  for (const [x, z] of [[-6.5, 2.5], [-7.2, -1]]) for (let j = 0; j < 6; j++) { const b = box(3.2, 0.16, 0.16, wood); b.position.set(x, 0.1 + Math.floor(j / 3) * 0.16, z + (j % 3) * 0.18); b.rotation.y = 1.57; scene.add(b); }
  const dump = box(3.6, 1.4, 1.8, std('#2F6B4F', 0.6)); dump.position.set(8.5, 0.7, 4.5); scene.add(dump);
  const truck = new THREE.Group(); truck.position.set(-8.5, 0, 9); truck.rotation.y = 0.3; scene.add(truck);
  const tb = box(4.6, 0.9, 1.9, std('#FFFFFF', 0.35, { metalness: 0.3 })); tb.position.y = 0.85; truck.add(tb); const tc = box(2.0, 0.85, 1.85, std('#FFFFFF', 0.35, { metalness: 0.3 })); tc.position.set(0.6, 1.7, 0); truck.add(tc);
  const glass = box(2.02, 0.5, 1.6, std('#2B3240', 0.15)); glass.position.set(0.6, 1.75, 0); truck.add(glass);
  for (const [x, z] of [[-1.5, 0.95], [1.5, 0.95], [-1.5, -0.95], [1.5, -0.95]]) { const w = sh(new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.3, 20), std('#1E1E1E', 0.8))); w.rotation.x = Math.PI / 2; w.position.set(x, 0.42, z); truck.add(w); }
  // rain
  const N = 1400, rm = new THREE.MeshBasicMaterial({ color: '#CFE3FF', transparent: true, opacity: 0.0 }), rain = new THREE.InstancedMesh(new THREE.BoxGeometry(0.03, 0.8, 0.03), rm, N), seeds = [];
  for (let i = 0; i < N; i++) seeds.push([(Math.random() - 0.5) * 40, Math.random() * 20, (Math.random() - 0.5) * 30 + 4]); scene.add(rain); const tmp = new THREE.Object3D();
  const L = lightRig(scene, { key: '#FFD9AE', keyI: 3.0, keyPos: [10, 14, 12], target: [0, 1, 0], rimCol: '#CFE0FF', rimI: 0.9, hemiI: 0.8, sky: '#DDEEFF', ground: '#8C7A60', shadowBox: 14 });
  const fill = new THREE.DirectionalLight('#FFF1E2', 0.6); fill.position.set(-8, 6, 10); scene.add(fill);
  return { scene, crane, top, load,
    update(t, { craneYaw = 0.6, rain: r = 0, mood = 0 } = {}) {
      top.rotation.y = craneYaw; load.rotation.y = Math.sin(t * 0.8) * 0.15;
      rm.opacity = 0.85 * r; rain.visible = r > 0.01;
      if (rain.visible) for (let i = 0; i < N; i++) { const [x, y, z] = seeds[i]; tmp.position.set(x, ((y - t * 14) % 20 + 20) % 20, z); tmp.rotation.z = 0.12; tmp.updateMatrix(); rain.setMatrixAt(i, tmp.matrix); }
      rain.instanceMatrix.needsUpdate = true;
      L.key.intensity = 3.0 - 2.0 * mood; fill.intensity = 0.6 - 0.25 * mood; L.key.color.set(mood > 0.5 ? '#AFC0DA' : '#FFD9AE'); scene.background = mood > 0.5 ? dusk : day;
    } };
}

/** a giant stylized dollar bill standing upright (2.6 m wide x 6 m tall), made of 4 cost slabs and a gold profit strip on top.
 *  set({ split 0..1 (slabs fly apart), dim 0..1 (cost slabs darken), profit 0..1 (gold strip height), glow, splitEach[4] }) */
export function dollar() {
  const c = document.createElement('canvas'); c.width = 520; c.height = 1200; const g = c.getContext('2d');
  g.fillStyle = '#CFE3C4'; g.fillRect(0, 0, 520, 1200); g.strokeStyle = '#2F6B4F'; g.lineWidth = 26; g.strokeRect(24, 24, 472, 1152); g.lineWidth = 6; g.strokeRect(60, 60, 400, 1080);
  g.fillStyle = '#2F6B4F'; g.font = '900 420px Inter, Arial'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText('$1', 260, 640);
  g.font = '900 64px Inter, Arial'; g.fillText('ONE', 260, 210); g.fillText('DOLLAR', 260, 1000);
  for (let i = 0; i < 18; i++) { g.globalAlpha = 0.12; g.beginPath(); g.arc(260, 640, 120 + i * 14, 0, 7); g.stroke(); } g.globalAlpha = 1;
  const base = new THREE.CanvasTexture(c); base.colorSpace = THREE.SRGBColorSpace;
  const grp = new THREE.Group(), Wb = 2.6, Hb = 6, slabs = [], fr = [0.235, 0.235, 0.235, 0.235]; let y0 = 0;
  fr.forEach((f, i) => { const t = base.clone(); t.needsUpdate = true; t.repeat.set(1, f); t.offset.set(0, y0 / Hb);
    const m = new THREE.MeshStandardMaterial({ map: t, roughness: 0.6 }); const s = sh(new THREE.Mesh(new THREE.BoxGeometry(Wb, Hb * f, 0.06), [std('#2F6B4F'), std('#2F6B4F'), std('#2F6B4F'), std('#2F6B4F'), m, std('#BFD6B4')]));
    s.userData.home = new THREE.Vector3(0, y0 + Hb * f / 2, 0); s.userData.mat = m; grp.add(s); slabs.push(s); y0 += Hb * f; });
  const gm = new THREE.MeshStandardMaterial({ color: '#FFC53D', emissive: '#FFB000', emissiveIntensity: 0.6, metalness: 0.5, roughness: 0.3 });
  const strip = sh(new THREE.Mesh(new THREE.BoxGeometry(Wb, Hb * 0.06, 0.09), gm)); grp.add(strip); const sy = y0 + Hb * 0.03;
  const OUT = [[-1.0, -0.9, 0.8], [1.0, -0.3, -0.3], [-1.0, 0.3, -0.4], [1.0, 0.9, 0.6]];
  return { group: grp, slabs, strip, top: new THREE.Vector3(0, sy, 0),
    set({ split = 0, dim = 0, profit = 1, glow = 0, splitEach = null } = {}) {
      slabs.forEach((s, i) => { const k = splitEach ? splitEach[i] : split; const o = OUT[i]; s.position.copy(s.userData.home).add(new THREE.Vector3(o[0] * k, o[1] * k, o[2] * k)); s.rotation.set(0, 0, (i % 2 ? -1 : 1) * 0.12 * k);
        s.userData.mat.color.setScalar(1 - 0.55 * dim); });
      strip.scale.y = Math.max(0.001, profit); strip.visible = profit > 0.01; strip.position.set(0, y0 + Hb * 0.06 * profit / 2, 0); gm.emissiveIntensity = 0.6 + glow;
      this.top.set(0, y0 + Hb * 0.06 * profit, 0); } };
}
