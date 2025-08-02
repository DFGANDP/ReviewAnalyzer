from unittest.mock import Mock
import os
import json
import tempfile

from review_analyzer.infrastructure.json_loader import JsonReviewLoader


def test_load_reviews_basic():
    mock_data = {
        "reviews": [
            {"language": "english", "review": "Great game!", "votes_funny": 5, "voted_up": True, 'recommendationid': 3541},
            {"language": "polish", "review": "Super gra", "votes_funny": 1, "voted_up": False, 'recommendationid': 3542},
        ]
    }
    mock_logger = Mock()

    appid = 12345
    filename = f"{appid}_123456.json"

    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(mock_data, f)

        loader = JsonReviewLoader(filepath, mock_logger)
        reviews = loader.load_reviews()

        assert len(reviews) == 2
        assert reviews[0].appid == appid
        assert reviews[1].language == "polish"
        assert reviews[0].votes_funny == 5
        assert reviews[1].voted_up is False
        assert reviews[1].recommendationid == 3542


def test_filter_by_language():
    mock_data = {
        "reviews": [
            {"language": "english", "review": "ok", "votes_funny": 0, "voted_up": True},
            {"language": "polish", "review": "niezla", "votes_funny": 2, "voted_up": True},
        ]
    }

    appid = 99999
    filename = f"{appid}_999999.json"
    mock_logger = Mock()

    with tempfile.TemporaryDirectory() as temp_dir:
        filepath = os.path.join(temp_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(mock_data, f)

        loader = JsonReviewLoader(filepath, mock_logger)
        reviews = loader.load_reviews(language="english")

        assert len(reviews) == 1
        assert reviews[0].language == "english"
