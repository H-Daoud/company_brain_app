#!/bin/bash

echo "📦 Starte Setup für dein OCR+GPT Steuerprojekt..."

# Homebrew prüfen
if ! command -v brew &> /dev/null
then
    echo "❌ Homebrew nicht gefunden. Installiere es zuerst: https://brew.sh/"
    exit 1
fi

echo "✅ Homebrew gefunden."

# Tesseract & Poppler installieren
echo "🔧 Installiere Systemtools..."
brew install tesseract
brew install poppler

# Python-Venv
echo "🐍 Erstelle Python-Virtualenv..."
python3 -m venv venv
source venv/bin/activate

# Pip aktualisieren
pip install --upgrade pip

# Python-Dependencies
echo "📦 Installiere Python-Abhängigkeiten..."
pip install -r requirements.txt

echo "✅ Setup abgeschlossen. Starte z.B. mit:"
echo "   source venv/bin/activate && streamlit run streamlit_invoice_app.py"

#You may want to run the setup script again if you have made changes to the requirements.txt file.
# Make setup.sh executable run ths command  < chmod +x setup.sh >
# You can run this script in your terminal to set up the environment. < ./setup.sh >

