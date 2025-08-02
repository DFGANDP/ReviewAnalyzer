from unittest.mock import Mock
import pytest
import pandas as pd
from pathlib import Path
from review_analyzer.infrastructure.sentence_loader import SentenceLoader

def test_load_dataframes_splits_correctly(tmp_path: Path):
    # --- Przygotuj dane wejściowe
    sample_data = [
        '{"appid": 123, "recommendationid": "1", "liked": ["fun gameplay", "music"], "disliked": ["bugs"], "original_review": "Great game"}',
        '{"appid": 456, "recommendationid": "2", "liked": [], "disliked": [], "original_review": "Meh"}',
        '{"appid": 789, "recommendationid": "3", "original_review": "This is broken", "bad_json"}'
    ]
    mock_logger = Mock()
    jsonl_path = tmp_path / "test.jsonl"
    jsonl_path.write_text("\n".join(sample_data), encoding="utf-8")

    # --- Wczytaj dane
    loader = SentenceLoader(str(jsonl_path), mock_logger)
    reviews_df, liked_df, disliked_df = loader.load_dataframes()

    # --- Sprawdź reviews_df
    assert len(reviews_df) == 3
    assert "error" in reviews_df.columns
    assert reviews_df["error"].notna().sum() == 1  # jeden błąd JSON

    # --- Sprawdź liked_df
    liked_aspects = liked_df["aspect"].tolist()
    assert sorted(liked_aspects) == ["fun gameplay", "music"]

    # --- Sprawdź disliked_df
    disliked_aspects = disliked_df["aspect"].tolist()
    assert disliked_aspects == ["bugs"]
