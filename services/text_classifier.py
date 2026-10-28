from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Training examples
texts = [
    "study Python for exam",
    "prepare mathematics homework",
    "finish university assignment",
    "complete project report",
    "attend work meeting",
    "send email to manager",
    "buy milk and bread",
    "go shopping for groceries",
    "go to the gym",
    "exercise and improve fitness"
]

# Correct categories
labels = [
    "Education",
    "Education",
    "Education",
    "Work",
    "Work",
    "Work",
    "Shopping",
    "Shopping",
    "Health",
    "Health"
]

model = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ("classifier", LogisticRegression())
])

model.fit(texts, labels)

new_todo = ["Prepare for my Python exam"]

prediction = model.predict(new_todo)

print("Predicted category:", prediction[0])