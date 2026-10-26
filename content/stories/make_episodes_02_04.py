"""Writes content/stories/ep02-ep04 (episode.json + episode.md + dm.json) for the dateunoa story reels.
Every episode ends on an open loop: the key message and the reply appear as hidden bubbles,
and the comment keyword delivers them (plus the ending) by DM."""
import json
import os

R = os.path.dirname(os.path.abspath(__file__))
STYLE = "Stylized 3D animated feature-film look, soft cinematic lighting, shallow depth of field, vertical 9:16."
SILENT = "No dialogue, mouth closed, no talking. No on-screen text, no subtitles, no watermark."
MUSIC = "../../../tools/music/music_0{}.m4a"


def shot(setting, chars, action, camera, silent=SILENT):
    body = ""
    if chars.strip():
        c = chars.strip()
        body = c + ("" if c.endswith((",", ";")) else ",") + " " + action.strip()
    elif action.strip(" ."):
        body = action.strip()
    cam = camera.strip().rstrip(".") + "."
    return "\n".join(x for x in [STYLE, setting, body, cam, silent] if x)


def T(text, a, b, y=260, style="thought"):
    return {"text": text, "start": a, "end": b, "style": style, "y": y}


EPS = []

# ---------------------------------------------------------------- EP02
NOOR = ("NOOR, a woman in her late 20s with shoulder-length straight black hair held by a small gold hair clip, "
        "light brown skin, an emerald-green satin midi dress, small gold hoop earrings")
APT = "A small, tidy apartment in the evening, warm lamp light, a dresser with a round mirror, a grey couch, a front door in the background."
EPS.append(dict(
    id="ep02", title="Read at 10:48", keyword="TEXT", book="What Do I Text Back?", music=4,
    logline=("Noor is ready at 8 for a date who never shows. At 11:42 she stops waiting and sends one sentence. "
             "At midnight he replies, and her face changes. The video never shows either message."),
    cast=[NOOR, "KARIM appears only as a phone contact."],
    shots=[
        ("s1", "hailuo-2.3-fast 6s", shot(APT, NOOR, "stands at the mirror putting on lipstick, smiling with excitement, then glances at her phone on the dresser.",
                                          "Medium shot from the side, slow push-in"), [0, 4.5], [T("8:00 PM. He said he'd pick me up.", 0.3, 4.3)]),
        ("s2", "hailuo-2.3-fast 6s", shot(APT, NOOR, "sits on the edge of the grey couch with her purse on her lap, glancing at the front door; her excited smile slowly fades.",
                                          "Wide shot, static"), [0, 4.5], [T("9:15 PM.", 0.3, 4.3)]),
        ("s3", "hailuo-2.3-fast 6s", shot("The same apartment, now darker, only the lamp and the glow of a phone.", NOOR,
                                          "looks down at her phone, its light on her face; her eyes become glassy and she swallows hard.",
                                          "Close-up on her face, slow push-in"), [0.5, 5], [T("He read it. Nothing.", 0.3, 4.2)]),
        ("phone",),
        ("s4", "kling-3.0 8s (hero)", shot("The apartment at night, lamp light, she sits on the couch.", NOOR,
                                          "reads a new message on her phone; her eyes widen, she slowly covers her mouth with one hand, then a small, knowing smile appears.",
                                          "Close-up on her face, the phone screen faces away from the camera, slow push-in"), [0.5, 6], [T("She didn't expect that.", 0.4, 5.2)]),
        ("s5", "hailuo-2.3-fast 6s", shot("Close view of a coffee table at night, a phone lying face-down, its edges glowing as new messages keep arriving, lamp light, her hand resting next to it.",
                                          "", "", "Static close-up"), [0, 5], [T("Comment TEXT for her message and his reply", 0.4, 5.0, 640, "cta")]),
    ],
    phone=dict(type="phone", contact="Karim", duration=14.0,
               history=[["stamp", "Today 6:02 PM"], ["them", "Pick you up at 8"], ["me", "Can't wait!"],
                        ["stamp", "10:47 PM"], ["me", "Hey, are you still coming?"], ["stamp", "Read 10:48 PM"]],
               events=[{"type": "draft", "text": "Did something happen?? Are you mad at me? I've been ready since 8 and I just don't understand why you",
                        "start": 0.8, "end": 4.6},
                       {"type": "send", "hidden": True, "text": "I was looking forward to tonight. I'm not going to wait by the phone. Take care.",
                        "start": 5.0, "end": 7.4},
                       {"type": "typing", "start": 9.0, "end": 11.2},
                       {"type": "receive", "hidden": True, "text": "You're right. I messed up. Tomorrow, 8 PM. I'll be at your door at 7:55.", "at": 11.2}],
               captions=[T("No. Not this time.", 3.9, 5.0, 1000), T("11:42 PM. One sentence.", 7.4, 9.0, 1085),
                         T("12:03 AM. He replied.", 11.4, 14.0, 1085)]),
    reveal_intro="Here's what she sent, and what he replied 🤍",
    reveal=[("Her (11:42 PM)", "I was looking forward to tonight. I'm not going to wait by the phone. Take care."),
            ("Him (12:03 AM)", "You're right. I messed up. Tomorrow, 8 PM. I'll be at your door at 7:55.")],
    ending="He knocked at 7:50. With flowers. She never had to chase him again.",
    why=("She didn't beg, accuse or ask why. She said how she felt and stopped waiting, on her terms. "
         "Calm boundaries get respect; long paragraphs get left on read."),
    hook="She was ready at 8. He read it at 10:48. At 11:42 she sent one sentence. 🌙",
    cta_long="Comment TEXT and I'll send you her message and his reply 👇",
    tags_ig="#datingadvice #selfrespect #situationship #relationships #textingtips",
))

