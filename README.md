# 🧠 AI-Based Resume Shortlisting System

An intelligent AI-powered web application that automatically shortlists candidates by analyzing resumes against job descriptions using NLP and machine learning.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Download spaCy Language Model
```powershell
python -m spacy download en_core_web_sm
```

### Step 3: Run the Application
```powershell
streamlit run app.py
```

✅ **The app will open at:** `http://localhost:8501`

---

## ✨ Features

- ✅ **Multi-Format Resume Upload** - Accept PDF and DOCX files
- ✅ **Intelligent Skill Extraction** - Detect 150+ technical and soft skills using spaCy NER
- ✅ **Smart Job Description Parsing** - Auto-detect required skills from job descriptions
- ✅ **AI-Powered Scoring** - TF-IDF + cosine similarity for accurate matching
- ✅ **Weighted Ranking** - Combines skill match, document similarity, and experience
- ✅ **Beautiful Dashboard** - Modern Streamlit UI with interactive visualizations
- ✅ **Export Results** - Download shortlisted candidates as CSV
- ✅ **Experience Detection** - Automatically extract years of experience

---

## 📊 How It Works

### Input
- Paste a job description
- Upload resume files (PDF/DOCX)
- Skills auto-detected from JD

### Processing
1. Extract text from resumes
2. Extract: name, education, experience, skills
3. Calculate TF-IDF similarity to job description
4. Compute skill match percentage
5. Apply weighted scoring formula
6. Rank candidates by final score

### Output
- Ranked candidate list with scores
- Found vs. missing skills
- Education and experience info
- Interactive score chart
- CSV export with all details

---

## 💯 Scoring Formula

```
Final Score = min(Base Score + Experience Bonus, 100%)

Base Score = (TF-IDF × 50%) + (Skill Match % × 40%)

Experience Bonus:
  - 10% if experience ≥ 3 years
  - 5% if experience ≥ 1 year
  - 0% otherwise
```

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (interactive web UI)
- **NLP**: spaCy (Named Entity Recognition)
- **ML**: scikit-learn (TF-IDF, cosine similarity)
- **PDF**: pdfplumber
- **DOCX**: python-docx
- **Data**: pandas, numpy
- **Charts**: plotly

---

## 📁 Project Structure

```
AI-Based-Resume-Shortlisting-System/
├── app.py                    # Main Streamlit application
├── parser.py                 # PDF & DOCX text extraction
├── ner.py                    # NLP skill & info extraction
├── scorer.py                 # Scoring algorithm
├── skills_list.py            # 150+ skills database
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── APP_README.md             # Detailed app documentation
└── resumes/                  # Folder for uploaded resumes
```

---

## 📋 Skills Database

The system includes **150+ skills** covering:

- **Programming**: Python, Java, C++, JavaScript, TypeScript, R, Go, Rust, PHP, Ruby, Scala, MATLAB, Kotlin, Swift, Perl, Groovy, Haskell, Elixir, Clojure

- **Web Development**: HTML, CSS, React, Angular, Vue, Node.js, Django, Flask, FastAPI, REST API, GraphQL, Bootstrap, Tailwind, Express, Spring Boot, ASP.NET

- **Data Science & ML**: Machine Learning, Deep Learning, NLP, Computer Vision, TensorFlow, PyTorch, Keras, scikit-learn, Pandas, NumPy, Matplotlib, Seaborn, OpenCV, NLTK, spaCy, Hugging Face, LLM, Generative AI

- **Databases**: SQL, MySQL, PostgreSQL, MongoDB, SQLite, Firebase, Redis, Oracle, Cassandra, DynamoDB, Elasticsearch, Neo4j, Snowflake, BigQuery, Redshift

- **DevOps/Cloud**: Git, Docker, Kubernetes, AWS, Azure, GCP, Linux, CI/CD, Jenkins, Terraform, Ansible, Prometheus, Grafana, ELK Stack

- **Soft Skills**: Communication, Leadership, Teamwork, Problem Solving, Agile, Scrum, Project Management, Time Management

---

## ⚙️ System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, Linux
- **RAM**: 2GB minimum (4GB recommended)
- **Disk**: 500MB for dependencies + spaCy model

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: Run `pip install -r requirements.txt`

### Issue: "spaCy model not found"
**Solution**: Run `python -m spacy download en_core_web_sm`

### Issue: "Port 8501 already in use"
**Solution**: Run `streamlit run app.py --server.port 8502`

### Issue: "PDF extraction returns empty text"
**Cause**: PDF contains only images (not text)
**Solution**: Use text-based PDFs for best results

### Issue: App takes long time to start
**Cause**: First run loads spaCy model
**Solution**: This is normal, subsequent runs are faster

---

## 💡 Usage Tips

1. **Sample Job Description**: The app comes with a pre-filled Data Scientist JD for testing
2. **Batch Processing**: For best results, upload 3-5 resumes at a time
3. **Large Files**: First run takes 5-10 seconds (model loading), subsequent runs are 2-3 seconds per resume
4. **Skills Customization**: Edit `skills_list.py` to add more skills
5. **Scoring Weights**: Modify `scorer.py` to adjust scoring formula

---

## 📈 Performance

- **Startup**: 5-10 seconds (first run), 2-3 seconds (subsequent)
- **Per Resume**: 2-5 seconds (depends on file size)
- **10 Resumes**: 20-50 seconds total
- **Memory**: ~500MB-1GB while running

---

## 🎯 Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Download model: `python -m spacy download en_core_web_sm`
3. Run app: `streamlit run app.py`
4. Paste a job description and upload resumes
5. Click "Rank Resumes" and view results
6. Download CSV with ranked candidates

---

## 📖 More Information

For detailed documentation, see **APP_README.md**

---

## 🎉 You're All Set!

Everything is ready to run. Just follow the 3 quick start steps above and you'll have a fully functional AI resume shortlister!

**Happy Resume Shortlisting! 🚀**