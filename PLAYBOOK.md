# @dateunoa daily reel playbook

Goal: sell the ebook **"What Do I Text Back?"** (Gumroad, $28, link in the Instagram bio) with quote reels on Instagram @dateunoa.
The owner has approved every post in advance. Do not ask for approval; schedule directly.

## Accounts
- Metricool brand id (blogId): `7569841`, timezone `Asia/Jerusalem`. Check with getBrandSettings that `instagramData` is `dateunoa` before scheduling. If it is a different handle, schedule nothing and report it.
- Media host: this repo (public). A file at `reels/<batch>/<name>.mp4` on `main` is served at
  `https://raw.githubusercontent.com/majddarawshe96-lang/dateunoa-reels/main/reels/<batch>/<name>.mp4`

## Daily run
1. Target day = tomorrow (Asia/Jerusalem).
2. getScheduledPosts for the target day. If 6 or more Instagram posts are already scheduled, stop: nothing to do.
3. Write new quotes to fill the day up to 6 reels. Never reuse anything in `used_quotes.txt`.
4. Render: `python3 tools/make_post.py tools/avatar.jpg out dateunoa "<quote 1>" "<quote 2>" ...`
   Use only `out/reel_N.mp4` (1080x1920, 8 s). Look at one rendered frame to check nothing overflows.
5. Copy the mp4s to `reels/<YYYY-MM-DD>/dateunoa_reel_NN.mp4`, append the quotes (one per line, newlines replaced by spaces) to `used_quotes.txt`, commit and push to `main`.
6. Schedule each reel with createScheduledPost (type REEL, showReelOnFeed true, autoPublish true) at the free slots among:
   **08:40, 11:50, 14:20, 17:10, 19:40, 22:10** (Asia/Jerusalem).
7. Music: try `audioConfiguration` with a mood-fitting song on the first reel. If Metricool returns an authorization error, schedule all reels without audio.

## Visual style (already in tools/make_post.py — don't change it)
Black background, X/Twitter-post look: round avatar, bold "dateunoa", grey "@dateunoa", white Inter text.

## Quote rules
- Short (1–3 short lines, under ~30 words). Line breaks between beats, like the examples.
- Every quote is about the texting moment: slow replies, "haha", "u up", read receipts, double texting, mixed signals, ghosting, "busy", dry texters, setting a boundary by text, what to send.
- Mix per day: 3 relatable (built to be shared), 2 self-respect (built to be saved), 1 that points at needing a plan / the right words (soft pitch).
- No emojis inside the quote image. No real people, no song lyrics, nothing sexual, nothing insulting to men or women as a group.
- Examples of the voice:
  - "If they wanted to text you back, you'd have a text. / Stop decoding silence."
  - "\"sorry I've been so busy\" / is a reason once. / the third time, it's an answer."
  - "Read at 9:42 PM. / Replied at 2:17 AM. / That's not mystery. That's a schedule you're not on."

## Caption template
```
<short hook line, different every reel, 1 emoji> 

Still staring at your phone? "What Do I Text Back?" gives you the exact words for slow replies, mixed signals & boundaries — without looking needy.

📲 Link in bio

<hashtag set>
```
Rotate hashtag sets:
- A: #datingadvice #textingtips #mixedsignals #situationship #relationshipadvice
- B: #datingtips #situationships #overthinking #selfrespect #moderndating
- C: #textingadvice #datinglife #relationshipquotes #knowyourworth #dating

## Weekly check (Mondays only)
Pull Instagram reels analytics for the last 7 days (views IGRE23, reach IGRE11, saves IGRE12, shares IGRE21, plus content IGRE03).
Find the 3 best and 3 worst reels by shares + saves. Write more quotes like the best ones that week.
Append a short dated note to `NOTES.md` (what worked, what to do more of) and push.

## Report
End every run with one short summary message: how many reels were scheduled, for which times, and any errors (especially Metricool plan limits or a wrong Instagram handle).