# ---------------------------------------------------------------- EP03
AMARA = ("AMARA, a woman in her early 30s with dark brown skin, short natural coily hair, a silver nose ring, "
         "an oversized soft grey sweatshirt")
DANIEL = "DANIEL, a man in his early 30s with light brown skin, short black hair, a faded denim jacket"
LOFT = ("A cozy small apartment at night full of plants, an easel with a half-finished colorful painting, "
        "a warm floor lamp, a big window with city lights.")
EPS.append(dict(
    id="ep03", title="1:07 AM", keyword="REPLY", book="What Do I Text Back?", music=5,
    logline=("Four months after Daniel walked out without a word, Amara has rebuilt her peace. At 1:07 AM: 'I miss you.' "
             "She deletes the paragraph and sends one sentence. His answer makes her cry. The video never shows either."),
    cast=[AMARA, DANIEL + " (only in a memory shot)"],
    shots=[
        ("s1", "hailuo-2.3-fast 6s", shot(LOFT, AMARA, "paints with a small brush, humming, relaxed and content, a mug of tea beside her.",
                                          "Medium shot, slow push-in"), [0, 4.5], [T("4 months since he left.", 0.3, 4.3)]),
        ("s2", "hailuo-2.3-fast 6s", shot(LOFT, AMARA, "freezes mid-brushstroke as her phone on the side table lights up; she slowly turns to look at it, her calm face tightening.",
                                          "Medium close-up, static"), [0, 4.5], [T("1:07 AM.", 0.3, 4.3)]),
        ("s3", "hailuo-2.3-fast 6s", shot("Memory: the same apartment months earlier, cool blue desaturated light, emptier.", DANIEL,
                                          "walks out the front door with a duffel bag over his shoulder without looking back; the door closes.",
                                          "Wide shot from inside the room, static, dreamy soft focus"), [0, 4.5], [T("The night he left without a word.", 0.3, 4.3)]),
        ("phone",),
        ("s4", "kling-3.0 8s (hero)", shot(LOFT, AMARA, "sits on the floor against the couch reading her phone; a single tear rolls down her cheek, she presses her lips together, then lets out a long shaky breath and almost smiles.",
                                          "Close-up on her face, the phone screen faces away from the camera, slow push-in"), [0.5, 6], [T("She never expected him to say that.", 0.4, 5.2)]),
        ("s5", "hailuo-2.3-fast 6s", shot("The window sill with plants at night, city lights outside, a phone lying face-down glowing softly next to a pot.",
                                          "", "", "Static close-up"), [0, 5], [T("Comment REPLY for what she said and what he answered", 0.4, 5.0, 640, "cta")]),
    ],
    phone=dict(type="phone", contact="Daniel", duration=14.0,
               history=[["stamp", "Today 1:07 AM"], ["them", "hey"], ["them", "I miss you"]],
               events=[{"type": "draft", "text": "You miss me?? I missed you every single day for months and you never once checked if I was okay, and now you just",
                        "start": 0.7, "end": 4.8},
                       {"type": "send", "hidden": True, "text": "I'm glad you're okay. I'm not going back to what we were.", "start": 5.2, "end": 7.2},
                       {"type": "typing", "start": 8.4, "end": 11.0},
                       {"type": "receive", "hidden": True, "text": "I know. I didn't text to get you back. I texted to say sorry for how I left. You deserved a goodbye.", "at": 11.0}],
               captions=[T("She almost sent the paragraph.", 3.9, 5.2, 1000), T("She sent one sentence instead.", 7.2, 8.4, 1000),
                         T("Then he answered.", 11.2, 14.0, 1000)]),
    reveal_intro="Here's what she sent, and what he answered 🤍",
    reveal=[("Her (1:09 AM)", "I'm glad you're okay. I'm not going back to what we were."),
            ("Him (1:12 AM)", "I know. I didn't text to get you back. I texted to say sorry for how I left. You deserved a goodbye.")],
    ending="She wrote back: \"Thank you. I hope you find peace too.\" Then she slept better than she had in four months.",
    why=("One calm sentence closed the door without a fight. No history lesson, nothing for him to argue with. "
         "And it left room for the apology she was owed."),
    hook="4 months of healing. Then 1:07 AM: \"I miss you.\" 🌙",
    cta_long="Comment REPLY and I'll send you what she said and what he answered 👇",
    tags_ig="#datingadvice #healing #movingon #relationships #selfrespect",
))

