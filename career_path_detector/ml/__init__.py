"""
ml/
────
Machine learning pipeline: career path prediction and CSV export.
"""

from .career_detector import predict_career_paths, print_predictions
from .csv_builder import build_flat_row, save_csv
