from sklearn.feature_extraction.text import CountVectorizer

def create_bow(todos: list):
    documents = [
        f"{todo.title} {todo.description or ''}"
        for todo in todos
        ]
    
    if not any(text.strip() for text in documents):
        return {"vocabulary": [], "vectors": []}
    
    vectorizer = CountVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(documents)
    
    return {
        "vocabulary": vectorizer.get_feature_names_out().tolist(),
        "vectors": matrix.toarray().tolist()
    }