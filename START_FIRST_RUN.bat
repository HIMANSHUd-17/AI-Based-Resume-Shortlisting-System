@echo off
setlocal enabledelayedexpansion
title AI Resume Shortlisting System - First Run Setup
color 0A

cd /d "%~dp0"

echo.
echo ===============================================
echo   🚀 AI Resume Shortlisting System
echo ===============================================
echo.
echo Setting up for FIRST RUN...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found
    echo Install from: https://www.python.org
    echo IMPORTANT: Check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
echo ✅ Python found
echo.

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
    echo.
)

REM Activate
call venv\Scripts\activate.bat

REM Install packages with progress
echo 📥 Installing required packages...
echo    (First run: 3-5 minutes, Subsequent: Instant)
echo.

pip install -q streamlit>=1.32.0 && echo    ✅ Streamlit
pip install -q spacy>=3.7.0 && echo    ✅ spaCy
pip install -q scikit-learn>=1.4.0 && echo    ✅ scikit-learn
pip install -q pdfplumber>=0.10.0 && echo    ✅ pdfplumber
pip install -q python-docx>=1.1.0 && echo    ✅ python-docx
pip install -q pandas numpy plotly && echo    ✅ Data libraries
echo.

REM Download spaCy model
echo 🧠 Downloading spaCy language model...
python -m spacy download en_core_web_sm -q
echo ✅ spaCy model ready
echo.

REM Start app
echo ===============================================
echo ✨ LAUNCHING APPLICATION
echo ===============================================
echo.
echo 🌐 App will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

timeout /t 2
streamlit run app.py

pause
