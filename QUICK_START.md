# 🚀 Quick Start Guide

## Option 1: **FASTEST** - Double-click the batch file

1. **Navigate to your project folder:**
   ```
   c:\Users\himan\Documents\GitHub\AI-Based-Resume-Shortlisting-System
   ```

2. **Double-click `START_APP.bat`**
   - Everything starts automatically
   - App opens at `http://localhost:8501`
   - First run: 2-3 minutes (installs dependencies)
   - Subsequent runs: ⚡ Instant

## Option 2: Manual Start (Advanced)

```powershell
cd "c:\Users\himan\Documents\GitHub\AI-Based-Resume-Shortlisting-System"

# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run app
streamlit run app.py
```

## 📋 Project Files

✅ **Core Files** (Ready to use)
- `app.py` - Main Streamlit application
- `ner.py` - NLP processing
- `parser.py` - PDF/DOCX extraction
- `scorer.py` - Scoring algorithm
- `skills_list.py` - 200+ skills database
- `requirements.txt` - Dependencies

✅ **Config Files**
- `.gitignore` - Git ignore rules
- `.gitattributes` - Git LFS config
- `README.md` - Full documentation

✅ **Launchers**
- `START_APP.bat` - Batch launcher
- `START_APP.ps1` - PowerShell launcher

📹 **Assets**
- `assets/OUTPUT.mp4` - Demo video

## 🎯 How to Use

1. **Paste Job Description** - Fill in the left panel
2. **Auto-detect Skills** - Skills auto-detect from JD
3. **Upload Resumes** - Upload PDF/DOCX files
4. **Click "🚀 Rank Resumes"** - Run analysis
5. **Download Results** - Export as CSV

## ⚡ Performance

- **Setup Time**: ~2-3 minutes (first time only)
- **App Load**: ~3-5 seconds
- **Single Resume Analysis**: ~1-2 seconds
- **10 Resumes**: ~10-20 seconds

## 🐛 Troubleshooting

### Python not found
- Install from https://www.python.org
- ✅ Check "Add Python to PATH"

### Port 8501 already in use
```powershell
streamlit run app.py --server.port 8502
```

### Dependencies won't install
```powershell
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### spaCy model error
```powershell
python -m spacy download en_core_web_sm
```

## 📊 Features

✅ Auto-detect skills from job description
✅ Extract candidate names, education, experience
✅ TF-IDF + Skill matching scoring
✅ Beautiful rankings with visualizations
✅ Export to CSV with all metrics
✅ Support PDF and DOCX resumes
✅ Up to 200MB file size
✅ Responsive UI design

---

**Ready?** Just double-click `START_APP.bat` and you're done! 🎉
