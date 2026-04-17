"""
extractor/gemini_parser.py
───────────────────────────
Uses Google Gemini AI to extract structured resume data from raw text.
Returns a clean Python dict matching the standard resume schema.
"""

import re
import json

PROMPT = """
You are an expert resume parser. Extract ALL information from the resume below
and return ONLY a single valid JSON object — no markdown, no explanation.

Use EXACTLY this schema (null for missing fields):

{
  "personal_info": {
    "full_name": "string",
    "email": "string",
    "phone": "string",
    "location": "string",
    "linkedin": "string",
    "github": "string",
    "website": "string",
    "date_of_birth": "string or null"
  },
  "summary": "string or null",
  "skills": {
    "technical": ["list"],
    "soft": ["list"],
    "languages": ["spoken/programming languages"],
    "tools": ["frameworks, platforms, software"]
  },
  "experience": [
    {
      "job_title": "string",
      "company": "string",
      "location": "string or null",
      "start_date": "YYYY-MM or YYYY",
      "end_date": "YYYY-MM or YYYY or Present",
      "responsibilities": ["bullet points"],
      "achievements": ["notable achievements"]
    }
  ],
  "education": [
    {
      "degree": "string",
      "field_of_study": "string",
      "institution": "string",
      "location": "string or null",
      "start_date": "YYYY or null",
      "end_date": "YYYY or null",
      "gpa": "string or null",
      "honors": "string or null"
    }
  ],
  "certifications": [
    {
      "name": "string",
      "issuer": "string or null",
      "date": "string or null"
    }
  ],
  "projects": [
    {
      "name": "string",
      "description": "string",
      "technologies": ["list"],
      "url": "string or null"
    }
  ],
  "awards": ["list"],
  "languages_spoken": [
    {"language": "string", "proficiency": "string or null"}
  ],
  "interests": ["list"]
}

Resume:
\"\"\"
{resume_text}
\"\"\"
"""


def extract_with_gemini(text: str, api_key: str) -> dict:
    """
    Send resume text to Gemini and parse the JSON response.
    Strips any accidental markdown code fences before parsing.
    """
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(PROMPT.format(resume_text=text[:12000]))

    raw = response.text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE)
    return json.loads(raw.strip())
