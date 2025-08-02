# infrastructure/sentence_analyzer.py

import pandas as pd
import json
from collections import Counter
import re
from typing import Dict
from review_analyzer.domain.interfaces import ReviewAnalyzer


class ValidReviewAspectAnalyzer(ReviewAnalyzer):
    def __init__(self, output_path: str = None, label: str = "liked"):
        self.output_path = output_path
        self.label = label  # "liked" albo "disliked" — dla raportu

    def analyze_data(self, data: pd.DataFrame) -> Dict:
        required_cols = {"recommendationid", "aspect", "appid"}
        if not required_cols.issubset(data.columns):
            raise ValueError(f"Missing required columns: {required_cols - set(data.columns)}")

        summary = {}

        # --- 1. Statystyki ogólne
        summary["label"] = self.label
        summary["total_reviews"] = int(data["recommendationid"].nunique())
        aspects_per_review = data.groupby("recommendationid").size()
        summary["avg_aspects_per_review"] = float(round(aspects_per_review.mean(), 2))
        summary["aspects_per_review_variance"] = float(round(aspects_per_review.var(), 2))

        # --- 2. Top aspekty
        summary["top_aspects"] = Counter(data["aspect"]).most_common(10)

        # --- 3. Unikalność aspektów
        total_aspects = len(data)
        unique_aspects = data["aspect"].nunique()
        summary["unique_aspects"] = int(unique_aspects)
        summary["duplicated_aspects_ratio"] = round(1 - (unique_aspects / total_aspects), 3)

        # --- 4. Rozkład liczby aspektów na recenzję
        summary["aspect_count_distribution"] = (
            aspects_per_review.value_counts().sort_index().to_dict()
        )

        # --- 5. Długość aspektów (w słowach)
        word_counts = data["aspect"].str.split().str.len()
        summary["aspect_length_stats"] = {
            "mean": float(round(word_counts.mean(), 2)),
            "min": int(word_counts.min()),
            "max": int(word_counts.max()),
        }

        # --- 6. Top słowa
        tokens = data["aspect"].str.lower().apply(lambda s: re.findall(r"\b\w{3,}\b", s))
        flat_tokens = [token for sublist in tokens for token in sublist]
        summary["top_words"] = Counter(flat_tokens).most_common(15)

        # --- 7. Top aspekty per gra
        summary["top_aspects_per_game"] = (
            data.groupby("appid")["aspect"]
            .apply(lambda x: Counter(x).most_common(5))
            .to_dict()
        )

        if self.output_path is not None:
            with open(self.output_path, "w", encoding="utf-8") as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            print(f"✅ Zapisano analizę aspektów '{self.label}' do {self.output_path}")

        return summary


class ErrorReviewAnalyzer(ReviewAnalyzer):
    def analyze_data(self, data: pd.DataFrame) -> Dict:
        if "error" not in data.columns:
            raise ValueError("Missing 'error' column in input data")

        errors_only = data[data["error"].notna()]
        summary = {
            "total_errors": int(len(errors_only)),
            "error_types": dict(Counter(errors_only["error"])),
            "sample_errors": list(errors_only["error"].dropna().unique()[:5])
        }
        return summary


class FullReviewAnalyzer:
    def __init__(
        self,
        liked_analyzer: ReviewAnalyzer,
        disliked_analyzer: ReviewAnalyzer,
        error_analyzer: ReviewAnalyzer,
        output_path: str = r"review_analyzer/output/full_aspect_summary.json",
    ):
        self.liked_analyzer = liked_analyzer
        self.disliked_analyzer = disliked_analyzer
        self.error_analyzer = error_analyzer
        self.output_path = output_path

    def run(
        self,
        liked_df: pd.DataFrame,
        disliked_df: pd.DataFrame,
        error_df: pd.DataFrame
    ) -> None:
        liked_result = self.liked_analyzer.analyze_data(liked_df)
        disliked_result = self.disliked_analyzer.analyze_data(disliked_df)
        error_result = self.error_analyzer.analyze_data(error_df)

        result = {
            "liked_analysis": liked_result,
            "disliked_analysis": disliked_result,
            "error_analysis": error_result
        }

        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"✅ Zapisano pełną analizę do {self.output_path}")
