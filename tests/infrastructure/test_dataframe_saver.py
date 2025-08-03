import pytest
import pandas as pd
import tempfile
import os
from unittest.mock import Mock
from review_analyzer.infrastructure.dataframe_saver import DataFrameSaverCsv


class TestDataFrameSaverCsv:
    """Test suite for DataFrameSaverCsv"""

    def test_saver_initialization(self):
        """Test saver initialization"""
        mock_logger = Mock()
        saver = DataFrameSaverCsv(mock_logger)
        assert saver.logger == mock_logger

    def test_save_successful_dataframe(self):
        """Test successful saving of dataframe"""
        mock_logger = Mock()
        saver = DataFrameSaverCsv(mock_logger)

        test_data = pd.DataFrame({
            'col1': ['value1', 'value2'],
            'col2': [1, 2]
        })

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_path = f.name

        try:
            saver.save(test_data, csv_path)
            
            assert os.path.exists(csv_path)
            loaded_df = pd.read_csv(csv_path, sep=';')
            assert len(loaded_df) == 2
            assert list(loaded_df.columns) == ['col1', 'col2']
            mock_logger.info.assert_called_with("Zapisano plik: %s", csv_path)
        finally:
            os.unlink(csv_path)

    def test_save_empty_dataframe(self):
        """Test saving empty dataframe"""
        mock_logger = Mock()
        saver = DataFrameSaverCsv(mock_logger)

        # Create empty dataframe with columns
        empty_df = pd.DataFrame(columns=['col1', 'col2'])

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_path = f.name

        try:
            saver.save(empty_df, csv_path)
            
            assert os.path.exists(csv_path)
            loaded_df = pd.read_csv(csv_path, sep=';')
            assert len(loaded_df) == 0
            assert list(loaded_df.columns) == ['col1', 'col2']
            mock_logger.info.assert_called_with("Zapisano plik: %s", csv_path)
        finally:
            os.unlink(csv_path)

    def test_save_to_nonexistent_directory(self):
        """Test saving to non-existent directory"""
        mock_logger = Mock()
        saver = DataFrameSaverCsv(mock_logger)

        test_data = pd.DataFrame({'col': ['test']})
        nonexistent_path = "/nonexistent/directory/test.csv"

        saver.save(test_data, nonexistent_path)
        
        mock_logger.warning.assert_called() 