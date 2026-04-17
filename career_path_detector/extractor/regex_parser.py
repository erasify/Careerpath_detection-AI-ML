"""
extractor/regex_parser.py
──────────────────────────
Offline fallback extractor — no API key required.
Scans resume text using curated keyword lists and regex patterns
to extract skills, education, experience, certifications, and contact info.

Less accurate than Gemini, but works 100% offline.
"""

import re


# ── Skill Keyword Libraries ───────────────────────────────────────────────────

KNOWN_TECHNICAL = {
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "c", "ruby",
    "go", "golang", "rust", "swift", "kotlin", "scala", "r", "matlab",
    "perl", "php", "bash", "shell", "powershell", "dart", "lua", "elixir",
    "haskell", "julia",
    # Web
    "html", "css", "html5", "css3", "sass", "less", "bootstrap", "tailwind",
    "jquery", "xml", "json", "rest", "restful", "graphql", "soap", "ajax",
    # Frontend frameworks
    "react", "react.js", "vue", "vue.js", "angular", "next.js", "nuxt",
    "svelte", "redux", "webpack", "vite", "gatsby",
    # Backend frameworks
    "node.js", "express", "django", "flask", "fastapi", "spring", "laravel",
    "rails", "asp.net", ".net", "fastify", "nestjs", "fiber",
    # Databases
    "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis", "cassandra",
    "dynamodb", "firebase", "supabase", "oracle", "mariadb", "elasticsearch",
    "neo4j", "influxdb",
    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "github actions", "gitlab ci", "ci/cd", "nginx", "apache",
    "linux", "ubuntu", "centos", "bash scripting",
    # ML / AI / Data
    "machine learning", "deep learning", "neural networks", "nlp",
    "computer vision", "data science", "data analysis", "data engineering",
    "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "xgboost",
    "lightgbm", "hugging face", "openai", "langchain", "llm",
    "pandas", "numpy", "matplotlib", "seaborn", "plotly", "scipy",
    "spark", "hadoop", "airflow", "kafka", "dbt", "tableau", "power bi",
    "excel", "google sheets",
    # Mobile
    "android", "ios", "react native", "flutter", "xamarin",
    # Testing
    "pytest", "jest", "selenium", "cypress", "unit testing", "tdd", "bdd",
    "postman", "junit", "mocha",
    # Security
    "cybersecurity", "penetration testing", "ethical hacking", "owasp",
    "firewalls", "vpn", "ssl", "tls", "encryption",
    # Networking
    "tcp/ip", "dns", "http", "https", "networking", "cisco", "juniper",
    # Other
    "git", "github", "gitlab", "bitbucket", "jira", "confluence", "agile",
    "scrum", "kanban", "microservices", "api", "sdk", "oop", "mvc",
    "design patterns", "algorithms", "data structures",
}

KNOWN_SOFT = {
    "leadership", "communication", "teamwork", "problem solving",
    "critical thinking", "time management", "adaptability", "creativity",
    "collaboration", "attention to detail", "project management",
    "decision making", "conflict resolution", "mentoring", "presentation",
    "analytical", "organizational", "self-motivated", "multitasking",
    "interpersonal", "negotiation", "customer service", "public speaking",
}

KNOWN_TOOLS = {
    "vs code", "visual studio", "intellij", "pycharm", "eclipse",
    "android studio", "xcode", "sublime", "atom", "vim", "neovim", "emacs",
    "photoshop", "illustrator", "figma", "sketch", "canva", "adobe xd",
    "notion", "trello", "asana", "slack", "teams", "zoom", "discord",
    "linux", "windows", "macos", "unix",
    "heroku", "netlify", "vercel", "digitalocean", "cloudflare",
    "github", "gitlab", "bitbucket",
    "jupyter", "colab", "anaconda", "spyder",
}

KNOWN_SPOKEN_LANGUAGES = {
    "english", "urdu", "hindi", "arabic", "french", "spanish", "german",
    "chinese", "mandarin", "japanese", "korean", "portuguese", "russian",
    "turkish", "punjabi", "sindhi", "bengali", "persian", "italian",
    "dutch", "polish", "swedish", "norwegian", "danish", "greek",
}

CERT_PATTERNS = [
    r"\baws\s+certified[\w\s]+",
    r"\bgoogle\s+certified[\w\s]+",
    r"\bmicrosoft\s+certified[\w\s]+",
    r"\bcisco\s+\w+\b",
    r"\bpmp\b", r"\bpmp®\b",
    r"\bcertified\s+[\w\s]+professional\b",
    r"\bscrum\s+master\b",
    r"\bcomptia\s+\w+",
    r"\bceh\b", r"\boscp\b",
    r"\bsix\s+sigma\b",
    r"\bpython\s+certificate\b",
    r"\btensorflow\s+developer\b",
]

