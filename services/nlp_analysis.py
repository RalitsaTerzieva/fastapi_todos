import nltk
from nltk.tree import Tree

def analyze_pos(text: str):

    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)

    return pos_tags

def analyze_ner(text: str):
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)

    ner_tree = nltk.ne_chunk(pos_tags)

    entities = []

    for item in ner_tree:
        if isinstance(item, Tree):
            entity_text = " ".join(
                word for word, tag in item.leaves()
            )

            entities.append({
                "text": entity_text,
                "label": item.label()
            })

    return entities
