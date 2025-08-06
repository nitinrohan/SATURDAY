# BACKEND/backend.py

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from transformers import BertTokenizerFast, BertForSequenceClassification
import torch
import random
import os

app = Flask(__name__)
CORS(app)

# Serve frontend
@app.route("/")
def index():
    return render_template("index.html")

# Load model
model_path = os.environ.get(
    "MODEL_PATH",
    os.path.join(os.path.dirname(__file__), "trained_emotion_model"),
)
tokenizer = BertTokenizerFast.from_pretrained(model_path, local_files_only=True)
model = BertForSequenceClassification.from_pretrained(model_path, local_files_only=True)
model.eval()

# Greetings and emotions
greeting_responses = [
    "Hey there! 👋 How's your day going?",
    "Hello! 😊 Hope you're doing well. How can I support you today?",
    "Hi! ✨ What’s on your mind?",
    "Hey! 🖐️ I'm here for you. How are you feeling today?",
]

emotion_responses = {
    "admiration": "That's so inspiring! 🌟 What inspired you the most?",
    "amusement": "Haha, sounds hilarious! 😄 What made you laugh today?",
    "anger": "I hear you. It's okay to feel angry sometimes. 🔥 What happened?",
    "annoyance": "That's really annoying, I understand. 😤 What annoyed you?",
    "approval": "That's wonderful! 👍 What else has been exciting for you?",
    "caring": "You're very thoughtful. ❤️ Who are you thinking about?",
    "confusion": "It's okay to be confused. 🤔 What's on your mind?",
    "curiosity": "Curiosity leads to learning! 🔍 What are you curious about?",
    "desire": "Dreams are powerful. ✨ What do you wish for?",
    "disappointment": "I'm sorry things didn't go well. 💔 Want to talk about it?",
    "disapproval": "It's okay to feel that way. 🌿 What concerns you?",
    "disgust": "That sounds very upsetting. 😖 What exactly happened?",
    "embarrassment": "Everyone feels embarrassed sometimes. 😊 What happened?",
    "excitement": "That's so exciting! 🎉 Tell me more!",
    "fear": "Fear is natural. 🛡️ What made you feel scared?",
    "gratitude": "Gratitude is beautiful. 🙏 What are you thankful for today?",
    "grief": "I'm truly sorry for your loss. 🖤 Would you like to share more?",
    "joy": "That's wonderful news! 😄 What brought you so much joy?",
    "love": "Love is powerful. ❤️ Who or what are you thinking of?",
    "nervousness": "Nerves mean you care. 💪 What's making you nervous?",
    "optimism": "Optimism brightens everything! 🌟 What are you looking forward to?",
    "pride": "You should be proud! 🏆 What achievement makes you proud?",
    "realization": "Realizations change us. 🌈 What did you realize?",
    "relief": "Relief feels great. 😌 What made you feel better?",
    "remorse": "It's okay to feel sorry. 🌼 What would you like to talk about?",
    "sadness": "I'm here for you. 💙 Want to share what's making you sad?",
    "surprise": "Surprises keep life exciting! 😲 What surprised you?",
    "positive": "That's so great to hear! 🌟 What's keeping you positive?",
    "negative": "Sorry to hear that. 🤗 Want to talk about it?",
    "satisfaction": "I'm glad you're feeling satisfied. ✨ What's been going well?",
    "jealousy": "Jealousy is a natural feeling. 💚 What triggered it?",
    "guilt": "Forgive yourself and heal. 🌼 What's bothering you?",
    "neutral": "Alright! 🙂 Tell me more if you want!",
}

fallback_responses = [
    "I'm here for you! 🧡 Want to tell me more?",
    "Sounds interesting! ✨ Tell me what’s on your mind.",
    "I'm listening carefully. 👂 Feel free to share more!",
    "Thanks for opening up. 🧡 I'm here for you.",
]

def is_greeting(message):
    message = message.lower()
    greeting_keywords = [
        "hello", "hi", "hey", "good morning", "good evening", "good afternoon",
        "how are you", "greetings", "sup", "yo"
    ]
    return any(word in message for word in greeting_keywords)

def predict_emotion(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_id = logits.argmax().item()
    label = model.config.id2label.get(predicted_class_id, "neutral")
    return label

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
