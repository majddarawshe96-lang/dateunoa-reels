"""@masculinepack week 1 (Oct 27 - Nov 2, 2026). 3 reels a day at 09:30, 15:00, 21:15 (Asia/Jerusalem).

Each post: (kind, quote_or_promo_id, mood, caption_body)
  kind "q": X-style quote reel; mood picks the music (dark, epic, stoic, grind)
  kind "p": promo reel for The Iron Code (promo ids in PROMOS)
"""

PROMOS = {
    "p1": "Nobody taught you\nhow to be a man.\n\nSo we wrote it down.",
    "p2": "12 laws.\n30 days.\nA different man.",
    "p3": "Discipline. Frame. Purpose.\nWomen. Money. Brotherhood.\n\nOne code.",
}

DAYS = {
    "2026-10-27": [
        ("q", "Nobody is coming to save you.\n\nNot a woman.\nNot a mentor.\nNot luck.\n\nWake up. Train. Build. Repeat.", "dark",
         "Most men spend their twenties waiting. Waiting for motivation, for the right woman, for a lucky break.\n\nIt never comes. Not because life is unfair, but because nobody else is responsible for your life.\n\nThe moment you accept that, everything gets simpler. You stop waiting. You start building."),
        ("q", "If she only texts you\nwhen she's bored,\nyou're not her man.\n\nYou're her entertainment.", "dark",
         "Pay attention to WHEN she reaches out, not just that she does.\n\nInterest shows up on ordinary days, not only when she has nothing better to do.\n\nA man who knows his value notices the pattern and stops making himself available on demand. No anger. No speech. He just gets busy with his own life."),
        ("q", "Men don't get respected\nfor being nice.\n\nThey get respected\nfor being reliable,\ncalm under pressure,\nand impossible to manipulate.", "stoic",
         "Nice is easy. Anyone can be nice when it costs nothing.\n\nRespect comes from what you do when it costs you something: keeping your word, staying calm when others panic, and holding your line when people push.\n\nBe kind. But be solid first."),
    ],
    "2026-10-28": [
        ("q", "Your body is the only place\nyou'll ever live.\n\nStop treating it like a rental.", "grind",
         "Bad sleep. Junk food. No training. Endless scrolling at 2 a.m.\n\nThen we wonder why we feel tired, anxious and unmotivated.\n\nYour energy, mood and confidence all start in your body. Lift heavy things. Sleep 7-9 hours. Eat real food. Walk every day. The basics, done for years, change everything."),
        ("p", "p1", "epic",
         "Nobody sat you down and taught you how to be a man. So we wrote it down.\n\n📕 THE IRON CODE: 12 laws of discipline, frame and purpose, plus the 30-Day Iron Protocol with daily trackers and worksheets.\n\nOwnership. Discipline. Your mind. Your body. Frame. Speech. Boundaries. Confidence. Mission. Money. Brotherhood. Women.\n\nOne payment. Yours forever."),
        ("q", "Stop explaining yourself to people\nwho already decided\nto misunderstand you.", "stoic",
         "You don't owe everyone a defense.\n\nSome people aren't asking questions to understand you. They're asking so they can argue.\n\nSay it once. Say it clearly. Then let your actions do the rest of the talking."),
    ],
    "2026-10-29": [
        ("q", "The man who can sit alone\nwith his thoughts\nis more dangerous than the man\nwho always needs a crowd.", "stoic",
         "Most men can't sit in silence for ten minutes without reaching for their phone.\n\nBut the man who is comfortable alone doesn't need validation, doesn't fear rejection, and can't be controlled by people who threaten to leave.\n\nLearn to enjoy your own company. It's the root of real confidence."),
        ("q", "Double texting a woman\nwho left you on read\nisn't confidence.\n\nIt's begging with extra steps.", "dark",
         "She saw it. She chose not to reply. That IS the reply.\n\nYou don't need to send \"??\" or \"hello?\" or a paragraph about how you feel.\n\nMatch the energy. Put your phone down. Go train, go build, go see your friends. Your attention is valuable. Stop giving it to people who aren't asking for it."),
        ("q", "Discipline is doing it\nwhen you don't feel like it.\n\nThat's the whole secret.\nThat's why most men never find it.", "grind",
         "Motivation is a mood. It comes and goes like the weather.\n\nDiscipline is a decision you already made before the mood showed up.\n\nYou don't train because you feel like it. You train because it's Monday. That's it. That's the difference between the man you are and the man you want to be."),
    ],
    "2026-10-30": [
        ("q", "A man with a mission\ndoesn't have time to wonder\nwho she's talking to.", "epic",
         "When a woman becomes your entire world, you start checking your phone, overthinking every reply and bending your life around her mood.\n\nThat's not love. That's an empty schedule.\n\nBuild something that matters to you. A man with a mission is calmer, more interesting and far more attractive than a man waiting for a text."),
        ("p", "p2", "epic",
         "12 laws. 30 days. A different man.\n\n📕 THE IRON CODE is the book nobody gave you: how to own your life, build discipline that lasts, guard your mind, build your body, hold your frame, set boundaries, earn real confidence, find your mission, handle money, build a brotherhood, and become the man worth choosing.\n\nIncludes the 30-Day Iron Protocol, daily trackers and worksheets."),
        ("q", "Broke. Out of shape.\nAddicted to his phone.\nAnd still wondering why life\nisn't giving him anything.\n\nBrother. Start with you.", "dark",
         "Harsh? Maybe. But somebody needs to say it.\n\nLife doesn't owe you a woman, a career or respect. You build those.\n\nStart small. Cut the scrolling. Get in the gym. Learn one skill that pays. In a year you won't recognize yourself."),
    ],
    "2026-10-31": [
        ("q", "Speak less.\nObserve more.\nReact slower.\n\nThe calmest man in the room\nis usually the one in control of it.", "stoic",
         "Men who react to everything are easy to read and easy to control.\n\nThe man who pauses, listens and responds when he's ready is the one people trust and respect.\n\nNext time someone tries to provoke you, take one full breath before you answer. Watch what changes."),
        ("q", "She can lose interest in you.\n\nYou can't lose interest in yourself.", "epic",
         "Rejection hurts. A breakup hurts. Being ignored hurts.\n\nBut the worst move is letting it stop your training, your work and your growth.\n\nKeep building. Keep your standards. The man you're becoming is bigger than one person's opinion of you."),
        ("q", "Every day you're either\nbuilding or decaying.\n\nThere is no standing still.", "grind",
         "Muscles you don't use get weaker. Skills you don't practice fade. Money you don't manage disappears.\n\nNothing in a man's life stays the same on its own.\n\nPick one thing today that builds you, and do it before you do anything else."),
    ],
    "2026-11-01": [
        ("q", "Your circle is a forecast\nof your future.\n\nLook at the five men\nyou spend the most time with.\n\nThat's who you're becoming.", "epic",
         "If your friends only talk about women, drama and what they'll do \"one day\", that's the ceiling you're living under.\n\nFind men who train, build and push you. Go where they are: the gym, the club, the business meetup.\n\nIron sharpens iron. Choose your iron."),
        ("p", "p3", "epic",
         "Discipline. Frame. Purpose. Women. Money. Brotherhood. One code.\n\n📕 THE IRON CODE: 12 laws with 46 practical exercises, plus the 30-Day Iron Protocol to make them who you are.\n\nNot motivation you'll forget by lunch. A system you'll actually live."),
        ("q", "It's okay to break down.\n\nIt's not okay to stay down.\n\nFeel it. Fix it. Move.", "stoic",
         "Strong men feel everything: grief, anger, fear, heartbreak.\n\nThe difference is that they don't let it drive the car. They feel it, talk to someone they trust, train it out, write it down, and then they get back up.\n\nYou're allowed to fall. You're not allowed to make the floor your home."),
    ],
    "2026-11-02": [
        ("q", "Don't chase her.\n\nTake the attention you give her\nand give it to your goals.\n\nThe right one will notice.", "dark",
         "Chasing tells her she's the prize and you're the one trying to qualify.\n\nBuilding tells her you have a life worth joining.\n\nBe interested, be clear, ask her out like a man. Then if she's not matching your effort, step back and get back to work."),
        ("q", "Nobody respects a man\nwho doesn't keep\nthe promises he makes to himself.", "grind",
         "You said you'd wake up at 6. You said you'd train today. You said you'd quit.\n\nEvery broken promise to yourself teaches your brain one thing: this guy doesn't follow through.\n\nStart with small promises and keep them every single day. That's where real confidence comes from."),
        ("q", "One day you'll be the old man.\n\nMake sure he's proud\nof what you did with his body,\nhis time,\nand his name.", "epic",
         "Every choice you make today is a gift or a debt to the man you'll be in 40 years.\n\nThe workouts. The money you saved. The skills you built. The promises you kept. The people you treated well.\n\nLive in a way he'll thank you for."),
    ],
}
