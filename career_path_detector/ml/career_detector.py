"""
ml/career_detector.py
──────────────────────
Career path detection engine.

Maps a candidate's extracted skills + experience to one or more
predicted career tracks using a rule-based scoring approach.
This module is designed to be replaced or enhanced with a trained
ML model (e.g. scikit-learn classifier) once labelled data is available.

Predicted tracks
────────────────
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
"""

from __future__ import annotations

# ── Career Track Definitions ──────────────────────────────────────────────────
# Each track is defined by a set of indicator skills.
# The score for a track = number of its skills present in the candidate's profile.

CAREER_TRACKS: dict[str, set[str]] = {
    "Full-Stack Developer": {
        "javascript", "typescript", "react", "vue", "angular", "next.js",
        "node.js", "express", "django", "flask", "fastapi", "laravel",
        "html", "css", "rest", "graphql", "mongodb", "postgresql", "mysql",
        "docker", "git",
    },
    "Frontend Developer": {
        "javascript", "typescript", "react", "vue", "angular", "next.js",
        "html", "css", "tailwind", "bootstrap", "sass", "webpack", "vite",
        "redux", "figma", "responsive design", "accessibility",
    },
    "Backend Developer": {
        "python", "java", "node.js", "go", "rust", "c#", "ruby",
        "django", "flask", "fastapi", "spring", "express", "laravel",
        "postgresql", "mysql", "mongodb", "redis", "rest", "graphql",
        "docker", "kubernetes", "microservices", "api",
    },
    "Data Scientist / ML Engineer": {
        "python", "machine learning", "deep learning", "tensorflow", "pytorch",
        "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn",
        "natural language processing", "computer vision", "data science",
        "jupyter", "sql", "spark", "data analysis", "statistics",
        "hugging face", "langchain", "llm", "openai",
    },
    "DevOps / Cloud Engineer": {
        "docker", "kubernetes", "terraform", "ansible", "jenkins",
        "github actions", "ci/cd", "aws", "azure", "google cloud platform",
        "linux", "bash", "nginx", "monitoring", "grafana", "prometheus",
        "git", "infrastructure as code",
    },
    "Mobile Developer": {
        "android", "ios", "swift", "kotlin", "react native", "flutter",
        "dart", "java", "xcode", "android studio", "mobile", "app development",
    },
    "Cybersecurity Engineer": {
        "cybersecurity", "penetration testing", "ethical hacking", "owasp",
        "firewalls", "ssl", "tls", "encryption", "networking", "tcp/ip",
        "linux", "bash", "python", "vulnerability assessment", "siem",
    },
    "QA / Test Engineer": {
        "selenium", "cypress", "pytest", "jest", "junit", "mocha",
        "unit testing", "tdd", "bdd", "postman", "test automation",
        "manual testing", "performance testing", "api testing",
    },
    "Embedded / Systems Engineer": {
        "c", "c++", "assembly", "rtos", "embedded systems", "microcontrollers",
        "arduino", "raspberry pi", "fpga", "verilog", "vhdl",
        "linux", "networking", "hardware",
    },
    "Business Analyst / Product Manager": {
        "project management", "agile", "scrum", "kanban", "jira",
        "confluence", "sql", "excel", "tableau", "power bi",
        "stakeholder management", "requirements gathering", "data analysis",
        "communication", "presentation",
    },
}

# Minimum score (matched skills) to include a track in results
MIN_SCORE = 2


# ── Scorer ────────────────────────────────────────────────────────────────────

def score_tracks(all_skills: list[str]) -> dict[str, int]:
    """
    Score every career track against the candidate's skill list.
    Returns {track_name: score} sorted descending.
    """
    skill_set = set(s.lower() for s in all_skills)
    scores = {}
    for track, indicators in CAREER_TRACKS.items():
        score = len(skill_set & indicators)
        if score >= MIN_SCORE:
            scores[track] = score
    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))


def predict_career_paths(data: dict) -> list[dict]:
    """
    Given a cleaned resume dict, return a ranked list of career path predictions.

    Each prediction is:
        {
            "track":   "Full-Stack Developer",
            "score":   12,
            "matched": ["react", "node.js", ...]
        }
    """
    all_skills = data.get("all_skills", [])
    skill_set  = set(s.lower() for s in all_skills)
    scores     = score_tracks(all_skills)

    results = []
    for track, score in scores.items():
        matched = sorted(skill_set & CAREER_TRACKS[track])
        results.append({"track": track, "score": score, "matched": matched})

    return results


# ── Display ───────────────────────────────────────────────────────────────────

def print_predictions(predictions: list[dict], name: str = "Candidate"):
    """Pretty-print career path predictions to the terminal."""
    print(f"\n  🎯  Career Path Predictions for: {name}")
    print("  " + "─" * 50)
    if not predictions:
        print("  ⚠  Not enough skills matched any career track.")
        return
    for rank, pred in enumerate(predictions, 1):
        bar = "█" * pred["score"] + "░" * max(0, 15 - pred["score"])
        print(f"  #{rank}  {pred['track']:<35} [{bar}] {pred['score']} pts")
        print(f"       Skills: {', '.join(pred['matched'][:8])}")
    print("  " + "─" * 50)
