# tests/infrastructure/test_json_saver.py
import pytest
import json
import tempfile
import os
from unittest.mock import Mock
from review_analyzer.infrastructure.json_saver import JsonlSaver, JsonSaver


class TestJsonlSaver:
    """Test suite for JsonlSaver"""

    def test_saver_initialization(self):
        """Test saver initialization"""
        mock_logger = Mock()
        saver = JsonlSaver("test.jsonl", mock_logger)
        assert saver.output_path == "test.jsonl"
        assert saver.logger == mock_logger

    def test_save_data(self):
        """Test saving data to JSONL file"""
        mock_logger = Mock()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonl', delete=False) as f:
            output_path = f.name

        try:
            saver = JsonlSaver(output_path, mock_logger)
            test_data = [
                {"id": 1, "text": "test1"},
                {"id": 2, "text": "test2"}
            ]

            saver.save(test_data)
            
            assert os.path.exists(output_path)
            with open(output_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                assert len(lines) == 2
                assert json.loads(lines[0]) == {"id": 1, "text": "test1"}
                assert json.loads(lines[1]) == {"id": 2, "text": "test2"}
            
            mock_logger.info.assert_called_with('Wyniki zapisano do pliku: %s', output_path)
        finally:
            os.unlink(output_path)


class TestJsonSaver:
    """Test suite for JsonSaver"""

    def test_saver_initialization(self):
        """Test saver initialization"""
        saver = JsonSaver("test.json")
        assert saver.filepath == "test.json"
        assert saver.logger is None

    def test_save_data_with_logger(self):
        """Test saving data with logger"""
        mock_logger = Mock()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name

        try:
            saver = JsonSaver(filepath, mock_logger)
            test_data = {"key": "value", "number": 123}

            saver.save(test_data)
            
            assert os.path.exists(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                assert loaded_data == test_data
            
            mock_logger.info.assert_called_with("Wyniki zapisano do pliku: %s", filepath)
        finally:
            os.unlink(filepath)

    def test_save_data_without_logger(self):
        """Test saving data without logger"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filepath = f.name

        try:
            saver = JsonSaver(filepath)
            test_data = {"key": "value"}

            saver.save(test_data)
            
            assert os.path.exists(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                assert loaded_data == test_data
        finally:
            os.unlink(filepath)
