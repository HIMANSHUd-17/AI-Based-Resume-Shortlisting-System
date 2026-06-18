@echo off
REM Quick test to verify Python and dependencies
python --version
pip list | find "streamlit"
if errorlevel 1 (
    echo.
    echo Installing dependencies...
    pip install -q -r requirements.txt
    python -m spacy download en_core_web_sm -q
)
echo.
echo Starting app...
echo.
streamlit run app.py
pause
