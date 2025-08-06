from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from transformers import BertTokenizerFast, BertForSequenceClassification
import torch
import random
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)

# Load model and tokenizer
model_path = os.environ.get(
    "MODEL_PATH",
    os.path.join(os.path.dirname(__file__), "trained_emotion_model")
)
tokenizer = BertTokenizerFast.from_pretrained(model_path, local_files_only=True)
model = BertForSequenceClassification.from_pretrained(model_path, local_files_only=True)
model.eval()

# Serve frontend
@app.route("/")
def serve_index():
    return send_from_directory("../frontend", "index.html")

# Serve CSS/JS/images
@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory("../frontend", path)

# Greeting responses and emotion dictionary (same as before)...


greeting_responses = [ ... ]
emotion_responses = { ... }
fallback_responses = [ ... ]

def is_greeting(message):
    ...

def predict_emotion(text):
    ...

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if len(user_message.split()) <= 4 and is_greeting(user_message):
        bot_response = random.choice(greeting_responses)
        predicted_emotion = "greeting"
    else:
        predicted_emotion = predict_emotion(user_message)
        bot_response = emotion_responses.get(predicted_emotion, random.choice(fallback_responses))
    return jsonify({
        "user_message": user_message,
        "predicted_emotion": predicted_emotion,
        "bot_response": bot_response
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
