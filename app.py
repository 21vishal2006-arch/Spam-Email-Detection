from flask import Flask, render_template, request, jsonify
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load("model/spam_model.pkl")

# Load the TF-IDF vectorizer
vectorizer = joblib.load("model/tfidf_vectorizer.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    subject = data.get("subject", "")
    body = data.get("body", "")

    email_text = subject + " " + body

    if not email_text.strip():
        return jsonify({
            "error": "Please enter an email."
        }), 400

    # Convert email text into TF-IDF features
    email_vector = vectorizer.transform([email_text])

    # Make prediction
    prediction = model.predict(email_vector)[0]

    # Get confidence
    probabilities = model.predict_proba(email_vector)[0]
    confidence = max(probabilities) * 100

    if prediction == 1:
        result = "SPAM"
        description = "This email appears to be spam."
    else:
        result = "NOT SPAM"
        description = "This email appears to be legitimate."

    return jsonify({
        "result": result,
        "confidence": round(confidence, 2),
        "description": description
    })


if __name__ == "__main__":
    app.run(debug=True)