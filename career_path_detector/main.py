"""
main.py
────────
CLI entry point for the Career Path Detector.

Usage — single file:
    python main.py resume.pdf
    python main.py resume.pdf --api-key YOUR_KEY

Usage — batch folder:
    python main.py --batch ./resumes/
    python main.py --batch ./resumes/ --output results.csv

Environment variable (alternative to --api-key):
    export GEMINI_API_KEY=your_key
    python main.py resume.pdf
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# ── Local packages ────────────────────────────────────────────────────────────
from extractor import extract_resume
from utils.cleaner import clean_and_standardize
from utils.terminal import clr, banner, print_features
from ml.career_detector import predict_career_paths, print_predictions
from ml.csv_builder import build_flat_row, save_csv


# ── Process a single resume file ─────────────────────────────────────────────

def process_file(file_path: str, api_key: str | None) -> dict | None:
    print(clr(f"\n  📖  Reading: {Path(file_path).name}", "36"))
    try:
        raw = extract_resume(file_path, api_key=api_key)
    except Exception as e:
        print(clr(f"  ❌  Extraction error: {e}", "31"))
        return None

    data = clean_and_standardize(raw, source_file=file_path)
    print_features(data)

    # Career path prediction
    predictions = predict_career_paths(data)
    name = (data.get("personal_info") or {}).get("full_name") or Path(file_path).stem
    print_predictions(predictions, name=name)

    # Attach predictions to data for CSV export
    data["career_predictions"] = [p["track"] for p in predictions[:3]]
    data["top_career_track"]   = predictions[0]["track"] if predictions else "Unknown"

    return data


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Career Path Detector — Resume → AI-powered career prediction + ML CSV"
    )
    parser.add_argument("file", nargs="?", help="Single resume file (PDF/DOCX/TXT)")
    parser.add_argument("--batch",   metavar="DIR",  help="Folder of resumes to process in bulk")
    parser.add_argument("--api-key", default=None,   help="Google Gemini API key (or set GEMINI_API_KEY env)")
    parser.add_argument("--output",  default=None,   help="Output CSV path (default: auto-named)")
    args = parser.parse_args()

    banner()

    # ── Resolve API key ──
    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(clr("\n  ℹ  No Gemini API key set.", "33"))
        print(clr("  Get a FREE key → https://aistudio.google.com/apikey", "36"))
        api_key = input("  Paste API key (or press Enter to use offline regex mode): ").strip() or None

    # ── Collect files ──
    files = []
    if args.batch:
        folder = Path(args.batch)
        if not folder.is_dir():
            print(clr(f"  ❌  Not a directory: {folder}", "31"))
            sys.exit(1)
        for ext in ("*.pdf", "*.docx", "*.doc", "*.txt"):
            files.extend(folder.glob(ext))
        print(clr(f"\n  📂  Found {len(files)} resume(s) in {folder}", "36"))
    else:
        fp = args.file or input("\n  Enter resume file path: ").strip().strip('"').strip("'")
        if not os.path.isfile(fp):
            print(clr(f"  ❌  File not found: {fp}", "31"))
            sys.exit(1)
        files = [Path(fp)]

    # ── Process each file ──
    rows = []
    for fp in files:
        data = process_file(str(fp), api_key)
        if data:
            row = build_flat_row(data)
            # Add career prediction columns
            row["top_career_track"]   = data.get("top_career_track", "")
            row["career_predictions"] = "|".join(data.get("career_predictions", []))
            rows.append(row)

    if not rows:
        print(clr("\n  ❌  No data extracted. Exiting.", "31"))
        sys.exit(1)

    # ── Save CSV ──
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = args.output or f"career_results_{ts}.csv"
    df = save_csv(rows, out_path)

    # ── Batch summary ──
    if df is not None and len(df) > 1:
        print(clr("\n  📊  Dataset Summary:", "36"))
        print(f"      Rows              : {len(df)}")
        print(f"      Columns           : {len(df.columns)}")
        if "experience_level" in df.columns:
            print(f"      Exp Levels        : {df['experience_level'].value_counts().to_dict()}")
        if "top_career_track" in df.columns:
            print(f"      Career Tracks     : {df['top_career_track'].value_counts().to_dict()}")

    print(clr(f"\n  🎉  Done! Open {out_path} in pandas / Excel to begin training.\n", "1;32"))


if __name__ == "__main__":
    main()
