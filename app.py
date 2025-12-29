import os
import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from flask import Flask, request, jsonify
from flask_cors import CORS

# ===============================
# FILE PATHS (Step 8.3)
# ===============================
UNKNOWN_FILE = "unknown_questions/unknown_questions.txt"
CHAT_FILE = "chat_history/chat_history.txt"

# ===============================
# NLTK DATA DOWNLOAD
# ===============================
nltk.download('punkt')
nltk.download('stopwords')

# ===============================
# FLASK APP SETUP
# ===============================
app = Flask(__name__)
CORS(app)

# ===============================
# LOAD INTENTS
# ===============================
with open("intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# ===============================
# CHATBOT LOGIC
# ===============================
def chatbot_response(user_input):
    # Tokenize user input
    user_tokens = [
        w for w in word_tokenize(user_input.lower())
        if w.isalnum() and w not in stopwords.words('english')
    ]

    # Try matching intents
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            pattern_tokens = [
                w for w in word_tokenize(pattern.lower())
                if w.isalnum() and w not in stopwords.words('english')
            ]

            if set(pattern_tokens).intersection(user_tokens):
                return random.choice(intent["responses"])

    # ===============================
    # STEP 8.4 – SAVE UNKNOWN QUESTION
    # ===============================
    with open(UNKNOWN_FILE, "a", encoding="utf-8") as f:
        f.write(user_input + "\n")

    return "Sorry, I don't have an answer yet. Your question has been recorded."

# ===============================
# FLASK ROUTE
# ===============================
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    reply = chatbot_response(user_message)

    # ===============================
    # STEP 8.5 – SAVE CHAT HISTORY
    # ===============================
    with open(CHAT_FILE, "a", encoding="utf-8") as f:
        f.write(f"User: {user_message}\nBot: {reply}\n\n")

    return jsonify({"reply": reply})

# ===============================
# RUN APPLICATION
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
