"""Caption builder for @dateunoa posts on Instagram, Facebook and X (Buffer).

caption(pillar, hook, network, day_index) -> str
"""

BOOK = {"T": "I", "S": "I", "M": "II", "HE": "II", "W": "III", "SHE": "III", "B": "ALL", "PROMO": "ALL"}

LONG = {
    "I": "Still staring at your phone? \"What Do I Text Back?\" gives you the exact words for slow replies, mixed signals & boundaries — without looking needy.",
    "II": "Stop guessing what he means. \"What Do Men Want?\" helps you tell attention from commitment, say what you want, and ask about intentions.",
    "III": "Send this to him 👀 \"What Do Women Want?\" shows men how to show interest clearly, ask her out without pressure, and text without games.",
    "ALL": "The dateunoa Collection: \"What Do I Text Back?\", \"What Do Men Want?\" & \"What Do Women Want?\" — all 3 for $56. Buy 2, get 1 free.",
}
SHORT = {
    "I": "The exact words to send: \"What Do I Text Back?\"",
    "II": "Less guessing: \"What Do Men Want?\"",
    "III": "What she really wants: \"What Do Women Want?\"",
    "ALL": "All 3 ebooks for $56. Buy 2, get 1 free.",
}
TAGS = {
    "I": [["#datingadvice", "#textingtips", "#mixedsignals", "#situationship", "#relationshipadvice"],
          ["#datingtips", "#situationships", "#overthinking", "#selfrespect", "#moderndating"],
          ["#textingadvice", "#datinglife", "#relationshipquotes", "#knowyourworth", "#dating"]],
    "II": [["#whatmenwant", "#datingadviceforwomen", "#relationshipgoals", "#healthyrelationships", "#datingtips"]],
    "III": [["#whatwomenwant", "#datingadviceformen", "#mensadvice", "#relationshipadvice", "#modernromance"]],
    "ALL": [["#datingadvice", "#ebook", "#relationshipadvice", "#datingtips", "#selflove"]],
}
PROMO_CAPTIONS = {
 "men_cover": "NEW: \"What Do Men Want?\" 🖤 Tell attention from commitment, say what you want, and ask about intentions without the guesswork.",
 "women_cover": "NEW: \"What Do Women Want?\" 🖤 For men: show interest clearly, ask her out without pressure, and handle a no with dignity.",
 "bundle": "The dateunoa Collection 📚 \"What Do I Text Back?\" + \"What Do Men Want?\" + \"What Do Women Want?\" — all 3 for $56 (instead of $84). Buy 2, get 1 free.",
 "men_page": "A look inside \"What Do Men Want?\" 👀 18 scripts for asking what he wants, saying what you need, and stepping back with grace.",
 "women_page": "A look inside \"What Do Women Want?\" 👀 17 scripts for starting conversations, asking her out and repairing a misstep.",
 "textback": "\"What Do I Text Back?\" 📱 The exact words for slow replies, mixed signals, ghosting & boundaries — without looking needy.",
 "men_page2": "Inside \"What Do Men Want?\" 👀 Always texting, never planning? One honest question beats a hundred screenshots.",
 "women_page2": "Inside \"What Do Women Want?\" 👀 Confidence isn't smooth lines. It's steady, ordinary behavior. Chapter 3 shows how.",
}

CTA = {"instagram": "📲 All 3 ebooks: link in bio", "facebook": "📲 All 3 ebooks: link in our page intro", "twitter": "All 3: link in bio."}

# Every caption markets the whole collection (3 ebooks), led by the book that fits the post.
COLLECTION = ("📚 The dateunoa Collection, 3 dating ebooks:\n"
              "• What Do I Text Back?\n• What Do Men Want?\n• What Do Women Want?")
COLLECTION_X = "3 dating ebooks: What Do I Text Back? · What Do Men Want? · What Do Women Want?"


TITLES = ("What Do I Text Back?", "What Do Men Want?", "What Do Women Want?")


def caption(pillar, hook, network, n=0, promo_text=None):
    book = BOOK[pillar]
    named_all = bool(promo_text) and all(t in promo_text for t in TITLES)
    tagsets = TAGS[book]
    tags = tagsets[n % len(tagsets)]
    if network == "twitter":
        lead = promo_text if promo_text else hook
        coll = "" if named_all else f"{COLLECTION_X} "
        text = f"{lead}\n\n{coll}{CTA['twitter']}\n\n{' '.join(tags[:2])}"
        if len(text) > 275:
            text = f"{lead}\n\n{COLLECTION_X} {CTA['twitter']}"
        if len(text) > 275:
            text = f"{lead[:275 - len(COLLECTION_X) - 30].rsplit(' ', 1)[0]}…\n\n{COLLECTION_X} {CTA['twitter']}"
        return text
    if promo_text:
        body = promo_text
    elif book == "ALL":
        body = hook
    else:
        body = f"{hook}\n\n{LONG[book]}"
    ntags = tags if network == "instagram" else tags[:3]
    coll = "" if named_all else f"{COLLECTION}\n\n"
    return f"{body}\n\n{coll}{CTA[network]}\n\n{' '.join(ntags)}"