# ---------------------------------------------------------------- EP04
THEO = ("THEO, a man in his mid 30s with light skin, short sandy-brown hair, a neatly trimmed beard, round glasses, "
        "a navy cardigan over a white t-shirt")
LILY = "his daughter LILY, about 7 years old, with two brown braids and a yellow raincoat"
SOFIA = "SOFIA, a woman in her mid 30s with olive skin, dark wavy hair in a low bun, small star earrings, a sage-green apron"
CAFE = "A small sunny neighborhood café on a Saturday morning, wooden counter, pastries in a glass case, plants, soft morning light."
EPS.append(dict(
    id="ep04", title="Same order, every Saturday", keyword="ASK", book="What Do Women Want?", music=6,
    logline=("Every Saturday Theo almost asks the café owner out and orders the same thing instead. His daughter has seen enough. "
             "He finally says it, and we only see her face. That night she texts him. We never see what she said."),
    cast=[THEO, LILY, SOFIA],
    shots=[
        ("s1", "hailuo-2.3-fast 6s", shot(CAFE + f" Behind the counter stands {SOFIA}.", f"{THEO}, who stands at the counter holding hands with {LILY};",
                                          "Sofia smiles at him; Theo takes a breath as if about to say something, hesitates, then just points at the menu, a little embarrassed.",
                                          "Medium shot from the side of the counter"), [0, 5], [T("Every Saturday. Same order.", 0.3, 4.7)]),
        ("s2", "hailuo-2.3-fast 6s", shot(CAFE, SOFIA, "laughs warmly while making a hot chocolate with whipped cream, glancing up at the customer with a kind smile.",
                                          "Close-up on Sofia, shallow depth of field"), [0, 4.5], [T("Same almost.", 0.3, 4.2)]),
        ("s3", "hailuo-2.3-fast 6s", shot(CAFE + f" At a small table by the window sits {THEO}.", f"Opposite him, {LILY}",
                                          "looks from her father to the counter, rolls her eyes playfully, then gives him a determined thumbs-up and points toward the counter; her father looks surprised.",
                                          "Medium shot, static"), [0, 5], [T("His daughter had seen enough.", 0.3, 4.7)]),
        ("s4", "hailuo-2.3-fast 6s", shot(CAFE + f" Behind the counter stands {SOFIA}.", THEO,
                                          "walks back to the counter, takes a breath, leans in slightly and speaks to her quietly with a nervous but warm smile, his words drowned out by the hiss of the espresso machine.",
                                          "Medium shot over Sofia's shoulder, on Theo",
                                          silent="No audible dialogue. No on-screen text, no subtitles, no watermark."), [0, 5], [T("He finally said it.", 0.3, 4.7)]),
        ("s5", "kling-3.0 8s (hero)", shot(CAFE, SOFIA, "is surprised, puts one hand over her heart, her eyes go soft and shiny, and she starts to smile, but the shot ends before she answers.",
                                          "Close-up on Sofia, slow push-in, morning light"), [0.5, 5.5], []),
        ("s6", "hailuo-2.3-fast 6s", shot(CAFE, f"At the window table, {LILY}", "holds both hands up with crossed fingers, eyes squeezed shut, hoping.",
                                          "Medium close-up, static"), [0, 4], []),
        ("phone",),
        ("s7", "hailuo-2.3-fast 6s", shot("A quiet neighborhood street at dusk, the café with warm lights glowing, autumn leaves on the pavement.",
                                          "", "", "Wide shot, static"), [0, 5], [T("Comment ASK for his exact words and her answer", 0.4, 5.0, 640, "cta")]),
    ],
    phone=dict(type="phone", contact="Sofia (café)", duration=8.0,
               history=[["stamp", "Today 8:14 PM"]],
               events=[{"type": "typing", "start": 0.6, "end": 2.6},
                       {"type": "receive", "hidden": True, "text": "Yes. Friday at 7. And I have to tell you something about every Saturday :)", "at": 2.6}],
               captions=[T("That night, she texted him.", 0.4, 2.6, 1000), T("He read it three times.", 3.6, 8.0, 1000)]),
    reveal_intro="Here are the exact words he used, and her answer 🤍",
    reveal=[("Him, at the counter", "Sofia, would you like to have dinner with me on Friday? Just the two of us."),
            ("Her, that night", "Yes. Friday at 7. And I have to tell you something about every Saturday :)")],
    ending="At dinner she told him: every Saturday, she made his coffee a little slower, hoping he'd finally ask.",
    why=("It's clear (dinner, Friday, a date, not 'we should hang out sometime'), it's kind, and it's easy to answer either way. "
         "Clarity is what makes a woman feel safe saying yes."),
    hook="Every Saturday he almost asked. His daughter had seen enough. ☕",
    cta_long="Comment ASK and I'll send you his exact words and her answer 👇",
    tags_ig="#datingadviceformen #whatwomenwant #confidence #lovestory #relationships",
))


