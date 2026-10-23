"""Caption builder for @dateunoa posts on Instagram, Facebook and X (Buffer).

caption(pillar, hook, network, day_index) -> str
"""

BOOK = {"T": "I", "S": "I", "M": "II", "HE": "II", "W": "III", "SHE": "III", "B": "ALL", "PROMO": "ALL"}

LONG = {
    "I": "Still staring at your phone? \"What Do I Text Back?\" gives you the exact words for slow replies, mixed signals & boundaries — without looking needy.",
    "II": "Stop guessing what he means. \"What Do Men Want?\" shows you what he's really looking for, how real interest looks, and what makes him stay.",
    "III": "Send this to him 👀 \"What Do Women Want?\" — what makes her feel safe, what makes her choose you, and the exact texts to send.",
    "ALL": "The dateunoa Collection: \"What Do I Text Back?\", \"What Do Men Want?\" & \"What Do Women Want?\" — all 3 for $56. Buy 2, get 1 free.",
}
SHORT = {
    "I": "The exact words to send: \"What Do I Text Back?\"",
    "II": "What he really means: \"What Do Men Want?\"",
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
CTA = {"instagram": "📲 Link in bio", "facebook": "📲 Get it: link on our page (tap \"Shop now\" / see About)", "twitter": "Link in bio."}


def caption(pillar, hook, network, n=0, promo_text=None):
    book = BOOK[pillar]
    tagsets = TAGS[book]
    tags = tagsets[n % len(tagsets)]
    if network == "twitter":
        body = promo_text if promo_text else f"{hook}\n\n{SHORT[book]}"
        text = f"{body} {CTA['twitter']}\n\n{' '.join(tags[:2])}"
        if len(text) > 275:
            text = f"{body[:275 - 30].rsplit(' ', 1)[0]}… {CTA['twitter']}"
        return text
    body = promo_text if promo_text else f"{hook}\n\n{LONG[book]}"
    ntags = tags if network == "instagram" else tags[:3]
    return f"{body}\n\n{CTA[network]}\n\n{' '.join(ntags)}"
