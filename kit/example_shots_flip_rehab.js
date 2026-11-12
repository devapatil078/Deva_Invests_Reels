// WHERE DOES THE REHAB MONEY GO? : Deep Dive 3D, flipping series Part 3.  (REFERENCE EXAMPLE of a finished shots.js)
// A $50K repair budget shown as 20 gold coins ($2.5K each). Each repair takes its coins; over-budget coins come in red.
// Real world (the fixer-upper renovating part by part) ↔ studio coin piles ↔ x-ray walls hiding surprises.
// Costs: Angi 2026 averages (kitchen ~$27K, roof ~$9.6K, bathroom $6.6-17.6K, flooring ~$5K, paint ~$2K).
import * as THREE from 'three';
import { ctx, W, H, clamp, lerp, seg, eo, eio, eob } from './core/lib.js';
import { L, Wd, T } from './core/timing.js';
import { camera } from './core/engine.js';
import { Human } from './core/human.js';
import * as M from './core/money.js';
import * as FX from './core/flip.js';
import { label, pill } from './core/look2d.js';

const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
const lerpV = (a, b, k) => a.clone().lerp(b, k);
function screen(p, cam) { const v = p.clone().project(cam); return [(v.x + 1) / 2 * W, (1 - v.y) / 2 * H]; }
const GREEN = '#5BE38A', REDC = '#FF6B6B', GOLD = '#FFD43B';

