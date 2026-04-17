"""
utils/constants.py
───────────────────
Shared constants: skill normalization map and experience level thresholds.
Imported by both the ML pipeline and the cleaner.
"""

# ── Skill Alias → Canonical Name ─────────────────────────────────────────────
SKILL_MAP = {
    # Python
    "py": "python", "python3": "python",
    # JavaScript
    "js": "javascript", "javascript es6": "javascript", "es6": "javascript",
    "ts": "typescript",
    "node": "node.js", "nodejs": "node.js",
    "react.js": "react", "reactjs": "react",
    "vue.js": "vue", "vuejs": "vue",
    "next.js": "next.js", "nextjs": "next.js",
    # ML / AI
    "ml": "machine learning",
    "dl": "deep learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "sk-learn": "scikit-learn", "sklearn": "scikit-learn",
    "tf": "tensorflow", "tensorflow2": "tensorflow",
    "pytorch": "pytorch", "torch": "pytorch",
    # Databases
    "mongo": "mongodb", "mongo db": "mongodb",
    "postgres": "postgresql", "psql": "postgresql",
    "mysql": "mysql", "ms sql": "sql server",
    # Cloud
    "aws": "amazon web services",
    "gcp": "google cloud platform",
    "azure": "microsoft azure",
    # DevOps
    "k8s": "kubernetes",
    "ci/cd": "ci/cd", "cicd": "ci/cd",
    "gh actions": "github actions",
    # Languages / Misc
    "c++": "c++", "cpp": "c++",
    "c#": "c#", "csharp": "c#",
    "oop": "object-oriented programming",
    "ds": "data structures",
    "dsa": "data structures and algorithms",
}

# ── Experience Buckets (upper bound in years → label) ────────────────────────
EXPERIENCE_LEVEL_MAP = [
    (0,   "no experience"),
    (1,   "entry level"),   # 0–1 yr
    (3,   "junior"),        # 1–3 yr
    (6,   "mid level"),     # 3–6 yr
    (10,  "senior"),        # 6–10 yr
    (999, "executive"),     # 10+ yr
]
