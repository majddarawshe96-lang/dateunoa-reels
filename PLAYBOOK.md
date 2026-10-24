# @dateunoa content playbook (v3: Buffer, 10 posts/day on Instagram, Facebook and X)

Goal: sell the **dateunoa Collection** with short reels in the dating niche. Every post is built to be shared, saved or commented, and every caption points to the link.
The owner has approved every post in advance. Do not ask for approval; schedule directly.

> **If your run's prompt asks you to schedule Instagram reels in Metricool ("make sure tomorrow has 6 Instagram reels scheduled in Metricool"), or you have no Buffer tools:** you are the old scheduled task "dateunoa daily reels". (The current task, "dateunoa daily content", works through Buffer; this note is not for it.) Instagram moved to Buffer (10 reels/day from 2026-10-26), so do NOT schedule anything in Metricool. Just check that the Buffer schedule exists if you can, and report: "Old Metricool task ran; nothing scheduled. Please replace it with the Buffer task." Then stop.

## Products (all on Gumroad)
| Book | Price | Who it's for | Promise |
| --- | --- | --- | --- |
| I. **"What Do I Text Back?"** | $28 | women overthinking texts | the exact words for slow replies, mixed signals & boundaries |
| II. **"What Do Men Want?"** | $28 | women dating men | what he's really looking for, how he shows interest, what makes him stay |
| III. **"What Do Women Want?"** | $28 | men (and women who send it to him) | what makes her feel safe, what makes her choose you, the exact texts to send |
| **The dateunoa Collection** (all 3) | **$56** (instead of $84) | everyone | buy 2, get the 3rd free |

## Accounts
- **Buffer** organization `6ac7b051734c0ca7668122d6` ("My organization"), timezone Asia/Jerusalem. Channels:
  - Instagram `dateunoa` (business): `6ac7b0a16a5c39ccb651ff2c` (daily limit 50)
  - Facebook page `Dateunoa`: `6ada5f7b778b240e2f9111b7` (daily limit 35)
  - X `dateunoa`: `6ac7b0f46a5c39ccb6520e30` (daily limit 100)
  Check with list_channels that all three exist and are not disconnected before scheduling. If one is disconnected, schedule the others and report it.
- **Metricool** (brand `7569841`) is now only used for Instagram analytics. Do not schedule new posts there (it would double the Instagram volume).
- Media host: this repo (public). `reels/<folder>/<name>.mp4` on `main` is served at
  `https://raw.githubusercontent.com/majddarawshe96-lang/dateunoa-reels/main/reels/<folder>/<name>.mp4`
- Never commit the ebook PDFs or their text to this repo. It is public.
- Another app (a Replit tool, posts via Buffer with storage.googleapis.com videos) also posts to Instagram/X. Leave its posts alone.

## Daily run (keeps the schedule 7 days ahead)
1. Target day = today + 7 days (Asia/Jerusalem). Also check every day between tomorrow and the target day; fill any day that has fewer than 10 of our posts on a channel (oldest first, at most 3 days per run).
   Our posts are the ones whose video URL starts with the raw.githubusercontent.com link above. Query with `execute_query`:
   `posts(first:100, input:{organizationId:"6ac7b051734c0ca7668122d6", filter:{dueAt:{start:"<day>T00:00:00+02:00", end:"<day>T23:59:59+02:00"}, status:[scheduled,sent,sending]}})`
   (use +03:00 while Israel is on summer time).
2. Write the day's content as `content/days/<YYYY-MM-DD>.py` (same format as `content/week1.py`: `DAYS = {"<date>": {"promo": <name>, "posts": [9 × (pillar, quote, hook)]}}` ; promo captions live in `tools/captions.py`). Promo rotation by day: men_cover, women_cover, bundle, men_page, women_page, textback, men_page2, women_page2 (index = day-of-year % 8).
3. Never reuse a quote from `used_quotes.txt` (no near-duplicates either). Check with a quick word-overlap script before rendering.
4. Render: `python3 tools/make_post.py --music tools/music --start <day-of-year % 6> tools/avatar.jpg out/<date> dateunoa "<q1>" ... "<q9>"`.
   Look at one frame per day (no line over the edge, no orphan word on its own line). Copy `out/<date>/reel_N.mp4` to `reels/<date>/dq_0N.mp4`.
5. Append the quotes (one per line, newlines replaced by spaces) to `used_quotes.txt`, commit, push to `main`.
6. Build the Buffer batch: `python3 tools/buffer_plan.py content/days/<date>.py out/bp --batch 30` → `out/bp/batch_00.json` holds all 30 posts of the day (10 slots × 3 channels). Send it with Buffer `execute_mutation` (mutation + variables from the file). Max 30 aliases per request.
7. Verify: re-run the query from step 1 for that day and confirm 10 posts per channel and no `error`. If Buffer rejects a post, fix and resend only that post.
8. Also list posts with status `error` from the last 24 h. If any failed for a fixable reason (bad video, caption too long), fix and reschedule; otherwise report.

