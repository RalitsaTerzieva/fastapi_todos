from services.nlp_service import preprocess_text

CATEGORY_KEYWORDS = {
    "Study": {
        "learn",
        "study",
        "course",
        "python",
        "react",
        "fastapi",
        "redis",
        "book",
        "read",
    },
    "Shopping": {
        "buy",
        "milk",
        "eggs",
        "grocery",
        "store",
        "shop",
        "amazon",
    },
    "Work": {
        "meeting",
        "deploy",
        "jira",
        "ticket",
        "client",
        "feature",
        "project",
        "bug",
        "review",
    },
    "Health": {
        "doctor",
        "dentist",
        "gym",
        "exercise",
        "walk",
        "medicine",
    },
}


def classify_todo(title: str, description: str):

    processed = preprocess_text(title + " " + description)

    lemmas = processed["lemmas"]

    category = "Personal"

    for category_name, words in CATEGORY_KEYWORDS.items():
        if any(word in words for word in lemmas):
            category = category_name
            break

    keywords = list(set(lemmas))

    return {
        "category": category,
        "keywords": keywords,
        "analysis": processed,
    }