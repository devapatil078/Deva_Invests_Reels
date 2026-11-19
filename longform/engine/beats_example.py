"""Beat sheet EXAMPLE (start of video 1). Copy to beats.py and write the whole sheet for the new video.
For each narration section: list of (anchor phrase or None, scene fn name, kwargs). Anchor = exact phrase in that section's
narration where the beat starts (None = start of the section). Chapter cards play in the gap before a section."""
from engine import INK, RED, GOLD, TEAL, MUTED

GAPS = [0.0, 1.2, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 2.6, 1.4]   # silence before each section (10 sections)
CHAPTERS = {2: (1, "THE MACHINE"), 3: (2, "THE BRANCH"), 4: (3, "THE MONEY MACHINE"), 5: (4, "THE WHISTLEBLOWER"),
            6: (5, "EVERYONE SAW A PIECE"), 7: (6, "THE RECKONING"), 8: ("CHAPTER 7", "THE REAL NUMBER")}
TAIL = 16.0   # end-screen time after the last word

K = lambda **kw: kw
SECTIONS = [
 # 0 HOOK (video-1 specific scenes like cash_counter / one_branch were custom functions in its scenes.py)
 [(None, "big_number", K(value="€200B", label="through one bank branch", color=RED)),
  ("Between 2007 and 2015", "kinetic", K(lines=[("2007–2015", "Between 2007", {"size": 70, "color": MUTED}),
                                               ("€200,000,000,000", "200 billion", {"size": 130, "w": "black", "color": RED}),
                                               ("≈ 10× Estonia's entire economy", "ten times", {"size": 64})]))],
 # 1 INTRO
 [(None, "title_card", K(title="THE ECONOMICS OF MONEY LAUNDERING", sub="Danske Bank · Estonia · 2007–2015")),
  ("But this isn't really", "kinetic", K(lines=[("Not a crime story.", "But this isn't", {"size": 100, "color": MUTED, "w": "black"}),
                                               ("It's a business story", "It's a business story", {"size": 100, "w": "black"})]))],
 # 2 ... 8 chapters: mix bullets, bar_chart, split_view, tl_scene, cal_scene, filing, quote, maps and your own scenes
 # 9 CLOSE: end with (anchor_of_last_line, "endscreen", K(next_title="THE NEXT\nVIDEO TITLE"))
]
