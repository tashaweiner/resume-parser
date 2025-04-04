#!/bin/bash

echo "🔧 Setting up backend environment..."

# Step 1: Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "📁 Creating virtual environment..."
  python3 -m venv venv
fi

# Step 2: Activate virtual environment
source venv/bin/activate
echo "✅ Virtual environment activated"

# Step 3: Install dependencies
if [ -f "requirements.txt" ]; then
  echo "📦 Installing dependencies..."
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "⚠️ No requirements.txt found!"
fi

# Step 4: Ensure .env exists
if [ ! -f ".env" ]; then
  echo "🔐 Creating .env file..."
  echo "OPENAI_API_KEY=sk-REPLACE_ME" > .env
  echo "⚠️ Don't forget to replace your OPENAI_API_KEY in the .env file"
else
  echo "🔑 .env file already exists"
fi

echo "🚀 Backend setup complete. Run with:"
echo "   source venv/bin/activate && uvicorn main:app --reload"
