# deva invests: nightly run instructions (master copy)

This file is the owner's standing instructions for the three nightly scheduled tasks (FLIPPING, RENTALS, BUSINESS). Each task's own prompt names its series and slots and tells you to follow this file. Where this file and RUNBOOK_*.md / PLAYBOOK.md in Dropbox differ, THIS FILE WINS (it is newer: Nov 11, 2026, morning). Only the owner's Claude sessions edit this file; a nightly run never rewrites it.

You are producing the next 3 Reels of ONE series (the series named in your task prompt) for the faceless investing channel "deva invests" (@deva_invests on Instagram, its Facebook page, YouTube, TikTok and Threads), then uploading and scheduling them yourself in Metricool. The owner (devarshipatil88@gmail.com) posts 9 Reels a day in three back-to-back blocks of 3 consecutive parts of one series; three separate runs each handle one block. The runs are spread out so each has its own usage window: FLIPPING ~9:40 PM, RENTALS ~2:50 AM, BUSINESS ~8:05 AM (America/Toronto). Work unattended, decide sensibly, and report at the end. The owner should NOT need to upload anything. The owner wants the reels to be the best in the niche: so good that people open the profile and watch every reel.

## USAGE (added Nov 11 after a run died at the plan's usage limit and lost its work)
- Work ONE REEL AT A TIME, earliest part first: write, render, cover, push to GitHub, schedule in Metricool, save the state file. Only then start the next reel. A run that is cut off must leave every finished reel already scheduled and recorded.
- Do not redo work that exists: use a saved script (<Series>_Part<N>_script.json in Dropbox, or the captions saved in the state file) instead of researching again; skip any setup step whose files are already in the repo's kit/.
- Keep it lean: no extra candidate renders, no re-renders for small polish, no long explorations. One contact-sheet check and one listen-check per reel.

## ANIMATION STYLE (owner's request, Nov 10)
Keep the animation EXACTLY the same as the reels already posted (Flipping, Rentals and Business Parts 1-3 made Nov 9-10): the same Deep Dive 3D look, the same kit sets and props, the same series characters (Sam/Maya/Leo) and their designs, the same colors, lighting, camera moves, caption style, cover design and end cards. Do NOT try new animation styles, new characters, new looks or new visual effects. "More engaging" changes are allowed only in the script, hook, story, format, pacing and sound, never in the visual style. If a scene needs something the kit does not have, build it from the existing kit pieces in the same style.

## SOUND AND VOICE (owner's requests, Nov 11)
- ESSENTIAL SOUNDS ONLY (RUNBOOK section 0): the voice, ONE impact on the big reveal, and the end card's one soft chime. NO music bed, NO whoosh, no pops, no clicks, no other effects. apply_kit_patches.py enforces this in the mixer; set "music": "none" in script.json.
- The narration must sound like a real professional presenter: pauses at the right moments and weight on the important word. Give every script line a directed "say" field and make the narration with kit/pro_voice.py exactly as the RUNBOOK (section 5) says; never use plain piper_voice.py for a new reel, and do not run words.py after pro_voice.py.
- Explain it like you are talking to a 10-year-old: everyday words, one idea per line, short sentences, round numbers.

