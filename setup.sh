#!/bin/bash

# Personal Life OS - Simple Setup Script
# Rachel - Just run this file to get everything set up!

echo ""
echo "================================"
echo "Personal Life OS Setup"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ from python.org"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed. Please install pip or upgrade Python."
    exit 1
fi

echo "✅ pip found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo "   (This may take a minute...)"
echo ""

pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Dependencies installed successfully!"
else
    echo ""
    echo "❌ Failed to install dependencies. Please try manually:"
    echo "   pip3 install -r requirements.txt"
    exit 1
fi

echo ""
echo "================================"
echo "Setup Complete! 🎉"
echo "================================"
echo ""
echo "To start the app, run:"
echo "   python3 app.py"
echo ""
echo "Then open your browser to:"
echo "   http://localhost:5000"
echo ""
echo "Happy mind-dumping! 🧠"
echo ""