## Slot plan (10 posts a day, same video on all 3 channels)
| Time | Pillar | Sells | Built to be |
| --- | --- | --- | --- |
| 08:15 | T **Texting truth**: slow replies, "haha", read receipts, "wyd", dry texters | Book I | shared |
| 09:45 | M **What men want**: what he notices, how real interest looks, what makes him stay | Book II | saved |
| 11:15 | S **Self-respect**: standards, boundaries by text, walking away calmly | Book I | saved |
| 12:45 | W **What women want**: safety, consistency, effort, "Men: …" truths | Book III | tagged |
| 14:00 | PROMO reel (book cover / inside-the-book page / bundle) | rotates | clicked |
| 15:45 | HE **"He says / He means"** translator | Book II | commented |
| 17:15 | T **Relatable texting** (funny, POV) | Book I | shared |
| 18:45 | SHE **"She says / She means"** translator | Book III | commented |
| 20:15 | M **Standards / certainty line** ("Real interest looks like…", lists) | Book II | saved |
| 21:45 | B **Soft pitch** naming the collection | Bundle | clicked |

## Month themes (Oct 24 – Nov 22, 2026)
Each week leans on one topic across all pillars, so the feed tells a story and the promo reels match it.
| Dates | Theme | Push |
| --- | --- | --- |
| Oct 24 – Oct 29 | Launch week: introducing the three books | covers + bundle |
| Oct 30 – Nov 5 | Mixed signals & situationships ("what are we?") | What Do Men Want? |
| Nov 6 – Nov 12 | Slow replies, ghosting & people who come back | What Do I Text Back? |
| Nov 13 – Nov 19 | Effort, consistency & what men/women actually notice | What Do Women Want? |
| Nov 20 – Nov 22 | Holiday season: "send it to the group chat" gift angle | Bundle ($56) |
After Nov 22, repeat the cycle with the Monday analytics deciding the order.

## Visual style (tools/make_post.py — don't change it)
Black background, X/Twitter-post look: round avatar, bold "dateunoa", grey "@dateunoa", white Inter text, slow push-in, original lo-fi music bed (tools/music, made by tools/make_music.py, royalty-free).
Promo reels come from tools/make_promo.py (covers and sample pages in tools/promo_assets).

## Quote rules
- Short (1–4 short lines, under ~35 words). Line breaks between beats.
- Translator format: two labelled beats, e.g. `He says: "Let's just see where it goes."\n\nHe means: "I'm not choosing yet."`
- Balanced: never insulting to men or women as a group. Truths about behaviour, not a gender's worth.
- No emojis inside the quote image. No real people, no song lyrics, nothing sexual.
- What performs in this niche (vidIQ outliers, Oct 2026): first-person confessions ("I don't want an angry man."), certainty lines ("Nothing can stop a man who really wants to see you."), short standards lists ("Calm. Consistent. Makes plans. Not much to ask."), and men-vs-women contrasts that invite debate.

## Captions (tools/captions.py builds them — keep it as the single source)
Every caption markets the whole collection (all 3 ebooks), led by the book that fits the post. All 3 live behind ONE link in bio (a free link-in-bio page or the Gumroad profile page).
- Instagram: hook + the book's line + the 3-book list + "📲 All 3 ebooks: link in bio" + 5 hashtags.
- Facebook: same, with "📲 All 3 ebooks: link in our page intro" + 3 hashtags.
- X: hook + "3 dating ebooks: What Do I Text Back? · What Do Men Want? · What Do Women Want? All 3: link in bio." + 2 hashtags (under 280 characters).
Promo captions describe the current books (no claims that aren't in the PDFs). Hooks: different every post, 1 emoji, with a share/save/comment nudge when it fits.

## Weekly check (Mondays only)
1. Buffer `list_posts` with `includeMetrics: true` for the last 7 days per channel (views, reach, shares, saves, comments). Instagram can also be checked in Metricool (IGRE23 views, IGRE11 reach, IGRE12 saves, IGRE21 shares).
2. Rank pillars and hooks by shares + saves (+ comments for translators). Write more of the winners; if a pillar loses two weeks in a row, swap its slot to the best pillar.
3. Optionally one vidIQ outlier search for fresh hooks.
4. Append a dated note to `NOTES.md` and push.

## Report
End every run with one short summary: days filled, posts scheduled per channel, any errors. Send a push notification only if something failed or needs the owner.
