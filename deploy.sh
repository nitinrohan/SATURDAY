#!/bin/bash

echo "🚀 SATURDAY Chatbot Deployment Script"
echo "====================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
    echo "✅ Git repository initialized"
else
    echo "📁 Git repository already exists"
fi

# Check if model files exist
if [ ! -d "BACKEND/trained_emotion_model" ]; then
    echo "⚠️  WARNING: trained_emotion_model folder not found in BACKEND/"
    echo "   Please ensure your model files are in BACKEND/trained_emotion_model/"
    echo "   This is required for the chatbot to work!"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Model files found"
fi

# Test local deployment
echo "🧪 Testing local deployment..."
cd BACKEND
python -c "
import sys
try:
    from backend import app
    print('✅ Backend imports successfully')
except Exception as e:
    print(f'❌ Backend import failed: {e}')
    sys.exit(1)
"
cd ..

echo ""
echo "🎯 Deployment Options:"
echo "1. Deploy to Render.com (Recommended - Free)"
echo "2. Deploy to Heroku"
echo "3. Deploy with Docker"
echo "4. Exit"
echo ""

read -p "Choose an option (1-4): " choice

case $choice in
    1)
        echo "🌐 Deploying to Render.com..."
        echo "📋 Steps:"
        echo "1. Push your code to GitHub:"
        echo "   git remote add origin https://github.com/YOUR_USERNAME/SATURDAY.git"
        echo "   git push -u origin main"
        echo ""
        echo "2. Go to https://render.com and create a new Web Service"
        echo "3. Connect your GitHub repository"
        echo "4. Use these settings:"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: gunicorn BACKEND.backend:app"
        echo "   - Plan: Free"
        echo ""
        echo "5. Click 'Create Web Service'"
        ;;
    2)
        echo "🌐 Deploying to Heroku..."
        echo "📋 Steps:"
        echo "1. Install Heroku CLI"
        echo "2. Run these commands:"
        echo "   heroku login"
        echo "   heroku create saturday-chatbot"
        echo "   git push heroku main"
        echo "   heroku open"
        ;;
    3)
        echo "🐳 Deploying with Docker..."
        echo "📋 Building Docker image..."
        docker build -t saturday-chatbot .
        echo "✅ Docker image built successfully"
        echo ""
        echo "🚀 To run the container:"
        echo "   docker run -p 10000:10000 saturday-chatbot"
        echo ""
        echo "🌐 Access your chatbot at: http://localhost:10000"
        ;;
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment setup complete!"
echo "📖 For detailed instructions, see DEPLOYMENT.md" 