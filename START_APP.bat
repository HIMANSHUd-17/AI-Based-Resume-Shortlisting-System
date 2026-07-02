@echo off
title AI Resume Shortlisting System

REM Change to the script directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo   🚀 AI Resume Shortlisting System
echo ===============================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
    echo.
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated
echo.

REM Check if requirements are installed
echo 📚 Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo 📥 Installing required packages (this may take a few minutes)...
    pip install -r requirements.txt -q
    echo ✅ Dependencies installed
    echo.
)

REM Download spaCy model if not present
echo 🧠 Checking spaCy model...
python -c "import spacy; spacy.load('en_core_web_sm')" >nul 2>&1
if errorlevel 1 (
    echo 📥 Downloading spaCy language model (this may take a minute)...
    python -m spacy download en_core_web_sm -q
    echo ✅ spaCy model downloaded
    echo.
)

REM Launch Streamlit app
echo ===============================================
echo ✨ Starting Streamlit application...
echo ===============================================
echo.
echo The app will open in your default browser at:
echo 👉 http://localhost:8501
echo.
echo Press Ctrl+C in this window to stop the server
echo.

streamlit run app.py

pause
