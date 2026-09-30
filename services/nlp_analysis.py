import nltk

def analyze_pos(text: str):

    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)

    return pos_tags
