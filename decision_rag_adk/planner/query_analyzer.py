import re

INTENT_RULES = {
    "precedent": {
        "keywords": [
            "holding", "binding", "controlling", "precedent",
            "majority opinion", "concurrence", "dissent", "plurality",
            "join", "coalition", "opinion", "vote",
        ],
        "patterns": [
            r"who joined",
            r"which justices",
            r"vote \d+-\d+",
        ],
    },
    "marks": {
        "keywords": [
            "marks", "narrowest ground", "controlling opinion",
            "narrowest rationale",
        ],
        "patterns": [
            r"marks v\.?\s*united",
        ],
    },
    "compliance": {
        "keywords": [
            "satisfy", "predicate", "requirement", "elements",
            "precondition", "statutory authority", "within the scope",
            "balance of payments", "section 122", "legal basis",
            "authorized", "lawful", "meets the", "comply",
        ],
        "patterns": [
            r"does .+ satisfy",
            r"is .+ authorized",
            r"meet the .+ requirement",
        ],
    },
    "commentary_assessment": {
        "keywords": [
            "national review", "mccarthy", "whelan", "mclaughlin",
            "bench memos", "the corner", "commentary", "media",
            "assess claims", "external analysis",
        ],
        "patterns": [
            r"assess .+ claims",
            r"evaluate .+ argument",
        ],
    },
    "factual_summary": {
        "keywords": [
            "what happened", "summarize", "overview", "background",
            "facts of", "explain",
        ],
        "patterns": [
            r"what (did|does) the .+ (say|hold|decide)",
        ],
    },
}


def analyze_query(query_text):
    lower = query_text.lower()
    intents = {}
    triggered_rules = []
    matched_keywords = []

    for intent_name, rules in INTENT_RULES.items():
        hit = False
        for kw in rules["keywords"]:
            if kw in lower:
                hit = True
                matched_keywords.append(kw)
                triggered_rules.append(
                    {"intent": intent_name, "type": "keyword", "match": kw}
                )
        for pat in rules["patterns"]:
            m = re.search(pat, lower)
            if m:
                hit = True
                triggered_rules.append(
                    {"intent": intent_name, "type": "pattern", "match": m.group()}
                )
        intents[intent_name] = hit

    if not any(intents.values()):
        intents["factual_summary"] = True
        triggered_rules.append(
            {"intent": "factual_summary", "type": "fallback", "match": "no intent matched"}
        )

    return {
        "intents": intents,
        "keywords": matched_keywords,
        "triggered_rules": triggered_rules,
    }
