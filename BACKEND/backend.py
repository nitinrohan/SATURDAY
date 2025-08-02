# BACKEND/backend.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from transformers import BertTokenizerFast, BertForSequenceClassification
import torch
import random
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load model and tokenizer (local files only)
import os
model_path = os.path.join(os.path.dirname(__file__), "trained_emotion_model")

# Check if model files exist
if os.path.exists(model_path):
    try:
        tokenizer = BertTokenizerFast.from_pretrained(model_path, local_files_only=True)
        model = BertForSequenceClassification.from_pretrained(model_path, local_files_only=True)
        model.eval()
        MODEL_LOADED = True
    except Exception as e:
        print(f"Warning: Could not load model from {model_path}: {e}")
        MODEL_LOADED = False
else:
    print(f"Warning: Model directory not found at {model_path}")
    print("Using fallback emotion detection without ML model")
    MODEL_LOADED = False

# Greeting responses
greeting_responses = [
    "Hey there! 👋 How's your day going?",
    "Hello! 😊 Hope you're doing well. How can I support you today?",
    "Hi! ✨ What’s on your mind?",
    "Hey! 🖐️ I'm here for you. How are you feeling today?",
]

# Emotion-specific empathetic responses
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

# Fallback responses if emotion is not found
fallback_responses = [
    "I'm here for you! 🧡 Want to tell me more?",
    "Sounds interesting! ✨ Tell me what’s on your mind.",
    "I'm listening carefully. 👂 Feel free to share more!",
    "Thanks for opening up. 🧡 I'm here for you.",
]

# Detect greetings first
def is_greeting(message):
    message = message.lower()
    greeting_keywords = [
        "hello", "hi", "hey", "good morning", "good evening", "good afternoon",
        "how are you", "greetings", "sup", "yo"
    ]
    return any(word in message for word in greeting_keywords)

# Predict emotion using the fine-tuned BERT model or fallback
def predict_emotion(text):
    if MODEL_LOADED:
        try:
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                outputs = model(**inputs)
            logits = outputs.logits
            predicted_class_id = logits.argmax().item()
            label = model.config.id2label.get(predicted_class_id, "neutral")
            return label
        except Exception as e:
            print(f"Error predicting emotion with model: {e}")
            return fallback_emotion_detection(text)
    else:
        return fallback_emotion_detection(text)

# Fallback emotion detection using keyword matching
def fallback_emotion_detection(text):
    text_lower = text.lower()
    
    # Simple keyword-based emotion detection
    emotion_keywords = {
        "sadness": ["sad", "depressed", "unhappy", "crying", "tears", "lonely", "miss", "lost"],
        "joy": ["happy", "excited", "great", "wonderful", "amazing", "fantastic", "joy", "laugh"],
        "anger": ["angry", "mad", "furious", "hate", "rage", "annoyed", "frustrated"],
        "fear": ["scared", "afraid", "terrified", "worried", "anxious", "nervous", "panic"],
        "love": ["love", "adore", "heart", "romantic", "beautiful", "sweet", "caring"],
        "surprise": ["wow", "omg", "amazing", "incredible", "unbelievable", "shocked"],
        "gratitude": ["thank", "thanks", "grateful", "appreciate", "blessed"],
        "confusion": ["confused", "don't understand", "what", "how", "why", "puzzled"],
        "curiosity": ["curious", "wonder", "interested", "tell me more", "explain"],
        "optimism": ["hope", "optimistic", "positive", "future", "better", "improve"]
    }
    
    for emotion, keywords in emotion_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            return emotion
    
    return "neutral"

# Define the /chat API endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    print(f"User Message: {user_message}")

    # If the user message is very short (like greetings), only then check greeting
    if len(user_message.split()) <= 4 and is_greeting(user_message):
        bot_response = random.choice(greeting_responses)
        predicted_emotion = "greeting"
    else:
        # Use the trained model to predict emotion
        predicted_emotion = predict_emotion(user_message)
        bot_response = emotion_responses.get(predicted_emotion, random.choice(fallback_responses))

    return jsonify({
        "user_message": user_message,
        "predicted_emotion": predicted_emotion,
        "bot_response": bot_response
    })

# Serve frontend files
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
