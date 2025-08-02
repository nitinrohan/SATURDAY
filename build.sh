#!/bin/bash

echo "🚀 Building SATURDAY React Frontend..."

# Install Node.js dependencies
echo "📦 Installing dependencies..."
npm install

# Build React app
echo "🔨 Building React app..."
npm run build

# Copy build files to backend directory for serving
echo "📁 Copying build files..."
cp -r build/* BACKEND/build/

echo "✅ Build complete! React app is ready for deployment."
echo "🌐 Start the backend with: python BACKEND/backend.py" 