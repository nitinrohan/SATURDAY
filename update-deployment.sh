#!/bin/bash

echo "🔄 Updating SATURDAY Website with React Frontend"
echo "================================================"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Download from: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm found"

# Install dependencies
echo "📦 Installing React dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Build React app
echo "🔨 Building React app..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Failed to build React app"
    exit 1
fi

# Create build directory in backend
echo "📁 Preparing build files..."
mkdir -p BACKEND/build

# Copy build files
cp -r build/* BACKEND/build/

echo "✅ React build completed successfully!"

# Commit and push changes
echo "🚀 Deploying to GitHub..."
git add .
git commit -m "Add React frontend with modern UI and animations"
git push origin main

echo ""
echo "🎉 Deployment Update Complete!"
echo "=============================="
echo ""
echo "Your website will be updated automatically:"
echo "• Render.com: Automatic redeploy in progress"
echo "• Heroku: Automatic redeploy in progress"
echo "• Other platforms: Check your deployment dashboard"
echo ""
echo "New features:"
echo "• ✨ Modern React frontend with animations"
echo "• 🎨 Glassmorphism design with blur effects"
echo "• 📱 Responsive design for all devices"
echo "• 🚀 Enhanced user experience"
echo ""
echo "Check your deployment platform for the updated website!" 