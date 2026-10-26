"""Generate the dateunoa month content calendar page (HTML body for the Artifact tool).

Usage: python3 tools/make_calendar.py <out.html>
"""
import html
import importlib.util
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("w1", ROOT / "content/week1.py")
w1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w1)

START, END = date(2026, 10, 24), date(2026, 11, 22)
SLOTS = [("08:15", "T", "Texting truth", "I"), ("09:45", "M", "What men want", "II"), ("11:15", "S", "Self-respect", "I"),
         ("12:45", "W", "What women want", "III"), ("14:00", "P", "Promo reel", "rotates"), ("15:45", "HE", "He says / He means", "II"),
         ("17:15", "T", "Relatable texting", "I"), ("18:45", "SHE", "She says / She means", "III"), ("20:15", "M", "Standards line", "II"),
         ("21:45", "B", "Bundle pitch", "All 3")]
THEMES = [
    (date(2026, 10, 24), date(2026, 10, 29), "Launch week", "Introducing the three books", "Covers + bundle"),
    (date(2026, 10, 30), date(2026, 11, 5), "Mixed signals", "Situationships and “what are we?”", "What Do Men Want?"),
    (date(2026, 11, 6), date(2026, 11, 12), "Slow replies", "Ghosting and people who come back", "What Do I Text Back?"),
    (date(2026, 11, 13), date(2026, 11, 19), "Effort", "Consistency and what each side notices", "What Do Women Want?"),
    (date(2026, 11, 20), date(2026, 11, 22), "Gift season", "“Send it to the group chat”", "Bundle $56"),
]
PROMOS = ["men_cover", "women_cover", "bundle", "men_page", "women_page", "textback", "men_page2", "women_page2"]
PROMO_NAME = {"men_cover": "Men cover", "women_cover": "Women cover", "bundle": "Bundle", "men_page": "Inside: his texts",
              "women_page": "Inside: texting rules", "textback": "Text Back", "men_page2": "Inside: option or into you",
              "women_page2": "Inside: confident vs arrogant"}
BOOKS = {"I": "What Do I Text Back?", "II": "What Do Men Want?", "III": "What Do Women Want?"}


def theme_for(d):
    for a, b, name, desc, push in THEMES:
        if a <= d <= b:
            return name, desc, push
    return "", "", ""


def esc(s):
    return html.escape(s)


days = []
d = START
while d <= END:
    key = d.isoformat()
    if key in w1.DAYS:
        promo = w1.DAYS[key]["promo"]
        status = "scheduled"
    else:
        promo = PROMOS[d.timetuple().tm_yday % 8]
        status = "auto"
    ig = "from Oct 26" if d < date(2026, 10, 26) else ""
    days.append((d, promo, status, ig))
    d += timedelta(days=1)

# calendar grid (weeks start Sunday, Israel)
first = START - timedelta(days=(START.weekday() + 1) % 7)
cells = []
d = first
while d <= END or (d - first).days % 7:
    if START <= d <= END:
        _, promo, status, ig = next(x for x in days if x[0] == d)
        name, _, push = theme_for(d)
        cells.append(f'''<div class="day {status}" data-theme-name="{esc(name)}">
  <div class="dnum"><span>{d.day}</span><span class="mon">{d.strftime('%b')}</span></div>
  <div class="dtheme">{esc(name)}</div>
  <div class="dpromo">{esc(PROMO_NAME[promo])}</div>
  <div class="dstat">{'Scheduled' if status == 'scheduled' else 'Auto-filled 7 days ahead'}{(' · IG ' + ig) if ig else ''}</div>
</div>''')
    else:
        cells.append('<div class="day blank" aria-hidden="true"></div>')
    d += timedelta(days=1)

slot_rows = "".join(
    f'<tr><td class="t">{t}</td><td><span class="pill p-{c}">{c}</span></td><td>{esc(n)}</td><td>{esc(BOOKS.get(b, b))}</td></tr>'
    for t, c, n, b in SLOTS)
theme_rows = "".join(
    f'<li><div class="th-dates">{a.strftime("%b %-d")} – {b.strftime("%b %-d")}</div><div class="th-name">{esc(n)}</div>'
    f'<div class="th-desc">{esc(ds)}</div><div class="th-push">Push: {esc(p)}</div></li>'
    for a, b, n, ds, p in THEMES)

week1 = []
for key, v in w1.DAYS.items():
    dd = date.fromisoformat(key)
    posts = list(v["posts"])
    rows = []
    qi = 0
    for si, (t, c, n, b) in enumerate(SLOTS):
        if c == "P":
            rows.append(f'<li><span class="t">{t}</span><span class="pill p-P">Promo</span><span class="q">{esc(PROMO_NAME[v["promo"]])} reel</span></li>')
            continue
        p, q, h = posts[qi][:3]
        qi += 1
        rows.append(f'<li><span class="t">{t}</span><span class="pill p-{p}">{p}</span><span class="q">{esc(q).replace(chr(10)*2, " / ").replace(chr(10), " / ")}</span></li>')
    nets = "Facebook + X" if dd < date(2026, 10, 26) else "Instagram + Facebook + X"
    week1.append(f'<details class="wk"{" open" if key == "2026-10-24" else ""}><summary><span>{dd.strftime("%a %b %-d")}</span><span class="nets">{nets} · 10 posts each</span></summary><ol>{"".join(rows)}</ol></details>')