DEGREE_PATTERNS = {
    r"\bb\.?sc\.?\b|\bbachelor\b|\bbs\b":       "Bachelor",
    r"\bm\.?sc\.?\b|\bmaster\b|\bms\b|\bmba\b": "Master",
    r"\bph\.?d\.?\b|\bdoctorate\b":             "PhD",
    r"\bassociate\b":                            "Associate",
    r"\bdiploma\b":                              "Diploma",
}

JOB_TITLE_KEYWORDS = [
    "engineer", "developer", "programmer", "analyst", "designer", "architect",
    "manager", "consultant", "scientist", "researcher", "intern", "lead",
    "director", "officer", "specialist", "administrator", "coordinator",
    "technician", "support", "devops", "qa", "tester", "security",
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _match_keywords(text_lower: str, keyword_set: set) -> list:
    found = []
    for kw in keyword_set:
        pattern = r"(?<![a-z])" + re.escape(kw) + r"(?![a-z])"
        if re.search(pattern, text_lower):
            found.append(kw)
    return sorted(set(found))


def _extract_year_near(text: str, pat: str):
    m = re.search(pat, text, re.IGNORECASE)
    if not m:
        return None
    snippet = text[max(0, m.start() - 20): m.end() + 80]
    years = re.findall(r"\b(19|20)\d{2}\b", snippet)
    return years[-1] if years else None


# ── Main Extractor ────────────────────────────────────────────────────────────

def extract_basic_regex(text: str) -> dict:
    """
    Parse a resume using regex and keyword matching only.
    Returns a dict in the same schema as gemini_parser.extract_with_gemini().
    """
    text_lower = text.lower()
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # ── Contact info ──
    emails   = re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)
    phones   = re.findall(r"(\+?[\d][\d\s\-().]{7,}\d)", text)
    linkedin = re.findall(r"linkedin\.com/in/[\w\-]+", text, re.IGNORECASE)
    github   = re.findall(r"github\.com/[\w\-]+", text, re.IGNORECASE)
    websites = re.findall(r"https?://(?!linkedin|github)[^\s,]+", text, re.IGNORECASE)

    # ── Skills ──
    technical_skills = _match_keywords(text_lower, KNOWN_TECHNICAL)
    soft_skills      = _match_keywords(text_lower, KNOWN_SOFT)
    tools            = _match_keywords(text_lower, KNOWN_TOOLS)
    spoken_languages = _match_keywords(text_lower, KNOWN_SPOKEN_LANGUAGES)

    # ── Education ──
    education = []
    for pattern, degree_label in DEGREE_PATTERNS.items():
        if re.search(pattern, text_lower):
            match = re.search(pattern + r"[\w\s,.()\-]{0,60}", text, re.IGNORECASE)
            education.append({
                "degree": degree_label,
                "field_of_study": None,
                "institution": match.group().strip() if match else None,
                "location": None,
                "start_date": None,
                "end_date": _extract_year_near(text, pattern),
                "gpa": None,
                "honors": None,
            })

    # ── Experience ──
    experience = []
    for line in lines:
        if any(kw in line.lower() for kw in JOB_TITLE_KEYWORDS) and len(line) < 80:
            years = re.findall(r"\b(19|20)\d{2}\b", line)
            experience.append({
                "job_title": line,
                "company": None,
                "location": None,
                "start_date": years[0] if len(years) > 0 else None,
                "end_date": years[1] if len(years) > 1 else None,
                "responsibilities": [],
                "achievements": [],
            })

    # ── Certifications ──
    certifications = []
    for pat in CERT_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            certifications.append({"name": m.group().strip(), "issuer": None, "date": None})

    # ── Projects ──
    PROJECT_RE = re.compile(
        r"(?:projects?|portfolio)\s*[:\-]?\s*\n((?:.+\n?){1,20})", re.IGNORECASE
    )
    projects = []
    pm = PROJECT_RE.search(text)
    if pm:
        for proj_line in pm.group(1).splitlines():
            proj_line = proj_line.strip()
            if proj_line and len(proj_line) > 5:
                projects.append({"name": proj_line, "description": None, "technologies": [], "url": None})

    # ── Summary ──
    SUMMARY_RE = re.compile(
        r"(?:summary|objective|profile|about me)\s*[:\-]?\s*\n((?:.+\n?){1,6})", re.IGNORECASE
    )
    sm = SUMMARY_RE.search(text)
    summary = sm.group(1).strip() if sm else None

    return {
        "personal_info": {
            "full_name": lines[0] if lines else None,
            "email":     emails[0] if emails else None,
            "phone":     phones[0].strip() if phones else None,
            "location":  None,
            "linkedin":  linkedin[0] if linkedin else None,
            "github":    github[0] if github else None,
            "website":   websites[0] if websites else None,
            "date_of_birth": None,
        },
        "summary": summary,
        "skills": {
            "technical": technical_skills,
            "soft":      soft_skills,
            "languages": spoken_languages,
            "tools":     tools,
        },
        "experience":       experience,
        "education":        education,
        "certifications":   certifications,
        "projects":         projects,
        "awards":           [],
        "languages_spoken": [{"language": l, "proficiency": None} for l in spoken_languages],
        "interests":        [],
    }
