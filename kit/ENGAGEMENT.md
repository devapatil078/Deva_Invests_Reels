# deva invests: engagement playbook (read before writing every reel)

This is research on what is currently breaking out in faceless money/real-estate short video. Outlier scores are views as a multiple of the creator's usual views. The findings come from vidIQ outlier searches of YouTube Shorts, Instagram Reels and TikTok run on Nov 10, 2026. Refresh them every Sunday (see the bottom). Learn the patterns; never copy a creator's script, visuals or wording.

## What is working right now (evidence)
| Pattern | Examples (views, outlier ×) |
|---|---|
| **"Would you rather A or B?" split screen**: two options side by side, the numbers revealed step by step, a winner at the end | land vs house flip: 13.6M (1952×), 3.2M (680×), 755K (2454×); "which 10 acres would you buy" 690K (27×) |
| **Same start, different outcomes**: identical people or money, different choices, a data reveal | "Six friends. Same $80,000 salary." 1.5M (288×) |
| **"If you take $1…" process chain**: a character turns a small amount into a result, one step per beat | 6M (81×) |
| **Specific money number in the first frame** | "$44,000 a month…" 700K; "Dad buys stock at $250K. It grows to $12M." 6.3M (541×); "Our house in Italy was €78,000" 3.3M (248×) |
| **Ranking / countdown** ("I ranked 10 assets worst to best") | 1.3M (1415×) |
| **Contrarian one-liners** | "You don't get wealthy paying things off." 206K (40×); "I'd never go work for money." 139K (67×) |
| **A tiny character story explaining a concept** ("Timmy makes a coin in his bedroom…") | 914K (746×) |
| **Choice question that pulls comments** ("Who was in the wrong?", "Which would you buy?") | 840K (206×), 690K |
| **Looped endings**: the last line flows back into the first | most of the top Instagram outliers loop |
| **Sound effects in animated explainers** | almost every animated outlier uses them (ours do now) |

## Sunday refresh, Nov 22 2026 (vidIQ outlier search, Instagram + TikTok, last 30 days, creators under 200K followers; plus our own Metricool numbers)
Formats only; never copy anyone's script, visuals or wording. The CONTENT_STRATEGY_2026-11-12.md rules (standalone, no Parts, 25-40 s, one ask) still win.
| Pattern | Evidence |
|---|---|
| **"Same $X <one object>, 2-3 choices"**: one purchase, characters pick different paths, outcomes revealed step by step (fits our would-you-rather with kit characters) | 3D "Same $55,000 truck: cash, 7% loan or lease?" 1.1M (27.5x); "$1,500/mo for 30 years: rent vs own" 306K (25x, TikTok); "Same pay. Same house. One rents, one buys" 5.5M (9x, TikTok) |
| **One asset, upgraded step by step** until the money flips (3D house, each change adds a number) | 3D ADU explainer "You buy a house with a backyard and a two-car garage..." 584K (1,130x) |
| **"Your bank/agent hopes you never learn this" + a send ask aimed at a group** ("Send this to every homeowner") | text-on-screen mortgage tip 430K (1,567x) |
| **Everyday choice, expert answer** ("Credit card or debit card?") | 1.9M (141x) |
| **OUR data (Nov 15-22, Instagram):** hidden math on something the viewer already buys/owns wins: café $5 tap 924 views / 13.1 s / 37% skip; gift card $50 → $123: 365 / 16.4 s (best watch time) / 35% skip; $100 dinner 492; Costco 465. Investor-jargon and unpopular-truth hooks trail: Zestimate 124 / 60% skip; 1% rule 144 / 70% skip. The owner's own first-person deal post reached 521. |
Takeaways: keep "your $X <thing you buy/own>" hooks with a small surprising number; aim send asks at a named group ("someone about to sell their house", "every homeowner"); next would-you-rather: "same $X, two or three choices" with kit characters side by side.

## Rules for every reel
1. **Hook, 0-2 s:** the cover flashes first, then the first spoken line, at most 10 words, carrying a concrete number and tension. Use one of these patterns:
   - "Would you rather X or Y?"
   - "Same $X. Two very different results."
   - "You have $X. Watch it disappear."
   - "If you put $X into Y…"
   - a contrarian claim ("Paying off your house early can cost you $X.")
   No "In this video", no "Hey guys", no slow setup.
2. **Pick a format per reel and rotate it across the week.** Use each format at most twice in a row per series:
   - **A. Would you rather**: a split screen with two kit sets side by side (two houses, two shops), revealing the numbers step by step.
   - **B. Same start, different outcome**: two or three investors with the same money and different choices.
   - **C. Money chain**: one character turns $X into an outcome, one beat per step.
   - **D. Countdown**: rank 3-5 options worst to best and reveal #1 last.
   - **E. Breakdown**: watch $X disappear (Rehab Part 3 style).
   The topic still comes from SERIES.md; the format is how it is told. Example: Rentals "ONE" as format A: "Would you rather own 1 house free and clear, or 4 with mortgages?"
3. **Give the reel a character.** Use a named first-timer, the same name per series: Flipping = **Sam**, Rentals = **Maya**, Business = **Leo**. "Sam has $50,000 to fix this house." Viewers follow a person more readily than a concept, and the recurring name builds the series.
4. **Open a loop by 3 s and close it in the last 5 s** ("…and the last cost is the one that kills most flips").
5. **Add a mid-video comment bait at about 60-70% through:** a one-line choice question on screen and in the voice. Examples: "Would you take this deal? Yes or no in the comments." "Which one would you buy, A or B?" Keep the keyword CTA at the end; the question is extra and drives the comment count.
6. **Loop the ending.** The last spoken line should lead back into the first, so a rewatch feels seamless.
7. **Length:** 25-38 s of story plus an end card of 6-7 s at most (series_end_sfx.py is now shorter). If the script runs over 12 lines, cut it.
8. **Change something on screen at least every 2 s:** a new shot, a label pop, a counter ticking or a camera push. A reveal number gets its own shot, its impact sound and a yellow caption.
9. **Big numbers only.** Show at most 3 numbers on screen at once, rounded ($27K, not $27,350), each sourced in script.json.
10. **Captions** are short: a few words each, with key numbers and stakes in yellow (already the default).
11. **Cover text** = the hook in at most 7 words (make_cover.py, text in the middle, big PART badge).

## Weekly loop: learn from our own numbers
- **Every night, before writing:** pull Metricool analytics for the reels published 2-7 days ago, using getAnalyticsAvailableMetrics then getAnalyticsDataByMetrics on Instagram, TikTok and YouTube. Get views, likes, comments, shares, saves, and watch time or retention if available. Log them in the state file under "performance". Note which hook pattern and format each reel used, which ones lead on views per follower, and which on comments. Use more of what wins. When a series' last two reels both trail, switch its next reel to a format it hasn't used.
- **Every Sunday night:** refresh the research. Run 2-3 vidIQ outlier searches (vidiq_instagram_tiktok_outlier_search with embeddingType concept and format, and vidiq_outliers with contentType short) on flipping, rentals and small-business money. Credits are limited, so if vidIQ says there aren't enough credits, use web search instead. Add new patterns with evidence to this file (kit/ENGAGEMENT.md in the GitHub repo), update its date, commit and push. Mention the best new idea in the nightly summary.
