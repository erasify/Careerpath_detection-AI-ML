"""
utils/cleaner.py
─────────────────
Cleans and standardizes raw resume dicts produced by the extractor package.
Normalizes skill aliases, computes ML features, and enriches the data dict
so it's ready for the ML pipeline and CSV export.
"""

import re
from datetime import date
from pathlib import Path

from .constants import SKILL_MAP, EXPERIENCE_LEVEL_MAP


# ── Text / Skill Helpers ──────────────────────────────────────────────────────

def normalize_skill(s: str) -> str:
    """Map skill aliases to their canonical form (e.g. 'js' → 'javascript')."""
    s = s.strip().lower()
    return SKILL_MAP.get(s, s)


def clean_text(v) -> str | None:
    return v.strip().lower() if isinstance(v, str) and v.strip() else None


def clean_list(items) -> list[str]:
    """Normalize and deduplicate a list of skill strings."""
    if not isinstance(items, list):
        return []
    cleaned = [normalize_skill(i) for i in items if isinstance(i, str) and i.strip()]
    return sorted(set(cleaned))


# ── Date / Experience Helpers ─────────────────────────────────────────────────

def parse_year(date_str) -> int | None:
    if not date_str:
        return None
    m = re.search(r"\b(19|20)\d{2}\b", str(date_str))
    return int(m.group()) if m else None


def calc_experience_years(experience: list) -> float:
    """Sum total years of work experience across all job entries."""
    total_months = 0
    for exp in experience:
        start = parse_year(exp.get("start_date"))
        end_raw = exp.get("end_date", "")
        if isinstance(end_raw, str) and "present" in end_raw.lower():
            end = date.today().year
        else:
            end = parse_year(end_raw)
        if start and end and end >= start:
            total_months += (end - start) * 12
    return round(total_months / 12, 1)


def map_experience_level(years: float) -> str:
    for threshold, label in EXPERIENCE_LEVEL_MAP:
        if years <= threshold:
            return label
    return "executive"


# ── Education Helpers ─────────────────────────────────────────────────────────

def _highest_education(education: list) -> str:
    order = {
        "phd": 5, "doctorate": 5, "master": 4, "mba": 4,
        "bachelor": 3, "associate": 2, "diploma": 1, "certificate": 1,
    }
    best, best_label = 0, "unknown"
    for edu in education:
        deg = (edu.get("degree") or "").lower()
        for key, rank in order.items():
            if key in deg and rank > best:
                best, best_label = rank, key
    return best_label


def _latest_grad_year(education: list) -> int | None:
    years = [parse_year(e.get("end_date")) for e in education]
    years = [y for y in years if y]
    return max(years) if years else None


# ── Main Pipeline ─────────────────────────────────────────────────────────────

def clean_and_standardize(data: dict, source_file: str = "") -> dict:
    """
    Full cleaning + feature-engineering pass on a raw resume dict.

    Mutates and returns the dict enriched with:
      - normalized personal_info
      - deduplicated, canonical skills
      - all_skills list (union of technical + tools + languages)
      - ml_features dict (numeric + string features for ML/CSV)
    """
    pi         = data.get("personal_info", {}) or {}
    skills_raw = data.get("skills", {}) or {}
    experience = data.get("experience", []) or []
    education  = data.get("education", []) or []

    # ── Personal info ──
    data["personal_info"] = {
        "full_name":     pi.get("full_name"),
        "email":         clean_text(pi.get("email")),
        "phone":         pi.get("phone"),
        "location":      clean_text(pi.get("location")),
        "linkedin":      clean_text(pi.get("linkedin")),
        "github":        clean_text(pi.get("github")),
        "website":       clean_text(pi.get("website")),
        "date_of_birth": pi.get("date_of_birth"),
    }

    # ── Skills ──
    technical  = clean_list(skills_raw.get("technical"))
    tools      = clean_list(skills_raw.get("tools"))
    soft       = clean_list(skills_raw.get("soft"))
    langs      = clean_list(skills_raw.get("languages"))
    all_skills = sorted(set(technical + tools + langs))

    data["skills"]     = {"technical": technical, "soft": soft, "languages": langs, "tools": tools}
    data["all_skills"] = all_skills

    # ── ML feature block ──
    exp_years = calc_experience_years(experience)
    data["ml_features"] = {
        "source_file":             Path(source_file).name if source_file else "",
        "total_experience_years":  exp_years,
        "experience_level":        map_experience_level(exp_years),
        "num_jobs":                len(experience),
        "num_skills":              len(all_skills),
        "num_technical_skills":    len(technical),
        "num_soft_skills":         len(soft),
        "num_tools":               len(tools),
        "num_certifications":      len(data.get("certifications", []) or []),
        "num_projects":            len(data.get("projects", []) or []),
        "has_summary":             int(bool(data.get("summary"))),
        "has_linkedin":            int(bool(pi.get("linkedin"))),
        "has_github":              int(bool(pi.get("github"))),
        "education_level":         _highest_education(education),
        "latest_degree_year":      _latest_grad_year(education),
        "all_skills_joined":       "|".join(all_skills),
        "technical_skills_joined": "|".join(technical),
        "soft_skills_joined":      "|".join(soft),
        "tools_joined":            "|".join(tools),
    }

    return data
