# @dateunoa daily reel playbook

Goal: sell the **dateunoa Collection** with quote reels on Instagram @dateunoa. Every reel is built to be shared or saved, and every caption points to the link in bio.
The owner has approved every post in advance. Do not ask for approval; schedule directly.

## Products (all on Gumroad, link in the Instagram bio)
| Book | Price | Who it's for | Promise |
| --- | --- | --- | --- |
| I. **"What Do I Text Back?"** | $28 | women overthinking texts | the exact words for slow replies, mixed signals & boundaries |
| II. **"What Do Men Want?"** | $28 | women dating men | what he's really looking for, how he shows interest, what makes him stay |
| III. **"What Do Women Want?"** | $28 | men (and women who send it to him) | what makes her feel safe, what makes her choose you, the exact texts to send |
| **The dateunoa Collection** (all 3) | **$56** (instead of $84) | everyone | buy 2, get the 3rd free |

## Accounts
- Metricool brand id (blogId): `7569841`, timezone `Asia/Jerusalem`. Check with getBrandSettings that `instagramData` is `dateunoa` before scheduling. If it is a different handle, schedule nothing and report it.
- Media host: this repo (public). A file at `reels/<batch>/<name>.mp4` on `main` is served at
  `https://raw.githubusercontent.com/majddarawshe96-lang/dateunoa-reels/main/reels/<batch>/<name>.mp4`
- Never commit the ebook PDFs or their text to this repo. It is public.

## Daily run
1. Target day = tomorrow (Asia/Jerusalem).
2. getScheduledPosts for the target day. If 6 or more Instagram posts are already scheduled, stop: nothing to do.
3. Write new quotes for the free slots using the **slot plan** below. Never reuse anything in `used_quotes.txt` (no near-duplicates either).
4. Render: `python3 tools/make_post.py tools/avatar.jpg out dateunoa "<quote 1>" "<quote 2>" ...`
   Use only `out/reel_N.mp4` (1080x1920, 8 s). Look at one rendered frame to check nothing overflows (max ~9 rendered lines).
5. Copy the mp4s to `reels/<YYYY-MM-DD>/dateunoa_reel_NN.mp4`, append the quotes (one per line, newlines replaced by spaces) to `used_quotes.txt`, commit and push to `main`.
6. Schedule each reel with createScheduledPost (type REEL, showReelOnFeed true, autoPublish true) at its slot time (Asia/Jerusalem).
7. Music: try `audioConfiguration` with a mood-fitting song on the first reel. If Metricool returns an authorization error, schedule all reels without audio.

## Slot plan (6 reels a day)
| Time | Pillar | Sells | Built to be |
| --- | --- | --- | --- |
| 08:40 | **Texting truth**: slow replies, "haha", read receipts, "u up", dry texters | Book I | shared |
| 11:50 | **What men want**: what he notices, how real interest looks, what makes him stay | Book II | saved / shared |
| 14:20 | **Self-respect**: standards, boundaries by text, walking away calmly | Book I | saved |
| 17:10 | **What women want**: safety, consistency, effort, "tag him" truths aimed at men | Book III | shared / tagged |
| 19:40 | **Translator / debate**: "He says / He means", "She says / She means", "Men think… Women think…" | Book II or III (alternate daily) | commented |
| 22:10 | **Soft pitch**: needing a plan, the right words, understanding him/her; names the collection | Bundle | clicked |

If only some slots are free, fill those slots with their own pillar.

## Visual style (already in tools/make_post.py — don't change it)
Black background, X/Twitter-post look: round avatar, bold "dateunoa", grey "@dateunoa", white Inter text.

## Quote rules
- Short (1–4 short lines, under ~35 words). Line breaks between beats, like the examples.
- Translator format uses two labelled beats on separate lines, e.g. `He says: "I'm just bad at texting."\nHe means: "You're not a priority yet."`
- Balanced: never insulting to men or women as a group. Truths about behaviour, not about a gender's worth. Pair a "men" truth with a "women" truth across the day.
- No emojis inside the quote image. No real people, no song lyrics, nothing sexual.
- What performs right now in this niche (vidIQ outliers, Oct 2026): first-person confessions ("I don't want an angry man."), "nothing can stop a man who really wants you"-style certainty lines, short lists of standards ("Consistent. Calm. Makes plans. Not much to ask."), and men-vs-women contrasts that invite debate. Lean into those.
- Examples of the voice:
  - "If they wanted to text you back, you'd have a text. / Stop decoding silence."
  - "\"sorry I've been so busy\" / is a reason once. / the third time, it's an answer."
  - "Read at 9:42 PM. / Replied at 2:17 AM. / That's not mystery. That's a schedule you're not on."
  - (men) "Men don't fall for perfect. / They fall for peace."
  - (women) "She doesn't need a grand gesture. / She needs you to do what you said you'd do."
  - (translator) "She says: \"It's fine.\" / She means: \"Ask me again, but softer.\""

## Caption templates
Hook line: short, different every reel, 1 emoji. Then the block for the pillar's book, then the hashtag set.

Book I (texting truth, self-respect):
```
<hook>

Still staring at your phone? "What Do I Text Back?" gives you the exact words for slow replies, mixed signals & boundaries — without looking needy.

📲 Link in bio

<hashtag set>
```
Book II (what men want, translator about him):
```
<hook>

Stop guessing what he means. "What Do Men Want?" shows you what he's really looking for, how real interest looks, and what makes him stay.

📲 Link in bio

<hashtag set>
```
Book III (what women want, translator about her):
```
<hook>

Send this to him 👀 "What Do Women Want?" — what makes her feel safe, what makes her choose you, and the exact texts to send.

📲 Link in bio

<hashtag set>
```
Bundle (soft pitch):
```
<hook>

The dateunoa Collection: "What Do I Text Back?", "What Do Men Want?" & "What Do Women Want?" — all 3 for $56. Buy 2, get 1 free.

📲 Link in bio

<hashtag set>
```
End every caption's hook or first line with a share/save/comment nudge when it fits: "Send this to the group chat", "Save this for later", "Tag him", "Men, agree?".

Rotate hashtag sets:
- A: #datingadvice #textingtips #mixedsignals #situationship #relationshipadvice
- B: #datingtips #situationships #overthinking #selfrespect #moderndating
- C: #textingadvice #datinglife #relationshipquotes #knowyourworth #dating
- M (what men want): #whatmenwant #datingadviceforwomen #relationshipgoals #healthyrelationships #datingtips
- W (what women want): #whatwomenwant #datingadviceformen #mensadvice #relationshipadvice #modernromance

Use M for Book II reels, W for Book III reels, and rotate A/B/C for the rest.

## Weekly check (Mondays only)
Pull Instagram reels analytics for the last 7 days (views IGRE23, reach IGRE11, saves IGRE12, shares IGRE21, plus content IGRE03).
Find the 3 best and 3 worst reels by shares + saves, and compare pillars (which slot wins). Write more quotes like the best ones that week, and if one pillar is clearly losing for 2 weeks, swap that slot to the winning pillar.
Optionally run one vidIQ outlier search (dating niche, last 30 days) for fresh hooks.
Append a short dated note to `NOTES.md` (what worked, what to do more of) and push.

## Report
End every run with one short summary message: how many reels were scheduled, for which times, and any errors (especially Metricool plan limits or a wrong Instagram handle).
