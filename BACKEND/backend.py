##### backend code


from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Load pre-trained sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis")

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.json
    user_input = data.get("message", "")
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    # Analyze sentiment
    result = sentiment_pipeline(user_input)[0]
    sentiment = result['label']
    
    # Generate chatbot response based on sentiment
    responses = {
        "POSITIVE": "I'm glad to hear that! Tell me more!",
        "NEGATIVE": "I'm sorry you're feeling this way. Want to talk about it?",
        "NEUTRAL": "I see. How else can I assist you?"
    }
    
    bot_response = responses.get(sentiment, "I'm here to listen.")
    
    return jsonify({"sentiment": sentiment, "response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)