export function buildShots(E) {
  const S = [], CUES = [], add = (o) => (S.push(o), o), cue = (t, type, o = {}) => CUES.push({ t: +t.toFixed(3), type, ...o });
  const cut = (i) => (i === 0 ? 0 : L(i) - 0.08);
  const cam = camera(40);
  const KLOOK = { aperture: 0.0012, maxblur: 0.008, bloom: 0.2 }, XLOOK = { aperture: 0.0006, bloom: 0.45, bloomThreshold: 0.7, vignette: 0.45 }, SLOOK = { aperture: 0.0015, maxblur: 0.008, bloom: 0.35, bloomThreshold: 0.6, vignette: 0.5 };
  const look = (scene, target, base, extra = {}) => E.render(scene, cam, { ...base, focus: cam.position.distanceTo(target), ...extra });

  // ── the world ──────────────────────────────────────────────────────────
  const ST = M.street(E); ST.scene.remove(ST.house.group); const FH = FX.fixer(); ST.scene.add(FH.group); ST.board.visible = false;
  const buyer = new Human({ shirt: '#7A4E8C', pants: '#2B3550', skin: '#C68A62', hair: '#2A1A10' }); ST.scene.add(buyer.group);
  const SA = M.studio(E), redM = FX.redCoin(), blueM = new THREE.MeshStandardMaterial({ color: '#4F8BFF', metalness: 0.6, roughness: 0.3, emissive: '#0A1A4A', emissiveIntensity: 0.4 });
  const budget = M.coins(20); budget.group.position.set(0, 0, -0.6); budget.group.scale.setScalar(1.15); SA.scene.add(budget.group);
  const buffer = M.coins(4); buffer.group.children.forEach((c) => (c.material = blueM)); buffer.group.position.set(0, 20 * 0.08 * 1.15, -0.6); buffer.group.scale.setScalar(1.15); SA.scene.add(buffer.group);
  const P = [['KITCHEN', '$27K', 11, 'kitchen', 1], ['ROOF', '$10K', 4, 'roof', 2], ['BATHROOM', '$12K', 5, 'bathroom', 3], ['FLOORS', '$5K', 2, 'floors', 4], ['PAINT', '$2K', 1, 'paint', 4]];
  const POS = [[-1.9, 0.3], [-1.0, 1.1], [0, 1.45], [1.0, 1.1], [1.9, 0.3]];
  const piles = P.map((p, i) => { const c = M.coins(12); if (i >= 3) c.group.children.forEach((m) => (m.material = redM)); c.group.position.set(POS[i][0], 0, POS[i][1]); c.group.scale.setScalar(1.1); SA.scene.add(c.group); return c; });
  const PT = P.map(([, , , w, li]) => Wd(w, li));            // absolute time each repair is said
  const AMT = [27, 10, 12, 5, 2];
  const spentK = (t) => PT.map((x) => eo(seg(t, x - 0.1, x + 0.7)));
  const left = (t) => 50 - spentK(t).reduce((s, k, i) => s + k * AMT[i], 0);
  const coinsTo = (t) => { const k = spentK(t); piles.forEach((p, i) => p.set(Math.round(P[i][2] * k[i]))); budget.set(Math.max(0, Math.round(20 - (11 * k[0] + 4 * k[1] + 5 * k[2])))); };
  // budget meter (top of frame, every money shot)
  function meter(t, sc = 1) {
    if (sc <= 0) return; const l = left(t), f = clamp(l / 50); ctx.save(); ctx.globalAlpha = sc; ctx.translate(540, 235);
    ctx.fillStyle = 'rgba(12,14,20,0.82)'; ctx.beginPath(); ctx.roundRect(-330, -52, 660, 104, 52); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,0.15)'; ctx.beginPath(); ctx.roundRect(-300, 6, 600, 24, 12); ctx.fill();
    ctx.fillStyle = l > 0 ? GOLD : REDC; ctx.beginPath(); ctx.roundRect(-300, 6, Math.max(24, 600 * f), 24, 12); ctx.fill();
    ctx.font = '900 38px Inter'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = l > 0 ? '#FFFFFF' : REDC;
    ctx.fillText(l > 0 ? `BUDGET LEFT: $${Math.round(l)}K` : `OVER BUDGET: $${Math.round(-l)}K`, 0, -22); ctx.restore();
  }
  const pileTags = (t, cam, only = null) => P.forEach(([n, v], i) => { if (only && !only.includes(i)) return; const [x, y] = screen(piles[i].group.position.clone().add(V3(0, 1.25, 0)), cam);
    const k = eob(seg(t, PT[i], PT[i] + 0.3)); if (k <= 0) return; pill(`${n} ${v}`, x, y, k, i >= 3 ? REDC : GOLD, 'rgba(12,14,20,0.88)', 40); });
  // hidden surprises inside the x-ray walls
  const X = M.xrayHouse(E); X.you.visible = X.bank.visible = false; X.fill = () => {};
  const bad = new THREE.MeshStandardMaterial({ color: '#FF4A4A', emissive: '#FF2A2A', emissiveIntensity: 0.9, roughness: 0.4 });
  const hid = new THREE.Group(); X.house.group.add(hid);
  [[[-2.2, 0.2, 1.6], [-2.2, 2.7, 1.6]], [[-2.2, 2.6, 1.6], [1.5, 2.6, 1.6]], [[1.8, 0.2, -1.6], [1.8, 2.4, -1.6]], [[-1.0, 0.25, 0.0], [2.2, 0.25, 0.0]]].forEach(([a, b]) => {
    const A = V3(...a), B = V3(...b), len = A.distanceTo(B), c = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, len, 12), bad); c.position.copy(A).add(B).multiplyScalar(0.5);
    c.quaternion.setFromUnitVectors(V3(0, 1, 0), B.clone().sub(A).normalize()); hid.add(c); });
  const mold = new THREE.Mesh(new THREE.SphereGeometry(0.5, 20, 14), new THREE.MeshStandardMaterial({ color: '#5A8F3A', emissive: '#2F6B1F', emissiveIntensity: 0.8, transparent: true, opacity: 0.85 })); mold.scale.set(1.3, 0.6, 0.3); mold.position.set(0.8, 1.2, 1.75); hid.add(mold);
  const HOUSE = V3(0, 1.8, 0);
  const street = (o = {}) => { FH.parts2(o); ST.mood(o.mood || 0); buyer.group.visible = false; };

  // 1 · HOOK: rundown house; "you have $50K… watch it disappear"
  { const st = cut(0), td = Wd('disappears', 0) - st;
    add({ id: 'S01', at: st, note: 'rundown house push-in, BUDGET $50,000 meter appears', draw(lt, d, t, blit) {
      street({});
      cam.position.copy(lerpV(V3(-6, 1.5, 15), V3(-3.5, 1.8, 10.5), eio(lt / d))); cam.lookAt(0, 2.3, 1.5); look(ST.scene, HOUSE, KLOOK); blit();
      pill('$50,000 TO FIX IT', 540, 400, eob(seg(lt, 0.4, 0.7)), GOLD, 'rgba(12,14,20,0.88)', 76); meter(t, eo(seg(lt, td - 0.3, td)));
    } });
    cue(st + 0.05, 'whoosh'); cue(st + 0.4, 'pop'); }

  // 2 · a new kitchen, ~$27K: studio, 11 coins leave the budget stack for the KITCHEN pile
  { const st = cut(1);
    add({ id: 'S02', at: st, note: 'studio: 11 of 20 coins move to the kitchen pile', draw(lt, d, t, blit) {
      coinsTo(t); buffer.set(0);
      cam.position.copy(lerpV(V3(-3.4, 4.4, 10), V3(-2.4, 4.0, 9), eio(lt / d))); cam.lookAt(-0.5, -0.4, 0.4); look(SA.scene, V3(-0.9, 0.8, 0.5), SLOOK); blit();
      pileTags(t, cam, [0]); meter(t);
    } });
    cue(st, 'whoosh'); for (let i = 0; i < 6; i++) cue(PT[0] - 0.05 + i * 0.12, 'pop', { gain: 0.22 }); }

  // 3 · a new roof, ~$10K: outside, the roof re-shingles as the camera cranes up
  { const st = cut(2);
    add({ id: 'S03', at: st, note: 'street crane up: the roof renovates; ROOF $10K', draw(lt, d, t, blit) {
      street({ roof: eio(seg(t, PT[1] - 0.2, PT[1] + 0.7)) });
      cam.position.copy(lerpV(V3(5, 2.5, 11), V3(4.5, 6.5, 10), eio(lt / d))); cam.lookAt(0, 3.6, 0); look(ST.scene, V3(0, 3.5, 0), KLOOK); blit();
      pill('ROOF $10K', 540, 420, eob(seg(t, PT[1], PT[1] + 0.3)), GOLD, 'rgba(12,14,20,0.88)', 66); meter(t);
    } });
    cue(PT[1], 'thud', { gain: 0.5 }); }

  // 4 · one bathroom, ~$12K: studio, the budget stack empties
  { const st = cut(3);
    add({ id: 'S04', at: st, note: 'studio: bathroom pile takes the last coins, budget stack empty', draw(lt, d, t, blit) {
      coinsTo(t); buffer.set(0);
      cam.position.copy(lerpV(V3(0.6, 4.4, 10.5), V3(1.6, 4.6, 10.5), eio(lt / d))); cam.lookAt(0, -0.4, 0.4); look(SA.scene, V3(0, 0.8, 0.8), SLOOK); blit();
      pileTags(t, cam, [0, 1, 2]); meter(t);
    } });
    for (let i = 0; i < 3; i++) cue(PT[2] - 0.05 + i * 0.15, 'pop', { gain: 0.22 }); }

  // 5 · floors $5K, paint $2K: outside, the walls get repainted; the meter goes red
  { const st = cut(4);
    add({ id: 'S05', at: st, note: 'street: walls repaint; FLOORS $5K + PAINT $2K; meter turns red', draw(lt, d, t, blit) {
      street({ roof: 1, wall: eio(seg(t, PT[4] - 0.2, PT[4] + 0.7)) });
      const a = lerp(-0.35, -0.05, eio(lt / d)); cam.position.set(Math.sin(a) * 13, 1.8, 1 + Math.cos(a) * 13); cam.lookAt(0, 2.0, 1); look(ST.scene, HOUSE, KLOOK); blit();
      pill('FLOORS $5K', 540, 420, eob(seg(t, PT[3], PT[3] + 0.3)), REDC, 'rgba(12,14,20,0.88)', 60);
      pill('PAINT $2K', 540, 540, eob(seg(t, PT[4], PT[4] + 0.3)), REDC, 'rgba(12,14,20,0.88)', 60); meter(t);
    } });
    cue(PT[3], 'pop'); cue(PT[4], 'pop'); }

  // 6 · that's $56K, already over budget: studio pull back, all piles, red coins
  { const st = cut(5), to = Wd('over', 5) - st;
    add({ id: 'S06', at: st, note: 'studio pull back over all piles: $56,000 SPENT, OVER BUDGET', draw(lt, d, t, blit) {
      coinsTo(t); buffer.set(0);
      cam.position.copy(lerpV(V3(0, 5.2, 11.5), V3(0, 7.0, 14.5), eio(lt / d))); cam.lookAt(0, -0.5, 0.3); look(SA.scene, V3(0, 0.6, 0.5), SLOOK); blit();
      pileTags(99, cam); pill('$56,000 SPENT', 540, 420, eob(seg(lt, 0.2, 0.5)), '#FFFFFF', 'rgba(12,14,20,0.88)', 70); meter(t);
    } });
    cue(st + 0.2, 'pop'); cue(st + to, 'alarm', { dur: 0.8, gain: 0.4 }); }

  // 7 · and you haven't opened a single wall yet: x-ray walls reveal red pipes, wires and a mould patch
  { const st = cut(6), tw = Wd('wall', 6) - st;
    add({ id: 'S07', at: st, note: 'x-ray house: hidden red pipes, wires, mould glow inside the walls', draw(lt, d, t, blit) {
      const k = eo(seg(lt, tw - 0.5, tw + 0.3)); hid.scale.setScalar(Math.max(0.001, k)); bad.emissiveIntensity = 0.5 + 0.6 * Math.sin(lt * 8) ** 2;
      const a = lerp(0.7, 0.35, eio(lt / d)); cam.position.set(Math.sin(a) * 12.5, 2.8, Math.cos(a) * 12.5); cam.lookAt(0, 1.6, 0); look(X.scene, HOUSE, XLOOK); blit();
      pill('HIDDEN SURPRISES', 540, 420, eob(seg(lt, tw, tw + 0.3)), REDC, 'rgba(12,14,20,0.9)', 70);
    } });
    cue(st, 'whoosh'); cue(st + tw, 'heartbeat'); cue(st + tw + 0.5, 'heartbeat'); }

  // 8 · smart flippers fix what buyers pay for: a buyer walks the sidewalk and stops to look
  { const st = cut(7), tb = Wd('buyers', 7) - st;
    add({ id: 'S08', at: st, note: 'street: a buyer walks up and stops to look; WHAT BUYERS PAY FOR', draw(lt, d, t, blit) {
      street({}); buyer.group.visible = true; const wk = seg(lt, 0, 2.2); buyer.group.position.set(lerp(-7, -1.2, wk), 0, 5.8); buyer.group.rotation.y = wk < 1 ? Math.PI / 2 : lerp(Math.PI / 2, Math.PI, seg(lt, 2.2, 2.7));
      if (wk < 1) buyer.walk(lt * 7, 1); else buyer.pose({ head: [-10, 0, 0] });
      cam.position.copy(lerpV(V3(-4, 1.5, 12.5), V3(-2.5, 1.6, 11), eio(lt / d))); cam.lookAt(-1.2, 1.6, 3); look(ST.scene, V3(-1.2, 1.5, 5.8), KLOOK); blit();
      pill('FIX WHAT BUYERS PAY FOR', 540, 330, eob(seg(lt, tb - 0.2, tb + 0.1)), GREEN, 'rgba(12,14,20,0.88)', 58);
    } });
    cue(st + tb, 'pop'); }

  // 9 · paint, floors and a kitchen refresh: the house gets the smart makeover, a checklist stacks up
  { const st = cut(8), tw = ['paint', 'floors', 'refresh'].map((w) => Wd(w, 8) - st);
    add({ id: 'S09', at: st, note: 'street orbit: paint, door, windows, yard renovate; checklist PAINT / FLOORS / KITCHEN REFRESH', draw(lt, d, t, blit) {
      const k = tw.map((x) => eio(seg(lt, x - 0.2, x + 0.6))); street({ wall: k[0], door: k[1], win: k[2], yard: k[2] });
      const a = lerp(0.6, 0.15, eio(lt / d)); cam.position.set(Math.sin(a) * 14, 2.4, 1 + Math.cos(a) * 14); cam.lookAt(0, 2.1, 1); look(ST.scene, HOUSE, KLOOK); blit();
      ['+ PAINT', '+ FLOORS', '+ KITCHEN REFRESH'].forEach((s, i) => pill(s, 540, 300 + i * 110, eob(seg(lt, tw[i] - 0.1, tw[i] + 0.2)), GREEN, 'rgba(12,14,20,0.88)', 56));
      label('NOT A NEW KITCHEN', 760, 900, ...screen(V3(1.5, 1.6, 2.1), cam), eob(seg(lt, tw[2] + 0.5, tw[2] + 0.8)));
    } });
    tw.forEach((x) => cue(st + x, 'pop', { gain: 0.5 })); }

  // 10 · add 10-20% extra for surprises: studio, blue buffer coins stack on the full budget
  { const st = cut(9), tt = Wd('ten', 9) - st, ta = Wd('always', 9) - st;
    add({ id: 'S10', at: st, note: 'studio: a fresh 20-coin budget gets 2-4 blue buffer coins on top', draw(lt, d, t, blit) {
      piles.forEach((p) => p.set(0)); budget.set(20); buffer.set(Math.round(lerp(0, 2, eo(seg(lt, tt - 0.1, tt + 0.3))) + 2 * eo(seg(lt, tt + 0.5, tt + 0.9))));
      const a = lerp(-0.2, 0.25, eio(lt / d)); cam.position.set(Math.sin(a) * 5.5, 2.2, -0.6 + Math.cos(a) * 5.5); cam.lookAt(0, 1.3, -0.6); look(SA.scene, V3(0, 1.3, -0.6), SLOOK); blit();
      label('+10–20% FOR SURPRISES', 760, 560, ...screen(V3(0.3, 20 * 0.08 * 1.15 + 0.2, -0.6), cam), eob(seg(lt, tt + 0.3, tt + 0.6)));
      pill('THERE ARE ALWAYS SURPRISES', 540, 330, eob(seg(lt, ta - 0.2, ta + 0.1)), GOLD, 'rgba(12,14,20,0.88)', 52);
    } });
    cue(st + tt, 'pop'); cue(st + tt + 0.6, 'pop'); }

  // 11 · money isn't the only thing a flip eats: every month costs you too (teases Part 4)
  { const st = cut(10), tm = Wd('month', 10) - st;
    add({ id: 'S11', at: st, note: 'street at dusk, half-renovated house, month counter ticking', draw(lt, d, t, blit) {
      street({ wall: 1, door: 1, win: 1, yard: 0.6, mood: eio(seg(lt, 0, 1.5)) });
      cam.position.copy(lerpV(V3(3, 1.6, 11), V3(5, 3.5, 15), eio(lt / d))); cam.lookAt(0, 2.0, 1); look(ST.scene, HOUSE, KLOOK); blit();
      if (lt > tm - 0.2) { const m = 1 + Math.floor(seg(lt, tm, d) * 6); pill(`MONTH ${m}`, 540, 330, eob(seg(lt, tm - 0.2, tm + 0.1)), '#FFFFFF', 'rgba(12,14,20,0.88)', 80);
        pill('EVERY MONTH COSTS YOU', 540, 460, eob(seg(lt, tm + 0.2, tm + 0.5)), REDC, 'rgba(12,14,20,0.88)', 56); }
    } });
    cue(st + tm, 'heartbeat'); }

  return { shots: S, cues: CUES };
}
