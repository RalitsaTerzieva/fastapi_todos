import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def preprocess_text(text: str):
    """
    Complete NLP preprocessing pipeline.
    """

    text = text.lower()

    text = re.sub(r"[^\w\s]", "", text)

    tokens = word_tokenize(text)

    filtered_tokens = [
        token
        for token in tokens
        if token not in stop_words
    ]

    lemmas = [
        lemmatizer.lemmatize(token, pos="v")
        for token in filtered_tokens
    ]

    return {
        "clean_text": text,
        "tokens": tokens,
        "filtered_tokens": filtered_tokens,
        "lemmas": lemmas,
    }