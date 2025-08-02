import tempfile
import os
import json
import pandas as pd
import pytest

from review_analyzer.infrastructure.sentence_analyzer import (
    ValidReviewAspectAnalyzer,
    ErrorReviewAnalyzer,
    FullReviewAnalyzer,
)


@pytest.fixture
def liked_df():
    return pd.DataFrame([
        {"appid": 1, "recommendationid": "a", "aspect": "great graphics"},
        {"appid": 1, "recommendationid": "a", "aspect": "fun combat"},
        {"appid": 1, "recommendationid": "b", "aspect": "nice story"},
    ])


@pytest.fixture
def disliked_df():
    return pd.DataFrame([
        {"appid": 1, "recommendationid": "c", "aspect": "bad UI"},
        {"appid": 1, "recommendationid": "d", "aspect": "bugs"},
        {"appid": 1, "recommendationid": "d", "aspect": "low framerate"},
    ])


@pytest.fixture
def error_df():
    return pd.DataFrame([
        {"recommendationid": "e", "original_review": "xyz", "error": "JSONDecodeError"},
        {"recommendationid": "f", "original_review": "abc", "error": "Empty review"},
    ])


def test_valid_review_analyzer_basic(liked_df):
    analyzer = ValidReviewAspectAnalyzer(label="liked")
    result = analyzer.analyze_data(liked_df)

    assert result["label"] == "liked"
    assert result["total_reviews"] == 2
    assert "avg_aspects_per_review" in result
    assert len(result["top_aspects"]) > 0
    assert "aspect_length_stats" in result
    assert "top_words" in result
    assert result["top_aspects_per_game"][1]  # appid = 1


def test_disliked_analyzer_output(disliked_df):
    analyzer = ValidReviewAspectAnalyzer(label="disliked")
    result = analyzer.analyze_data(disliked_df)

    assert result["label"] == "disliked"
    assert result["total_reviews"] == 2
    assert result["unique_aspects"] == 3
    assert isinstance(result["top_words"], list)


def test_valid_review_analyzer_file_output(liked_df):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json") as tmp:
        path = tmp.name

    analyzer = ValidReviewAspectAnalyzer(output_path=path, label="liked")
    result = analyzer.analyze_data(liked_df)

    with open(path, "r", encoding="utf-8") as f:
        file_result = json.load(f)

    assert file_result["label"] == "liked"
    assert file_result["total_reviews"] == 2
    os.remove(path)


def test_error_review_analyzer(error_df):
    analyzer = ErrorReviewAnalyzer()
    result = analyzer.analyze_data(error_df)

    assert result["total_errors"] == 2
    assert "JSONDecodeError" in result["error_types"]
    assert "Empty review" in result["sample_errors"]


def test_full_review_analyzer_run(liked_df, disliked_df, error_df):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json") as tmp:
        output_path = tmp.name

    analyzer = FullReviewAnalyzer(
        liked_analyzer=ValidReviewAspectAnalyzer(label="liked"),
        disliked_analyzer=ValidReviewAspectAnalyzer(label="disliked"),
        error_analyzer=ErrorReviewAnalyzer(),
        output_path=output_path
    )

    analyzer.run(liked_df, disliked_df, error_df)

    with open(output_path, "r", encoding="utf-8") as f:
        result = json.load(f)

    assert "liked_analysis" in result
    assert "disliked_analysis" in result
    assert "error_analysis" in result
    os.remove(output_path)
