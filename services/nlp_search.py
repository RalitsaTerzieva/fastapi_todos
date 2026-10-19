from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_todos(query: str, todos: list, limit: int = 5):
    if not query.strip() or not todos:
        return []
    
    documents = [
        f"{todo.title} {todo.description or ''}"
        for todo in todos
        ]
    
    # Fit TF-IDF on this user's task collection.
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(documents + [query])

    # Compare the query with every task.
    scores = cosine_similarity(matrix[-1],
        matrix[:-1]).flatten()
    
    ranked_indices = scores.argsort()[::-1]

    results = []
    for index in ranked_indices:
        score = float(scores[index])

        if score <= 0:
            continue

        results.append({
            "todo": todos[index],
            "similarity": round(score, 3)
        })

        if len(results) >= limit:
            break

    return results


