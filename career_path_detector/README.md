# 🎯 Career Path Detector

An AI-powered resume parser and career path prediction system.
Upload a resume (PDF / DOCX / TXT) and get:
- **Structured data extraction** (skills, experience, education, projects)
- **Career track prediction** (Full-Stack, ML Engineer, DevOps, etc.)
- **ML-ready CSV output** for training classifiers

---

## 📁 Project Structure

```
career_path_detector/
│
├── main.py                     ← CLI entry point (run this)
│
├── extractor/                  ← Resume text extraction
│   ├── __init__.py             ← Public API: extract_resume()
│   ├── text_reader.py          ← PDF / DOCX / TXT → raw text
│   ├── gemini_parser.py        ← Gemini AI → structured JSON
│   └── regex_parser.py         ← Offline regex fallback
│
├── ml/                         ← Machine learning pipeline
│   ├── __init__.py
│   ├── career_detector.py      ← Career path scoring & prediction
│   └── csv_builder.py          ← Flatten resume → ML-ready CSV row
│
├── utils/                      ← Shared utilities
│   ├── __init__.py
│   ├── constants.py            ← SKILL_MAP, EXPERIENCE_LEVEL_MAP
│   ├── cleaner.py              ← Normalize & engineer features
│   └── terminal.py             ← Colored terminal output
│
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get a FREE Gemini API key
Visit → https://aistudio.google.com/apikey

### 3. Run on a single resume
```bash
python main.py resume.pdf --api-key YOUR_KEY
```

### 4. Run in batch mode (entire folder)
```bash
python main.py --batch ./resumes/ --output results.csv
```

### 5. Run offline (no API key — regex fallback)
```bash
python main.py resume.pdf
```

---

## 📊 Output CSV Columns

| Column | Description |
|---|---|
| `top_career_track` | Highest-scoring predicted career path |
| `career_predictions` | Top 3 predictions (pipe-separated) |
| `total_experience_years` | Computed years of experience |
| `experience_level` | entry level / junior / mid level / senior |
| `num_skills` | Total unique skills detected |
| `technical_skills` | Pipe-separated technical skills |
| `all_skills` | All skills combined (for TF-IDF) |
| `has_github` | 1 if GitHub profile found, else 0 |
| `education_level` | bachelor / master / phd / unknown |

---

## 🤖 Career Tracks Detected

- Full-Stack Developer
- Frontend Developer
- Backend Developer
- Data Scientist / ML Engineer
- DevOps / Cloud Engineer
- Mobile Developer
- Cybersecurity Engineer
- QA / Test Engineer
- Embedded / Systems Engineer
- Business Analyst / Product Manager

---

## 🧠 How It Works

```
Resume File (PDF/DOCX/TXT)
        │
        ▼
 extractor/text_reader.py      ← Extract raw text
        │
        ▼
 extractor/gemini_parser.py    ← AI → structured JSON
   (or regex_parser.py)        ← Offline fallback
        │
        ▼
 utils/cleaner.py              ← Normalize skills, compute features
        │
        ├──► ml/career_detector.py  ← Predict career paths
        │
        └──► ml/csv_builder.py      ← Save ML-ready CSV
```

---

## 📦 Tech Stack

- **Python 3.11+**
- **Google Gemini 2.0 Flash** (free tier)
- **pdfplumber / pypdf** for PDF reading
- **python-docx** for Word documents
- **pandas** for CSV output

---

## 🙋 Author

Built as a final-year CS project for career path detection using AI/ML.
