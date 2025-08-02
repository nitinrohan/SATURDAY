# 🚀 SATURDAY Chatbot Deployment Guide

This guide will help you deploy your SATURDAY chatbot to the web using various hosting platforms.

## 📋 Prerequisites

1. **GitHub Account**: You'll need to push your code to GitHub
2. **Model Files**: Ensure your `trained_emotion_model` folder is in the `BACKEND/` directory
3. **Dependencies**: All required packages are listed in `requirements.txt`

## 🎯 Recommended: Deploy to Render.com (Free)

### Step 1: Prepare Your Repository

1. Push your code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/SATURDAY.git
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:

   - **Name**: `saturday-chatbot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn BACKEND.backend:app`
   - **Plan**: Free

5. Click "Create Web Service"
6. Wait for deployment (5-10 minutes)

### Step 3: Access Your Website

- Your chatbot will be available at: `https://saturday-chatbot.onrender.com`

## 🌐 Alternative: Deploy to Heroku

### Step 1: Install Heroku CLI

```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Deploy

```bash
heroku login
heroku create saturday-chatbot
git push heroku main
heroku open
```

## 🐳 Alternative: Deploy with Docker

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "BACKEND.backend:app"]
```

### Step 2: Build and Run

```bash
docker build -t saturday-chatbot .
docker run -p 10000:10000 saturday-chatbot
```

## 🔧 Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the backend
cd BACKEND
python backend.py

# Open http://localhost:5000 in your browser
```

## 📁 File Structure for Deployment

```
SATURDAY/
├── BACKEND/
│   ├── backend.py
│   ├── trained_emotion_model/  # Your model files
│   └── ...
├── frontend/
│   ├── index.html
│   └── stylesheets/
├── requirements.txt
├── render.yaml
├── Procfile
├── runtime.txt
└── gunicorn.conf.py
```

## ⚠️ Important Notes

1. **Model Files**: Ensure your `trained_emotion_model` folder is included in your repository
2. **File Size**: If your model is large (>100MB), consider using model hosting services
3. **Environment Variables**: For production, consider adding environment variables for sensitive data
4. **CORS**: The backend is configured to allow CORS for frontend communication

## 🐛 Troubleshooting

### Common Issues:

1. **Model Not Found**: Ensure `trained_emotion_model` folder is in `BACKEND/`
2. **Port Issues**: The app runs on port 10000 in production
3. **Memory Issues**: Free tiers have memory limits; consider upgrading if needed
4. **Build Failures**: Check that all dependencies are in `requirements.txt`

### Debug Commands:

```bash
# Check logs on Render
# Use the Render dashboard

# Check logs on Heroku
heroku logs --tail

# Test locally
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## 🎉 Success!

Once deployed, your empathetic chatbot will be accessible worldwide! Users can:

- Chat with SATURDAY through the web interface
- Get emotion-aware responses
- Experience human-like conversation

## 📞 Support

If you encounter issues:

1. Check the deployment platform's logs
2. Verify all files are properly committed
3. Ensure the model files are included
4. Test locally first

Happy deploying! 🚀
