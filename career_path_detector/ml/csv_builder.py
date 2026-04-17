"""
ml/csv_builder.py
──────────────────
Converts cleaned resume dicts into a flat CSV row format suitable for
pandas, scikit-learn, and other ML frameworks.

Each resume becomes one row with numeric features, pipe-separated skill
strings (for TF-IDF / embeddings), and metadata columns.
"""

import csv
import pandas as pd

from utils.terminal import clr


# ── Row Builder ───────────────────────────────────────────────────────────────

def build_flat_row(data: dict) -> dict:
    """
    Flatten a single cleaned resume dict into one CSV-ready row dict.
    Experience entries are expanded into up to 5 individual columns each.
    """
    pi   = data.get("personal_info", {}) or {}
    feat = data.get("ml_features", {}) or {}

    row = {
        # Identity
        "source_file": feat.get("source_file", ""),
        "full_name":   pi.get("full_name", ""),
        "email":       pi.get("email", ""),
        "phone":       pi.get("phone", ""),
        "location":    pi.get("location", ""),
        "linkedin":    pi.get("linkedin", ""),
        "github":      pi.get("github", ""),
        "website":     pi.get("website", ""),

        # Summary
        "summary": (data.get("summary") or "").strip(),

        # Numeric ML features
        "total_experience_years": feat.get("total_experience_years", 0),
        "experience_level":       feat.get("experience_level", ""),
        "num_jobs":               feat.get("num_jobs", 0),
        "num_skills":             feat.get("num_skills", 0),
        "num_technical_skills":   feat.get("num_technical_skills", 0),
        "num_soft_skills":        feat.get("num_soft_skills", 0),
        "num_tools":              feat.get("num_tools", 0),
        "num_certifications":     feat.get("num_certifications", 0),
        "num_projects":           feat.get("num_projects", 0),
        "has_summary":            feat.get("has_summary", 0),
        "has_linkedin":           feat.get("has_linkedin", 0),
        "has_github":             feat.get("has_github", 0),
        "education_level":        feat.get("education_level", "unknown"),
        "latest_degree_year":     feat.get("latest_degree_year", ""),

        # Pipe-separated skill strings (for TF-IDF / embeddings)
        "all_skills":       feat.get("all_skills_joined", ""),
        "technical_skills": feat.get("technical_skills_joined", ""),
        "soft_skills":      feat.get("soft_skills_joined", ""),
        "tools":            feat.get("tools_joined", ""),

        # Education
        "education_institutions": "|".join(
            e.get("institution", "") for e in (data.get("education") or [])
        ),

        # Certifications
        "certifications": "|".join(
            c.get("name", "") for c in (data.get("certifications") or [])
        ),

        # Projects
        "projects": "|".join(
            p.get("name", "") for p in (data.get("projects") or [])
        ),

        # Interests & spoken languages
        "interests":       "|".join(data.get("interests") or []),
        "languages_spoken": "|".join(
            l.get("language", "") for l in (data.get("languages_spoken") or [])
        ),
    }

    # Expand up to 5 experience entries
    for i, exp in enumerate((data.get("experience") or [])[:5], 1):
        row[f"exp{i}_title"]   = exp.get("job_title", "")
        row[f"exp{i}_company"] = exp.get("company", "")
        row[f"exp{i}_start"]   = exp.get("start_date", "")
        row[f"exp{i}_end"]     = exp.get("end_date", "")

    return row


# ── CSV Saver ─────────────────────────────────────────────────────────────────

# Columns that appear first in the CSV (ML-friendly ordering)
PRIORITY_COLS = [
    "source_file", "full_name", "total_experience_years", "experience_level",
    "education_level", "num_jobs", "num_skills", "num_technical_skills",
    "num_soft_skills", "num_tools", "num_certifications", "num_projects",
    "has_summary", "has_linkedin", "has_github", "latest_degree_year",
    "all_skills", "technical_skills", "soft_skills", "tools",
]


def save_csv(rows: list[dict], out_path: str) -> pd.DataFrame | None:
    """
    Write a list of flat row dicts to a UTF-8 CSV file.
    Returns the resulting DataFrame (or None if rows is empty).
    """
    if not rows:
        print("  ⚠  No data to save.")
        return None

    df = pd.DataFrame(rows)
    df = df.fillna("")

    # Normalize whitespace in string cells
    map_fn = df.map if hasattr(df, "map") else df.applymap
    df = map_fn(lambda x: str(x).strip() if isinstance(x, str) else x)

    # Reorder columns: priority block first, then the rest
    other_cols = [c for c in df.columns if c not in PRIORITY_COLS]
    df = df[[c for c in PRIORITY_COLS if c in df.columns] + other_cols]

    df.to_csv(out_path, index=False, quoting=csv.QUOTE_ALL, encoding="utf-8")
    print(clr(f"\n  ✅  CSV saved → {out_path}  ({len(df)} row(s), {len(df.columns)} columns)", "32"))
    return df
