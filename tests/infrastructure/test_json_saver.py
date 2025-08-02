# tests/infrastructure/test_json_saver.py
from unittest.mock import Mock
import tempfile
import os
import json

from review_analyzer.infrastructure.json_saver import JsonlSaver

def test_save_jsonl_basic():
    data = [
        {"appid": 123, "liked": ["gameplay"], "disliked": [], "original_review": "Great!"},
        {"appid": 456, "liked": [], "disliked": ["bugs"], "original_review": "Crashes"}
    ]
    mock_logger = Mock()
    with tempfile.NamedTemporaryFile(mode='r+', delete=False) as tmp:
        path = tmp.name

    try:
        saver = JsonlSaver(path, mock_logger)
        saver.save(data)

        with open(path, encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) == 2
            for i, line in enumerate(lines):
                parsed = json.loads(line)
                assert parsed == data[i]

    finally:
        os.remove(path)
