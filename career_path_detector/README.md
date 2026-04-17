 Career Path Detector

Resume parser + career prediction tool. Feed it a PDF, DOCX, or TXT resume and it spits out structured data, a predicted career track, and a CSV you can plug straight into a classifier.

---

## Project Structure
career_path_detector/
│
├── main.py                     ← start here
│
├── extractor/                  ← everything to do with reading resumes
│   ├── init.py
│   ├── text_reader.py          ← PDF / DOCX / TXT → plain text
│   ├── gemini_parser.py        ← sends text to Gemini, gets back structured JSON
│   └── regex_parser.py         ← offline fallback if you don't have an API key
│
├── ml/
│   ├── career_detector.py      ← scores skills against career track profiles
│   └── csv_builder.py          ← flattens everything into a single CSV row
│
├── utils/
│   ├── constants.py            ← skill aliases, experience level thresholds
│   ├── cleaner.py              ← normalizes skills, engineers features
│   └── terminal.py             ← colored output helpers
│
├── requirements.txt
└── README.md
---

## Getting Started

```bash
pip install -r requirements.txt
```

Get a free Gemini API key at https://aistudio.google.com/apikey, then:

```bash
# single resume
python main.py resume.pdf --api-key YOUR_KEY

# whole folder
python main.py --batch ./resumes/ --output results.csv

# no API key — falls back to regex extraction
python main.py resume.pdf
```

You can also set `GEMINI_API_KEY` as an env variable instead of passing it every time.

---

## Output

Produces a CSV with one row per resume. Key columns:

| Column | What it is |
|---|---|
| `top_career_track` | best matching career path |
| `career_predictions` | top 3, pipe-separated |
| `total_experience_years` | calculated from job dates |
| `experience_level` | entry level / junior / mid / senior |
| `technical_skills` | pipe-separated, ready for TF-IDF |
| `has_github` | 1 or 0 |
| `education_level` | bachelor / master / phd / unknown |

---

## Career Tracks

Full-Stack Developer, Frontend Developer, Backend Developer, Data Scientist / ML Engineer, DevOps / Cloud Engineer, Mobile Developer, Cybersecurity Engineer, QA / Test Engineer, Embedded / Systems Engineer, Business Analyst / Product Manager

---

## How It Works
resume file
│
├─ text_reader.py        extract raw text
│
├─ gemini_parser.py      AI → structured JSON  (regex_parser.py if offline)
│
├─ cleaner.py            normalize skills, compute features
│
├─ career_detector.py    score against track profiles → predictions
│
└─ csv_builder.py        write ML-ready CSV
