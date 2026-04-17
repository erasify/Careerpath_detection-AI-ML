"""
utils/terminal.py
──────────────────
Lightweight terminal output helpers: ANSI colors, banner, feature summary.
No external dependencies.
"""


def clr(text: str, code: str) -> str:
    """Wrap text in an ANSI color escape code."""
    return f"\033[{code}m{text}\033[0m"


def banner():
    print(clr("\n" + "═" * 62, "1;32"))
    print(clr("   📄  CAREER PATH DETECTOR  —  ML-Ready CSV Pipeline", "1;37"))
    print(clr("   FREE Gemini API  |  PDF · DOCX · TXT  |  Clean CSV Output", "90"))
    print(clr("═" * 62, "1;32"))


def print_features(data: dict):
    """Pretty-print the extracted ML features to the terminal."""
    feat = data.get("ml_features", {})
    pi   = data.get("personal_info", {})
    print(clr("\n  ── Extracted ML Features ──────────────────────────", "90"))
    print(f"  Name             : {pi.get('full_name', 'N/A')}")
    print(f"  Email            : {pi.get('email', 'N/A')}")
    print(f"  Location         : {pi.get('location', 'N/A')}")
    print(f"  Experience       : {feat.get('total_experience_years')} yr(s)  [{feat.get('experience_level')}]")
    print(f"  Education Level  : {feat.get('education_level')}")
    print(f"  # Jobs           : {feat.get('num_jobs')}")
    print(f"  # Skills         : {feat.get('num_skills')}")
    print(f"  # Certifications : {feat.get('num_certifications')}")
    print(f"  # Projects       : {feat.get('num_projects')}")
    print(f"  Has LinkedIn     : {bool(feat.get('has_linkedin'))}")
    print(f"  Has GitHub       : {bool(feat.get('has_github'))}")
    print(f"  All Skills       : {feat.get('all_skills_joined', '')[:80]}")
    print(clr("  ────────────────────────────────────────────────────", "90"))
