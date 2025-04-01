#!/bin/bash

echo "🔧 Checking for Homebrew..."
if ! command -v brew &> /dev/null; then
  echo "🚨 Homebrew not found. Installing..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "✅ Homebrew is installed."
fi

echo "🐍 Installing Python via Homebrew..."
brew install python

echo "📁 Creating virtual environment..."
python3 -m venv venv

echo "✅ Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🎉 All set! Virtual environment is ready and dependencies installed."
echo "👉 To activate later, run: source venv/bin/activate"
