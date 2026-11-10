# deva invests sound effects (use in every new Reel)

The channel has its own pack of 15 original sound effects, made in code by `make_sfx.py`. No downloads, no licence and no credit needed. `sfx/credits.json` records this.

## Setup (once per machine)
- If `~/faceless-shorts/kit/sfx/` is missing, run `python3 ~/faceless-shorts/kit/make_sfx.py ~/faceless-shorts/kit/sfx`. The same seed rebuilds the same files.
- After `new_video.sh` creates a project, run `cp ~/faceless-shorts/kit/mix_sfx.py <project>/tools/mix.py`. This mixer uses the pack automatically.
- Use `series_end_sfx.py` instead of `series_end.py`. It has the same arguments and adds the end-card sounds: whoosh in, pops on the pills, a click on the keyword pill, and a chime when the ask lands.

## The pack (3 variants each, rotated automatically so repeats don't sound identical)
| cue type in shots.js | sound | use it for |
|---|---|---|
| `whoosh` (also `slide`, `zip`) | whoosh_1-3 (0.45 / 0.65 / 0.95 s) | every scene cut, camera swoops. Pass `{dur: 0.95}` for a big scene change. |
| `pop` (also `plop`, `boing`) | pop_1-3 | every card, pill, label or number badge appearing |
| `click` (also `tock`) | click_1-3 | UI moments: a bar/meter ticking up, a checkbox, a counter step, a screen() tap, a button |
| `impact` (also `thud`, `slam`) | impact_1-3 | the ONE big reveal per Reel (the profit, the loss, the shocking total). Max 2 per Reel. |
| `chime` (also `sparkle`) | chime_1-3 | a good-news or result moment (a deal passes, money lands); the end card adds its own |

Options on any cue: `{gain: 0.2-1.0}` makes it quieter, `{var: 0|1|2}` forces a variant, and `{pan: -1..1}` places it left or right.

## Placement rules
- Put `cue(st, 'whoosh')` at the start of every shot that changes scene. A plain camera move in the same scene gets none.
- Every pill or label gets `cue(t, 'pop')` at the moment it pops in. For a quick run of items (bars, coins), use `gain: 0.22` and space them 0.12-0.15 s apart.
- Use `cue(t, 'click')` for numbers ticking or interface taps, at 2-6 per Reel, not on every word.
- Use exactly one `cue(t, 'impact')` on the key word of the reveal line, `Wd('word', line)`, about 0.05 s early.
- Use 0-2 `chime` per Reel.
- Keep the voice on top. The mixer sets the levels; don't raise `gain` above 1.
- After `node tools/capture.mjs cues` and `tools/mix.py`, the line "sound pack: .../kit/sfx" must print. If it says "none", the pack is missing, so run the setup above.
