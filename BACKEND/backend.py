# BACKEND/backend.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from transformers import BertTokenizerFast, BertForSequenceClassification
import torch
import random
import os
from datetime import datetime
from BACKEND.database_auth import DatabaseAuth

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize authentication system
auth = DatabaseAuth()

# Conversation memory to make responses more contextual
conversation_memory = {}

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

# Enhanced emotion-specific empathetic responses with more context and follow-up questions
emotion_responses = {
    "admiration": [
        "That's genuinely inspiring! 🌟 I can feel your enthusiasm. What specifically about this resonated with you?",
        "Wow, that's amazing! 🌟 Your admiration shows you have great taste. How do you think this could influence your own path?",
        "That's so inspiring! 🌟 I love how you notice the good in things. What qualities do you admire most?"
    ],
    "amusement": [
        "Haha, that's absolutely hilarious! 😄 I can picture it now. What was the funniest part for you?",
        "That sounds like such a good time! 😄 Laughter is the best medicine. Did anyone else find it as funny as you did?",
        "Oh my, that's comedy gold! 😄 I love your sense of humor. What else has been making you laugh lately?"
    ],
    "anger": [
        "I can hear how frustrated you are, and that's completely valid. 🔥 What specifically triggered this feeling?",
        "That's really infuriating, I understand why you'd be angry. 🔥 How are you planning to handle this situation?",
        "Your anger is justified here. 🔥 It's okay to feel this way. What would help you feel better right now?"
    ],
    "annoyance": [
        "Ugh, that sounds incredibly frustrating! 😤 I'd be annoyed too. What's the most irritating part about it?",
        "That's really getting under your skin, isn't it? 😤 Sometimes the little things can be the most annoying. How are you coping?",
        "I totally get why that's annoying! 😤 It's the kind of thing that just builds up. What would make this situation better?"
    ],
    "approval": [
        "That's absolutely wonderful! 👍 I can feel your positive energy. What made this feel so right to you?",
        "You're absolutely right to feel good about this! 👍 It sounds like a great decision. What's the next step?",
        "That's fantastic! 👍 Your approval shows you have good judgment. How does this align with your values?"
    ],
    "caring": [
        "You have such a caring heart! ❤️ It's beautiful how much you think about others. Who are you most concerned about right now?",
        "Your caring nature is one of your best qualities! ❤️ How are you taking care of yourself while caring for others?",
        "That's so thoughtful of you! ❤️ Caring people like you make the world better. What inspired this caring feeling?"
    ],
    "confusion": [
        "It's totally normal to feel confused about this. 🤔 What part is most unclear to you?",
        "Confusion can be really frustrating, I get it. 🤔 Sometimes talking it through helps. What would make this clearer?",
        "You're not alone in feeling confused about this. 🤔 What information would help you understand better?"
    ],
    "curiosity": [
        "Your curiosity is infectious! 🔍 I love how you want to learn more. What sparked this interest?",
        "That's such an interesting question! 🔍 Your curiosity shows you're engaged. What would you like to explore first?",
        "I love your inquisitive mind! 🔍 Curiosity leads to amazing discoveries. What's the most intriguing part for you?"
    ],
    "desire": [
        "Your desires tell us about what matters to you! ✨ What makes this so important to you?",
        "That's a beautiful dream! ✨ I can feel your passion. What's the first step toward making this happen?",
        "Your desires are valid and worth pursuing! ✨ What would achieving this mean to you?"
    ],
    "disappointment": [
        "I'm so sorry this didn't work out as you hoped. 💔 Disappointment can really hurt. What were you most looking forward to?",
        "That's really disappointing, and it's okay to feel this way. 💔 What would have made this better?",
        "Your disappointment is completely understandable. 💔 Sometimes things don't go as planned. What's your next move?"
    ],
    "disapproval": [
        "It's okay to not be okay with this. 🌿 Your feelings are valid. What specifically concerns you?",
        "I understand why you'd disapprove. 🌿 Sometimes we need to trust our instincts. What would make this situation better?",
        "Your disapproval shows you have strong values. 🌿 What's the core issue here for you?"
    ],
    "disgust": [
        "That sounds really upsetting and gross. 😖 I can understand why you'd feel that way. What was the worst part?",
        "Ugh, that's disgusting! 😖 Your reaction is completely justified. How are you handling this?",
        "That's really disturbing, I'm sorry you had to experience that. 😖 What would help you feel better?"
    ],
    "embarrassment": [
        "Everyone has embarrassing moments, you're not alone! 😊 What made this feel so embarrassing?",
        "Embarrassment can be really uncomfortable, I know. 😊 But these moments often make the best stories later. What happened?",
        "It's okay to feel embarrassed! 😊 We've all been there. What would make you feel less embarrassed about this?"
    ],
    "excitement": [
        "Your excitement is contagious! 🎉 I can feel your energy! What are you most excited about?",
        "That's so exciting! 🎉 I love your enthusiasm. What's the next step you're looking forward to?",
        "Your excitement is absolutely justified! 🎉 This sounds amazing. How long have you been waiting for this?"
    ],
    "fear": [
        "Fear is a natural response, and it's okay to feel scared. 🛡️ What's making you feel most afraid?",
        "I can hear how frightened you are, and that's completely valid. 🛡️ What would help you feel safer?",
        "Your fear is real and important to acknowledge. 🛡️ Sometimes talking about it helps. What's the worst-case scenario you're worried about?"
    ],
    "gratitude": [
        "Gratitude is such a beautiful emotion! 🙏 What are you most thankful for today?",
        "Your gratitude shows you have a wonderful perspective! 🙏 What inspired this feeling of thankfulness?",
        "That's so heartwarming! 🙏 Gratitude can change everything. How does this make you feel?"
    ],
    "grief": [
        "I'm truly sorry for your loss. 🖤 Grief is one of the hardest emotions to process. Would you like to tell me more about what you're feeling?",
        "Your grief is valid and important. 🖤 There's no right way to grieve. What would be most helpful for you right now?",
        "I can't imagine how difficult this must be. 🖤 Loss changes us forever. What memories bring you comfort?"
    ],
    "joy": [
        "Your joy is absolutely radiant! 😄 I can feel your happiness through your words. What brought you this much joy?",
        "That's wonderful news! 😄 Your joy is contagious! What's the best part about this?",
        "I'm so happy for you! 😄 Joy like this is precious. How long have you been feeling this way?"
    ],
    "love": [
        "Love is one of the most powerful emotions! ❤️ Who or what are you thinking of with such love?",
        "Your love is beautiful and pure! ❤️ Love can transform everything. What makes this love so special?",
        "That's so heartwarming! ❤️ Love is what makes life worth living. How does this love make you feel?"
    ],
    "nervousness": [
        "Nerves are totally normal, especially when something matters to you. 💪 What's making you most nervous?",
        "Your nervousness shows you care! 💪 That's actually a good sign. What would help you feel more confident?",
        "It's okay to feel nervous! 💪 Sometimes nerves mean you're about to do something important. What's the outcome you're hoping for?"
    ],
    "optimism": [
        "Your optimism is inspiring! 🌟 I love your positive outlook. What are you most looking forward to?",
        "That's such a great attitude! 🌟 Optimism can change everything. What makes you feel so hopeful?",
        "Your optimism is contagious! 🌟 I can feel your positive energy. What's driving this hopeful feeling?"
    ],
    "pride": [
        "You absolutely should be proud! 🏆 This is a real achievement. What makes you most proud about this?",
        "Your pride is completely justified! 🏆 You've earned this feeling. How did you accomplish this?",
        "That's something to be really proud of! 🏆 Your hard work paid off. What was the most challenging part?"
    ],
    "realization": [
        "Realizations can be life-changing! 🌈 What did you discover that feels so important?",
        "That's a powerful realization! 🌈 Sometimes the truth hits us suddenly. How does this change things for you?",
        "Your realization sounds significant! 🌈 What led you to this understanding?"
    ],
    "relief": [
        "Relief is such a wonderful feeling! 😌 I can feel your tension releasing. What made you feel so much better?",
        "That's such a relief! 😌 Sometimes the weight lifting off our shoulders is the best feeling. What was worrying you before?",
        "Your relief is palpable! 😌 I'm glad you're feeling better. What changed that brought you this relief?"
    ],
    "remorse": [
        "It's okay to feel remorse, it shows you have a good heart. 🌼 What would you like to talk about?",
        "Remorse is a sign of growth and empathy. 🌼 What's on your mind that you'd like to discuss?",
        "Your remorse shows you care about doing the right thing. 🌼 What would help you feel better about this?"
    ],
    "sadness": [
        "I'm here for you, and it's okay to feel sad. 💙 What's making you feel this way?",
        "Your sadness is valid and important. 💙 Sometimes we need to feel our feelings. What would be most helpful right now?",
        "I can hear how much you're hurting. 💙 You don't have to go through this alone. What's weighing on your heart?"
    ],
    "surprise": [
        "Wow, that's really surprising! 😲 I can feel your shock. What was the most unexpected part?",
        "That's quite a surprise! 😲 Sometimes life throws us curveballs. How are you processing this?",
        "Your surprise is completely understandable! 😲 What were you expecting instead?"
    ],
    "positive": [
        "That's so great to hear! 🌟 Your positive energy is infectious. What's keeping you in such good spirits?",
        "I love your positive outlook! 🌟 It's refreshing to hear such optimism. What's going well for you?",
        "Your positivity is inspiring! 🌟 I can feel your good vibes. What's the highlight of your day?"
    ],
    "negative": [
        "I'm sorry you're going through a tough time. 🤗 What's been most difficult for you?",
        "It's okay to not be okay. 🤗 Sometimes we need to acknowledge the hard times. What would help you feel better?",
        "I hear you, and your feelings are valid. 🤗 What's been weighing on your mind?"
    ],
    "satisfaction": [
        "I'm glad you're feeling satisfied! ✨ That's such a good feeling. What's been going well?",
        "Your satisfaction is well-deserved! ✨ It sounds like things are working out. What made this feel so good?",
        "That's wonderful that you're feeling satisfied! ✨ Sometimes contentment is the best feeling. What's contributing to this?"
    ],
    "jealousy": [
        "Jealousy is a natural emotion, and it's okay to feel it. 💚 What triggered this feeling?",
        "Your jealousy is valid, and it's worth exploring. 💚 What would help you feel less jealous?",
        "Jealousy often points to what we really want. 💚 What's the underlying desire here?"
    ],
    "guilt": [
        "Guilt can be really heavy to carry. 🌼 What would help you forgive yourself?",
        "Your guilt shows you have a conscience, which is a good thing. 🌼 What's bothering you most?",
        "It's okay to feel guilty, but don't let it consume you. 🌼 What would be a healthy way to process this?"
    ],
    "neutral": [
        "I'm here to listen! 🙂 What's on your mind?",
        "Tell me more! 🙂 I'm curious about what you're thinking.",
        "I'm all ears! 🙂 What would you like to talk about?"
    ],
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
    session_id = data.get("session_id", "default")
    print(f"User Message: {user_message}")

    # Initialize conversation memory for this session
    if session_id not in conversation_memory:
        conversation_memory[session_id] = {
            "messages": [],
            "topics": [],
            "emotion_history": []
        }

    # If the user message is very short (like greetings), only then check greeting
    if len(user_message.split()) <= 4 and is_greeting(user_message):
        bot_response = random.choice(greeting_responses)
        predicted_emotion = "greeting"
    else:
        # Use the trained model to predict emotion
        predicted_emotion = predict_emotion(user_message)
        
        # Get enhanced response based on emotion
        if predicted_emotion in emotion_responses:
            # Choose a random response from the emotion-specific responses
            bot_response = random.choice(emotion_responses[predicted_emotion])
        else:
            # Use enhanced fallback responses
            enhanced_fallback_responses = [
                "I'm here for you! 🧡 That sounds really interesting. Tell me more about what's on your mind.",
                "That's fascinating! ✨ I'd love to hear more about your thoughts on this.",
                "I'm listening carefully. 👂 Your perspective is valuable. What else would you like to share?",
                "Thanks for opening up. 🧡 I appreciate you sharing with me. What's the most important part of this for you?",
                "That's really thought-provoking! 🤔 I can tell this matters to you. What would you like to explore further?",
                "I'm curious about your take on this! 🔍 What's your experience been like?",
                "That sounds meaningful to you. 💫 I'd love to understand more about your perspective.",
                "You have such interesting thoughts! 🌟 What's the story behind this?",
            ]
            bot_response = random.choice(enhanced_fallback_responses)

        # Update conversation memory
        conversation_memory[session_id]["messages"].append({
            "user": user_message,
            "bot": bot_response,
            "emotion": predicted_emotion,
            "timestamp": datetime.now().isoformat()
        })
        conversation_memory[session_id]["emotion_history"].append(predicted_emotion)

    return jsonify({
        "user_message": user_message,
        "predicted_emotion": predicted_emotion,
        "bot_response": bot_response,
        "session_id": session_id
    })

# Serve React frontend files
# Authentication endpoints
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name', email.split('@')[0])  # Use email prefix as name if not provided
        
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400
        
        result = auth.register_user(email, password, name)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": f"Registration failed: {str(e)}"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400
        
        result = auth.login_user(email, password)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": f"Login failed: {str(e)}"}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({"success": False, "message": "Session ID is required"}), 400
        
        result = auth.logout_user(session_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": f"Logout failed: {str(e)}"}), 500

@app.route('/api/validate-session', methods=['POST'])
def validate_session():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({"valid": False, "message": "Session ID is required"}), 400
        
        result = auth.validate_session(session_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"valid": False, "message": f"Session validation failed: {str(e)}"}), 500

@app.route('/api/user-profile', methods=['POST'])
def get_user_profile():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({"success": False, "message": "Session ID is required"}), 400
        
        # First validate the session
        session_result = auth.validate_session(session_id)
        if not session_result["valid"]:
            return jsonify({"success": False, "message": "Invalid session"}), 401
        
        # Get user profile
        user_id = session_result["user"]["id"]
        result = auth.get_user_profile(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": f"Failed to get profile: {str(e)}"}), 500

@app.route('/')
def serve_frontend():
    return send_from_directory('../build', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../build', path)

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