total_sched = sum(30 if x[0] >= date(2026, 10, 26) else 20 for x in days if x[2] == "scheduled")

page = f'''<title>dateunoa Content Calendar</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Manrope:wght@400;500;600;700&display=swap">
<style>
/* Layout: one column brief → slot table + themes side by side → month grid → week-1 post list */
:root {{
  --bg: #f6f2ea; --surface: #fffdf8; --ink: #1b1813; --muted: #6f675a; --line: #e2d9c8;
  --gold: #9a7a3e; --gold-soft: #efe4cc; --auto: #f0ece4;
  --display: "Cormorant Garamond", "Iowan Old Style", Georgia, serif;
  --body: "Manrope", "Segoe UI", system-ui, sans-serif;
  --pT: #e9dfcb; --pM: #dfe6ee; --pS: #ece2e6; --pW: #e2eadf; --pP: #f3e2bf; --pHE: #dce5ee; --pSHE: #e7e0ec; --pB: #f1dcc3;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #12100c; --surface: #1b1813; --ink: #f1e8d6; --muted: #a89d88; --line: #2f2a21;
  --gold: #d9b979; --gold-soft: #2c2518; --auto: #17140f;
  --pT: #2f281b; --pM: #1e2731; --pS: #2c2228; --pW: #212b21; --pP: #3a2f18; --pHE: #1f2a35; --pSHE: #2a2431; --pB: #362816; color-scheme: dark }} }}
:root[data-theme="dark"] {{
  --bg: #12100c; --surface: #1b1813; --ink: #f1e8d6; --muted: #a89d88; --line: #2f2a21;
  --gold: #d9b979; --gold-soft: #2c2518; --auto: #17140f;
  --pT: #2f281b; --pM: #1e2731; --pS: #2c2228; --pW: #212b21; --pP: #3a2f18; --pHE: #1f2a35; --pSHE: #2a2431; --pB: #362816; color-scheme: dark }}
body {{ background: var(--bg); color: var(--ink); font-family: var(--body); font-size: 15px; line-height: 1.55; }}
.wrap {{ max-width: 1120px; margin: 0 auto; padding-block: 40px 64px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 40px; }}
header {{ display: grid; gap: 10px; }}
.eyebrow {{ font-size: 12px; letter-spacing: .16em; text-transform: uppercase; color: var(--gold); font-weight: 600; }}
h1 {{ font-family: var(--display); font-weight: 600; font-size: clamp(36px, 6vw, 56px); line-height: 1.02; margin: 0; text-wrap: balance; }}
h2 {{ font-family: var(--display); font-weight: 600; font-size: 28px; margin: 0 0 14px; }}
.lede {{ max-width: 66ch; color: var(--muted); margin: 0; }}
.stats {{ display: flex; flex-wrap: wrap; gap: 28px; margin-top: 8px; font-variant-numeric: tabular-nums; }}
.stat b {{ display: block; font-family: var(--display); font-size: 34px; font-weight: 600; line-height: 1; }}
.stat span {{ font-size: 13px; color: var(--muted); }}
.two {{ display: grid; grid-template-columns: 1.15fr 1fr; gap: 32px; }}
.two > * {{ min-width: 0; }}
.tablebox {{ overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
th {{ text-align: left; font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); font-weight: 600; padding: 0 10px 8px 0; border-bottom: 1px solid var(--line); }}
td {{ padding: 9px 10px 9px 0; border-bottom: 1px solid var(--line); vertical-align: top; }}
td.t, .t {{ font-variant-numeric: tabular-nums; font-weight: 600; white-space: nowrap; }}
.pill {{ display: inline-block; min-width: 34px; text-align: center; font-size: 11px; font-weight: 700; letter-spacing: .04em; padding: 2px 7px; border-radius: 999px; color: var(--ink); background: var(--gold-soft); }}
.p-T {{ background: var(--pT); }} .p-M {{ background: var(--pM); }} .p-S {{ background: var(--pS); }} .p-W {{ background: var(--pW); }}
.p-P {{ background: var(--pP); }} .p-HE {{ background: var(--pHE); }} .p-SHE {{ background: var(--pSHE); }} .p-B {{ background: var(--pB); }}
.themes {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 14px; }}
.themes li {{ display: grid; grid-template-columns: 120px 1fr; column-gap: 14px; padding-bottom: 14px; border-bottom: 1px solid var(--line); }}
.th-dates {{ grid-row: span 3; font-size: 13px; color: var(--gold); font-weight: 600; font-variant-numeric: tabular-nums; }}
.th-name {{ font-family: var(--display); font-size: 21px; font-weight: 600; line-height: 1.1; }}
.th-desc {{ color: var(--muted); font-size: 14px; }}
.th-push {{ font-size: 13px; }}
.grid {{ display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 6px; }}
.dow {{ font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); font-weight: 600; padding: 0 4px 4px; }}
.day {{ background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 8px; min-height: 108px; display: grid; align-content: start; gap: 3px; }}
.day.auto {{ background: var(--auto); }}
.day.scheduled {{ border-color: var(--gold); }}
.day.blank {{ background: transparent; border: 0; }}
.dnum {{ display: flex; align-items: baseline; gap: 5px; }}
.dnum span:first-child {{ font-family: var(--display); font-size: 24px; font-weight: 600; line-height: 1; }}
.mon {{ font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: .08em; }}
.dtheme {{ font-size: 12px; font-weight: 700; }}
.dpromo {{ font-size: 12px; color: var(--muted); }}
.dstat {{ font-size: 11px; color: var(--gold); }}
.legend {{ display: flex; flex-wrap: wrap; gap: 16px; font-size: 13px; color: var(--muted); margin-top: 12px; }}
.legend i {{ display: inline-block; width: 12px; height: 12px; border-radius: 3px; vertical-align: -1px; margin-right: 6px; border: 1px solid var(--line); }}
.wk {{ border-top: 1px solid var(--line); padding: 12px 0; }}
.wk summary {{ cursor: pointer; display: flex; flex-wrap: wrap; gap: 12px; justify-content: space-between; font-weight: 600; }}
.wk summary:focus-visible {{ outline: 2px solid var(--gold); outline-offset: 3px; }}
.nets {{ font-weight: 500; color: var(--muted); font-size: 13px; }}
.wk ol {{ list-style: none; margin: 12px 0 0; padding: 0; display: grid; gap: 8px; }}
.wk li {{ display: grid; grid-template-columns: 52px 46px 1fr; gap: 10px; align-items: baseline; font-size: 14px; }}
.wk .q {{ min-width: 0; }}
.notes {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }}
.note {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 16px; }}
.note h3 {{ margin: 0 0 6px; font-size: 14px; }}
.note p {{ margin: 0; color: var(--muted); font-size: 14px; }}
@media (max-width: 820px) {{ .two {{ grid-template-columns: 1fr; }} }}
@media (max-width: 640px) {{
  .grid {{ grid-template-columns: 1fr 1fr; }} .dow, .day.blank {{ display: none; }}
  .day {{ min-height: 0; }}
}}
</style>
<div class="wrap">
<header>
  <div class="eyebrow">Instagram · Facebook · X — Oct 24 to Nov 22, 2026</div>
  <h1>dateunoa Content Calendar</h1>
  <p class="lede">Ten reels a day on each channel, every one with an original music bed, selling the three ebooks and the $56 bundle. The first six days are already in Buffer; a daily run writes, renders and schedules each new day seven days ahead, so the queue never runs dry.</p>
  <div class="stats">
    <div class="stat"><b>10</b><span>posts / day / channel</span></div>
    <div class="stat"><b>{total_sched}</b><span>posts already scheduled</span></div>
    <div class="stat"><b>~880</b><span>posts over the month</span></div>
    <div class="stat"><b>7 days</b><span>always queued ahead</span></div>
  </div>
</header>

<section class="two">
  <div>
    <h2>Daily slots</h2>
    <div class="tablebox"><table>
      <thead><tr><th>Time</th><th>Type</th><th>Content</th><th>Sells</th></tr></thead>
      <tbody>{slot_rows}</tbody>
    </table></div>
    <p class="lede" style="margin-top:12px;font-size:13px">Times are Israel time. The same video goes to all three channels; captions are written per network (Instagram gets 5 hashtags, Facebook 3, X a short line under 280 characters).</p>
  </div>
  <div>
    <h2>Weekly themes</h2>
    <ul class="themes">{theme_rows}</ul>
  </div>
</section>

<section>
  <h2>The month</h2>
  <div class="grid">
    <div class="dow">Sun</div><div class="dow">Mon</div><div class="dow">Tue</div><div class="dow">Wed</div><div class="dow">Thu</div><div class="dow">Fri</div><div class="dow">Sat</div>
    {"".join(cells)}
  </div>
  <div class="legend"><span><i style="background:var(--surface);border-color:var(--gold)"></i>Scheduled in Buffer now</span><span><i style="background:var(--auto)"></i>Written and scheduled automatically 7 days ahead</span><span>Promo line = the 14:00 promo reel of the day</span></div>
</section>

<section>
  <h2>Launch week, post by post</h2>
  {"".join(week1)}
</section>

<section>
  <h2>How it keeps running</h2>
  <div class="notes">
    <div class="note"><h3>Every evening</h3><p>The scheduled task writes nine new quotes for the day a week out, renders them with music, and schedules 30 posts in Buffer. It never repeats a quote.</p></div>
    <div class="note"><h3>Every Monday</h3><p>It ranks last week's reels by shares and saves, writes more of what wins, and swaps out a pillar that loses two weeks in a row.</p></div>
    <div class="note"><h3>Instagram</h3><p>Metricool's 6 reels a day run through Oct 25. From Oct 26 Instagram moves to Buffer at 10 a day, so it is never doubled.</p></div>
  </div>
</section>
</div>
'''
Path(sys.argv[1]).write_text(page)
print("ok", len(page))
