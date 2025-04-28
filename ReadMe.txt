SATURDAY 🤖 - Sentiment Aware Chatbot
-------------------------------------

Hi there!   
Welcome to SATURDAY — an empathetic chatbot that understands your emotions and responds like a supportive friend.

This guide explains how to run the project locally.

-------------------------------------
Prerequisites:
-------------------------------------
1. Python 3.8 or higher installed
2. pip package manager installed
3. Git installed (optional, for cloning)

-------------------------------------
Required Python Packages:
-------------------------------------
Install dependencies by running:

    pip install -r requirements.txt

(You must be inside the project root directory where `requirements.txt` is located.)

-------------------------------------
First Time Setup (ONLY if model not trained):
-------------------------------------
- Run the following scripts (in order) to train the model:

1. `emotion_data_preprocessing.py`
   - Prepares the GoEmotions dataset.

2. `train_emotion_model.py`
   - Fine-tunes a BERT model for emotion classification.
   - Saves the model inside `/BACKEND/trained_emotion_model/`

This step is already DONE if you have `trained_emotion_model` folder with saved model files.

-------------------------------------
Running the Chatbot:
-------------------------------------

1. Open terminal inside your project directory.

2. Navigate to BACKEND folder:

    cd BACKEND

3. Run the Flask backend server:

    python backend.py

4. The server will start on:

    http://localhost:5000

5. Open the `FRONTEND/index.html` file in your browser (just double-click it).

Now you can start chatting!

-------------------------------------
Project Structure:
-------------------------------------
TERM-PROJECT/
├── BACKEND/
│   ├── backend.py              # Flask backend server
│   ├── trained_emotion_model/   # Fine-tuned model files
│   ├── emotion_data_preprocessing.py
│   ├── train_emotion_model.py
│   └── evalscript.py
├── FRONTEND/
│   ├── index.html               # Chatbot frontend
│   └── style.css                # Chatbot UI styling
├── DATASETS/
│   └── goemotions_only.csv      # Preprocessed emotions dataset
├── requirements.txt             # Python dependencies
└── README.txt                   # This file!

-------------------------------------
Example Sentences You Can Try:
-------------------------------------

- "I just won the lottery! I'm so thrilled!" (Expect: Joy)
- "My cat is sick, and I feel really down." (Expect: Sadness)
- "Someone cut me off in traffic this morning, and it made me so angry." (Expect: Anger)
- "Honestly, I'm just feeling completely neutral about the whole situation." (Expect: Neutral)
- "Did you hear about the new project? I'm quite curious to learn more." (Expect: Curiosity)

SATURDAY will understand and respond empathetically. 

-------------------------------------
Tips:
-------------------------------------
- Make sure your Flask server (backend.py) is running before using the chatbot.
- If you want to deploy it online later, you can use services like Render, AWS, or Heroku.

