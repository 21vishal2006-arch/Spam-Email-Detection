import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report


# 1. Load dataset
data = pd.read_csv("dataset/spam.csv")

# 2. Convert labels into numbers
data["label"] = data["label"].map({
    "ham": 0,
    "spam": 1
})

# 3. Separate input and output
X = data["message"]
y = data["label"]

# 4. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# 5. Convert text into numerical features
vectorizer = TfidfVectorizer()

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 6. Create ML model
model = MultinomialNB()

# 7. Train model
model.fit(X_train_tfidf, y_train)

# 8. Test model
y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 9. Save model
joblib.dump(model, "model/spam_model.pkl")

# 10. Save TF-IDF vectorizer
joblib.dump(vectorizer, "model/tfidf_vectorizer.pkl")

print("\nModel saved successfully!")