for ep in EPS:
    d = os.path.join(R, ep["id"])
    os.makedirs(d + "/shots", exist_ok=True)
    scenes, prompts = [], []
    for sh in ep["shots"]:
        if sh[0] == "phone":
            scenes.append(ep["phone"])
            continue
        sid, model, prompt, trim, caps = sh
        scenes.append({"type": "clip", "src": f"shots/{sid}.mp4", "trim": trim, "captions": caps})
        prompts.append((sid, model, prompt))
    spec = {"title": ep["title"], "keyword": ep["keyword"], "size": [720, 1280], "fps": 30, "target_seconds": [35, 45],
            "music": MUSIC.format(ep["music"]), "music_volume": [0.15, 0.6], "scenes": scenes}
    json.dump(spec, open(f"{d}/episode.json", "w"), indent=1, ensure_ascii=False)
    est = sum((sc["trim"][1] - sc["trim"][0]) if sc["type"] == "clip" else sc["duration"] for sc in scenes)
    cost = sum(141 if "hailuo" in m else 500 for _, m, _ in prompts)
    kw = ep["keyword"]
    dm = [ep["reveal_intro"], ""] + [f"{who}: \"{msg}\"" for who, msg in ep["reveal"]] + \
         ["", ep["ending"], "", f"Why it works: {ep['why']}", "",
          f"The words come from \"{ep['book']}\". All 3 dateunoa ebooks are in my bio if you want the rest."]
    md = [f"# {ep['id']}: {ep['title']}", "",
          f"**Logline:** {ep['logline']}", "",
          f"**Keyword:** {kw} · **Book:** {ep['book']} · **Length:** about {est:.0f} s · **Krea cost:** about {cost} credits (+ retakes)", "",
          "**Open loop:** the key messages appear only as hidden bubbles. The video never shows the words or the ending; the DM does.", "",
          "## Cast (copy word for word into every prompt)", *[f"- {c}" for c in ep["cast"]], "",
          "## Shot prompts", ""]
    for sid, model, prompt in prompts:
        md += [f"### {sid} ({model})", "```", prompt, "```", ""]
    md += ["## Phone scene", f"Contact **{ep['phone']['contact']}**, {ep['phone']['duration']} s, defined in `episode.json` "
           "(hidden bubbles; free preview with `--only phone`).", "",
           f"## DM reply (send to everyone who comments {kw})", "```", *dm, "```", "",
           "## Post captions",
           f"**Instagram:** {ep['hook']}\n\n{ep['cta_long']}\n\n{ep['tags_ig']}", "",
           f"**Facebook:** {ep['hook']}\n\n{ep['cta_long']}\n\n{' '.join(ep['tags_ig'].split()[:3])}", "",
           f"**X:** {ep['hook']} Reply {kw} and I'll DM you how it ended. #datingadvice #relationships", ""]
    open(f"{d}/episode.md", "w").write("\n".join(md))
    json.dump({"keyword": kw, "dm": "\n".join(dm)}, open(f"{d}/dm.json", "w"), indent=1, ensure_ascii=False)
    print(ep["id"], f"{est:.1f}s", cost)