## BINGE-WATCH RULES (owner's request, Nov 10: viewers should want to open the profile and watch all the reels)
- Each block of 3 parts is one mini-story with the series character and rising stakes: the 1st part sets up a real problem with a concrete number, the 2nd part is the twist or the costly mistake, the 3rd part is the payoff (the real number, the lesson) and opens the next question for tomorrow.
- Every part fully pays off its own hook (it must satisfy someone who sees only that reel), AND ends on one specific unanswered question that the next part answers. Never end on a vague "stay tuned".
- Spoken end-card tease: for the 1st and 2nd part of a block, "Part N+1 is the next video on my page: <the question>"; for the 3rd part, "Part N+1 tomorrow: <the question>. Parts 1 to N are on my page."
- First line of every caption on every network = the hook. Second line = "🎬 <Series> series · Part N · start from Part 1 on my page".
- Watch-time: a concrete number on screen in the first second after the cover, a pattern interrupt (new scene, a number ticking, a reveal) at least every 2 s, a "pause and guess" beat at ~60-70% (no comment ask there), and an ending that loops back into the first line where possible.
- END QUESTION (owner's request, Nov 10): every reel ends with ONE question to viewers that they answer in the comments. It must come from THIS reel's exact story, numbers or decision (e.g. "Sam can offer $160K or walk away. What would you do?" or "Maya's rental clears $212 a month. Would you buy it: yes or no?"), never generic ("what do you think?", "agree?"), never about another topic, and answerable in one word or one number. It is the last story line: spoken by the narrator and shown on screen, right before the end card. Use the same question as the last line of the caption before the keyword line. This replaces the mid-video comment question in ENGAGEMENT.md.
- Never repeat a hook pattern or format twice in a row within a series; check the last 6 reels of the series in the state file.
- Quality bar before scheduling: look at the contact sheet and listen to the narration; if a reel is not something a beginner would rewatch or send to a friend, fix the script and re-render rather than ship it.

## TRIPLE HOOK (owner's request, Nov 10; modeled on @kallawaymarketing's "Triple Hook Method" reel the owner sent)
Every reel's first ~5 seconds after the cover are three beats, in this order:
1. CONTEXT: in the very first line the viewer instantly knows what this reel is about (the character, the deal, the money), with one concrete number. Say it, show it as on-screen text and show it in the scene AT THE SAME TIME. Never delay the context.
2. LEAN: make the viewer lean in: name a pain point the audience has, or show something surprising, so they quietly take one side ("sounds like easy money", "most people would buy this").
3. CONTRARIAN SNAPBACK: snap them back to the opposite of what they just assumed, with the real number ("...but Sam actually lost $9,000"). The snapback opens the loop the rest of the reel closes.

Shape (format only; real numbers always come from your research, never from these examples): "This house sold for $60K more than Sam paid. / Sounds like an easy win, right? / Sam actually lost money." Each beat is one short line (max 10 words; beat 1 must contain the number). Write 3 candidate triple hooks per reel, pick the one with the clearest context and the biggest snapback, and record all 3 in the state file. The cover's hook text comes from beat 1 + beat 3.

## WATCH-TIME STRUCTURE (owner's request, Nov 11; from the @robertmckeaveney reel the owner sent. This closes the RUNBOOK's "open owner request" about him: do not spend vidIQ credits on it.)
- Average watch time is the number that matters most. Every choice in the script serves it.
- Every reel is HOOK -> BUILDUP -> PAYOFF. The hook raises ONE question (the snapback does this). The buildup adds one new fact and one new visual per line and never answers the question early. The PAYOFF answers the hook's question and comes LAST, right before the END QUESTION. Never give the answer in the middle.
- Each reel gives at least two of the 3 E's: Educational (a real number or rule they can use), Emotional (a win or a loss for Sam/Maya/Leo), Entertaining (a surprise or a guess).
- Use formats that already worked on this channel (see "performance" in the state file) and judge each reel against the channel's OWN average, not against big accounts.
- Never copy his or anyone's scripts or visuals.

## FREE TOOLKITS (owner's request, Nov 10: no random tools; only legit, researched tools)
Do NOT build any new .xlsx, calculator or tool, and never mention or recommend a tool that is not in these kits. Each series has ONE fixed free toolkit and ONE comment keyword, used in every reel of that series:
- FLIPPING -> keyword FLIP -> "Flip Starter Toolkit" (7 free, trusted tools: Zillow sold homes filter, Redfin sold homes, DealCheck, Angi cost guides, county assessor/recorder records, ATTOM Home Flipping Report, Freddie Mac mortgage rates PMMS). Link: https://drive.google.com/file/d/1N22bPf3KHEPHyJ0c7VCWNVoj_yATxgaz/view
- RENTALS -> keyword RENT -> "Rental Starter Toolkit" (HUD Fair Market Rents, Zillow Rentals, Rentometer, DealCheck, Freddie Mac PMMS, Stessa, CMHC rental market data for Canada). Link: https://drive.google.com/file/d/1qx9waEZnuga6oOWMoHut2B-6u7AojmOS/view
- BUSINESS -> keyword BIZ -> "Business Starter Toolkit" (SBA startup costs + break-even calculator, SCORE Startup Expenses template, SCORE Break-Even template, SCORE free mentor, BLS business survival data, Wave Starter plan, BDC templates for Canada). Link: https://drive.google.com/file/d/1G8CODAgU1FLkkepxIzPk2udeKVAQuJwE/view

Ignore the per-part "Keyword" and "Free tool" columns in SERIES.md; they are retired. In each reel, pick the ONE tool from its series kit that best helps with that reel's topic and name it in the caption ("Inside: <tool> to <job>"); the narration may mention it once in a few words. Posts already scheduled before Nov 11 keep their old keywords (OFFER, BID, REHAB, etc.); do not edit them.

## DAILY SCHEDULE (America/Toronto), 9 Reels a day, parts always in order
- FLIPPING block: 8:00 AM, 9:00 AM, 10:00 AM (parts n, n+1, n+2)
- RENTALS block: 12:30 PM, 1:30 PM, 2:30 PM
- BUSINESS block: 7:00 PM, 8:00 PM, 9:00 PM

TARGET DAY: if this run starts between noon and midnight local time, the target day is tomorrow's date; if it starts between midnight and noon, the target day is today's date. Always fill the EARLIEST free future slots of your series first (a slot is free if no post of your series is scheduled in it and it is at least 45 minutes away).

## 0. SET UP THE MACHINE (every run starts on a fresh cloud machine)
Read the newest RUNBOOK_YYYY-MM-DD.md in Dropbox folder "/deva invests/kit" for the exact commands and known pitfalls (remember: this file wins where they differ).

(a) REPO WITH PUSH ACCESS. The task prompt already told you how (add_repo with access "push", then clone, then register_repo_root). This was tested on Nov 11 and works. There is NO repository setting in the task editor, so NEVER ask the owner to "add the repo to the task"; ignore RUNBOOK sections 1 and 6 where they say so. After cloning: `git pull`, then check `git push --dry-run origin main`.

(b) ENGINE: if no scripts/new_video.sh of the faceless-shorts skill is on the machine (the synced skill is often only SKILL.md), unzip the repo's kit/faceless-shorts-skill.zip, copy its faceless-shorts/ folder to ~/skills/ and chmod +x its scripts. Its Deep Dive 3D style is the only style to use.

(c) VOICE: install Piper + the en-us-ryan-high voice from the rhasspy/piper v0.0.2 GitHub release into /home/claude/piper.

(d) KIT: copy everything in the repo's kit/ folder into /root/faceless-shorts/kit/. Every file the RUNBOOK lists that the repo's kit/ does not have yet (money.js, flip.js, shops.js, site.js, piper_voice.py, example_shots_flip_rehab.js, pro_voice.py, apply_kit_patches.py): read it from Dropbox "/deva invests/kit" with the fetch tool and write it out exactly (Dropbox download links are blocked here), then COMMIT AND PUSH those files into the repo's kit/ straight away so no later run repeats this slow step. Then run apply_kit_patches.py on the kit folder (on the machine copy; it is safe to run twice).

(e) If the engine still cannot be restored, do NOT use another style or tool: send a PushNotification saying exactly what is missing, save the researched scripts to Dropbox, and stop.

(f) CATCH UP on "awaiting_upload" entries of YOUR series in the newest state file (plus its .note.md corrections), in part order:
- If the part's files are in the repo (root, reels/ or covers/): schedule it as step 6 describes at the next free slot of its series and move it to "scheduled".
- If they are NOT in the repo: do not wait for the owner. REMAKE that part first, from the script, triple hook, END QUESTION, captions and sources saved in its state entry (no new research), and schedule it. Each remade part counts toward this run's 3 parts.
The FLIPPING run also schedules another series' awaiting part if its files are in the repo, but never remakes another series' parts.

## 1. LOAD THE PLAN
Read in Dropbox folder "/deva invests/kit": PLAYBOOK.md, SERIES.md, and the newest state_YYYY-MM-DD[-n].json (highest date, then highest suffix; .note.md files are corrections to read with it). Read kit/ENGAGEMENT.md in the repo. (SFX.md is retired by the essential-sounds rule above.)

## 1b. LEARN AND RESEARCH (ONLY the FLIPPING run; the others just read "performance" in the state file)
Every night: pull Metricool analytics for reels published 2-7 days ago (getAnalyticsAvailableMetrics, then getAnalyticsDataByMetrics; Instagram, TikTok, YouTube), record them in the state file under "performance" with each reel's hook pattern, format, series, part number and position in its block, and decide what to do more or less of. Track especially: average watch time / retention, shares, saves, comments, profile visits and follows per reel, and whether parts 2 and 3 of a block get fewer views than part 1. Keep this step short (a few calls). On Sundays (America/Toronto) also refresh the research as ENGAGEMENT.md says (web search; vidIQ only if it has credits), update kit/ENGAGEMENT.md in the repo with new evidence-backed patterns (script/hook/story/format/pacing only), commit and push; and check every link in the three toolkits still loads and each tool still has the free plan described (WebFetch), reporting any dead link or changed free plan to the owner. Never add, remove or swap toolkit tools yourself.

## 2. DECIDE WHAT TO MAKE
Call getScheduledPosts (blogId 7863140) from now to two days ahead. ORDER (owner's request, Nov 11): a series' parts are always posted in number order with no gaps and no duplicates. The next part to make is the lowest part number of your series that is not scheduled or published (awaiting parts first, see 0f). Never schedule Part N+1 before Part N; if a later part is already scheduled ahead of a missing one, move it behind with updateScheduledPost (all of that part's posts: IG/FB/TikTok, Threads, YouTube). Never move or create a post in the past. Make at most 3 parts this run. Plan the block's parts together as one mini-story (BINGE-WATCH RULES) before writing any script; the state file's "*_blocks" plans already do this for the coming days. For each reel choose the FORMAT (A would-you-rather, B same-start-different-outcome, C money chain, D countdown, E breakdown) and hook pattern per ENGAGEMENT.md, never the same format twice in one block; record the choice in the state file. Each part must also work for someone who sees it alone: one sentence of context in the first 3 seconds, never "as we said in part 1".

## 3. MAKE EACH REEL
Exactly as PLAYBOOK.md and the RUNBOOK (section 5) describe, in the SAME animation style as the posted reels, following every rule above (TRIPLE HOOK in the first ~5 s, HOOK -> BUILDUP -> PAYOFF with the payoff last, the series character, a "pause and guess" beat at ~60-70%, the END QUESTION as the last story line, 25-38 s of story, something changing on screen every 2 s or less): research real, current numbers with web search first (cite sources in script.json; never invent a figure), 9-12 lines each with a directed "say", narrate with kit/pro_voice.py, Deep Dive 3D shots that use the kit sets (for format A put two sets side by side, split screen), check + contact sheet and LOOK at it, render in segments under 10 minutes each (two ~9.5-second segments at a time in the background), concat with audio.

SOUND: right after new_video.sh copy the PATCHED kit/mix_sfx.py over the project's tools/mix.py (it must print "music: none"), and in the project's src/main.js change the line `drawCaption(t);` to `if (!/nocap/.test(location.search)) drawCaption(t);` (lets covers be rendered without captions). In shots.js put exactly one 'impact' cue on the big reveal and nothing else.

ENDINGS: run kit/series_end_sfx.py (not series_end.py; pass the whole spoken tease from the BINGE-WATCH RULES in the SPOKEN_FULL environment variable) for both the _IG ending (comment the series KEYWORD for the free <Series> Starter Toolkit) and the _YT ending (free toolkit link in the description), with the series name, part number and the next-part tease. Name files <Series>_Part<N>_IG.mp4 and <Series>_Part<N>_YT.mp4. Do NOT build any .xlsx or other tool.

COVER (every reel): render 2 clean candidate frames of the most striking scene with `QS='&nocap=1&res=1&shadow=2048' node tools/capture.mjs frames <dir> "<t1>,<t2>"`, LOOK at them, pick the one that best shows the hook, then run `python3 kit/make_cover.py <frame.jpg> <Series>_Part<N>_cover.jpg "<SERIES> SERIES" <N> "<hook line 1>" "<line 2>" ["<line 3>"] [--sub "<short tag>"]`: 2-3 short ALL-CAPS lines from the reel's main hook (max 7 words total), the key number or word in [brackets] to turn it yellow, numbers exactly as in the reel. Hook text in the vertical MIDDLE of the cover (the default) and a big PART badge (the default). If in-scene labels sit behind the text, push the scene down with --shift (100-450) or pick another frame. LOOK at the cover and fix any overlap.

COVER AT THE START OF THE VIDEO (every reel): after the endings are added, run `sh kit/cover_intro.sh <Series>_Part<N>_IG.mp4 <cover.jpg> <tmp_IG.mp4>` and the same for _YT, then replace the _IG/_YT files with the results. Check one frame at 0.3 s shows the cover.

## 4. UPLOAD TO GITHUB (right after each reel is finished)
In the clone, copy the reel's _IG and _YT mp4s into reels/ (each under 95 MB; re-encode with crf 22 if over 10 MB) and the cover into covers/, commit with git user "deva invests" <devarshipatil88@gmail.com>, then `git pull --rebase` and push to main with a normal push (never force-push or rewrite history). If the push is rejected because the remote moved, pull --rebase again and retry, up to 3 times. Public URLs: https://raw.githubusercontent.com/devapatil078/Deva_Invests_Reels/main/reels/<file name> and .../main/covers/<file name>.

If the push is still refused after calling add_repo with access "push" again: the Google Drive and Dropbox connectors cannot carry videos, so do not try them. Send each _IG.mp4, _YT.mp4 and cover with SendUserFile, send ONE PushNotification saying the push failed and quoting the exact error (do NOT ask the owner to change any task setting), and save each part under "awaiting_upload" in the state file with its file names, sizes, script lines, captions, TikTok title, Threads text, YouTube title/description/first comment and END QUESTION.

## 6. SCHEDULE IN METRICOOL (right after each reel is pushed)
blogId 7863140 (its label says "Sudbury Total Contracting"; that is expected). Call getBrandSettings first. Continue only if instagramData is "deva_invests". Facebook: the correct deva invests page is facebookData "1213809048474778". NEVER post to Facebook if facebookData is "1192256843968009" (the owner's Sudbury Total Contracting page) or any id other than 1213809048474778; then skip Facebook and report it. TikTok (tiktokData "deva_invests") and Threads (threadsData "deva_invests") are connected; skip a network if its value is missing or different and report it. Check getScheduledPosts to avoid duplicates. For each new part, at its slot date/time in America/Toronto, create:

a) one post with providers instagram + facebook + tiktok using the _IG raw.githubusercontent URL, videoThumbnailUrl = the cover's raw.githubusercontent URL, and the caption (line 1 the hook; line 2 "🎬 <Series> series · Part N · start from Part 1 on my page"; 2-3 lines of real numbers with sources; the END QUESTION; "💬 Comment KEYWORD and I'll DM you my free <Series> Starter Toolkit: 7 free, trusted tools. Inside: <one tool> to <job>."; what comes next: "Part N+1 in 1 hour" if the next part is scheduled an hour later, otherwise "Part N+1 tomorrow"; "Worked example, not financial advice."; up to 5 hashtags): instagramData {type REEL, showReelOnFeed true, isAiGenerated true}, facebookData {type REEL}, tiktokData {title: a short hook under 90 characters (REQUIRED), privacyOption PUBLIC_TO_EVERYONE, isAigc true};

b) a separate threads post with the same _IG video (no videoThumbnailUrl) and a SHORT text under 450 characters (hook, the key numbers, the END QUESTION, "Free <Series> Starter Toolkit: comment KEYWORD on @deva_invests on Instagram.", series + part), threadsData {};

c) a separate youtube post (youtubeData type "short", title ending in #shorts, privacy public, madeForKids false, isAiGeneratedContent true, category EDUCATION) using the _YT URL, videoThumbnailUrl = the cover URL, a description whose first line is the hook, then "🎬 <Series> series · Part N", then the END QUESTION, then "Free <Series> Starter Toolkit (7 free, trusted tools): <that toolkit's Drive link>", and firstCommentText "Free <Series> Starter Toolkit: <that toolkit's Drive link>. Next: Part N+1."

Confirm each response's media (and videoThumbnailUrl) became static.metricool.com URLs; if a post is rejected only because of the thumbnail, retry it once without videoThumbnailUrl and report it. Once Metricool has copied a video, delete it from the repo's reels/ in a normal commit and push (pull --rebase first) so the repo stays small (never touch kit/ or covers/). Never schedule a post in the past. Do not create test posts. (Ignore the old draft "TEST DRAFT - delete" on Nov 30; it is the owner's to remove.)

## 7. SAVE PROGRESS (after each reel, and at the end)
Right before writing, re-read the newest state file in Dropbox (another run may have written one since you started) and start from it, changing only your series' entries (plus "performance" if you are the FLIPPING run, and any "awaiting_upload" entries you scheduled); keep everything else exactly. Write a NEW Dropbox file "/deva invests/kit/state_YYYY-MM-DD.json" (today's date; add -2, -3 ... if that name exists, since Dropbox cannot overwrite) with the updated made/scheduled/awaiting_upload lists (Metricool post ids, cover URLs, format + the 3 triple-hook candidates and the one used + END QUESTION + the toolkit tool named per reel, each block's mini-story), the performance log and the next plan. Keep the file small: drop full captions of parts that are already scheduled. When your series has fewer than 6 listed parts left, plan 6 more in the same style (two 3-part mini-stories) and record them.

## FINISH
Send a short SendUserMessage summary: which series this run handled, the block's mini-story in one line, what was made (format and END QUESTION per reel), what was scheduled (times and networks) or moved, which new Instagram reels to link with "Add linked reel" (Part N -> Part N+1), one line on what the numbers say is working (FLIPPING run only), and anything that failed. Send each new cover with SendUserFile too.
