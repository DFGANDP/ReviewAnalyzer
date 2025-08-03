import pytest
import pandas as pd
import tempfile
import os
from unittest.mock import Mock
from review_analyzer.infrastructure.dataframe_loader import DataFrameLoaderCsv


class TestDataFrameLoaderCsv:
    """Test suite for DataFrameLoaderCsv"""

    def test_loader_initialization(self):
        """Test loader initialization"""
        mock_logger = Mock()
        loader = DataFrameLoaderCsv(mock_logger)
        assert loader.logger == mock_logger

    def test_load_successful_csv(self):
        """Test successful loading of CSV file"""
        mock_logger = Mock()
        loader = DataFrameLoaderCsv(mock_logger)

        # Create test data
        test_data = pd.DataFrame({
            'col1': ['value1', 'value2'],
            'col2': [1, 2]
        })

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            test_data.to_csv(f.name, index=False, sep=';')
            csv_path = f.name

        try:
            result = loader.load(csv_path)
            
            assert result is not None
            assert len(result) == 2
            assert list(result.columns) == ['col1', 'col2']
            mock_logger.info.assert_called_with("Wczytano plik: %s posiada %d lini", csv_path, 2)
        finally:
            os.unlink(csv_path)

    def test_load_nonexistent_file(self):
        """Test loading non-existent file"""
        mock_logger = Mock()
        loader = DataFrameLoaderCsv(mock_logger)
        
        result = loader.load("/nonexistent/file.csv")
        
        assert result is None
        mock_logger.warning.assert_called()

    def test_load_empty_csv(self):
        """Test loading empty CSV file"""
        mock_logger = Mock()
        loader = DataFrameLoaderCsv(mock_logger)

        # Create CSV with headers but no data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("col1;col2\n")  # Write headers only
            csv_path = f.name

        try:
            result = loader.load(csv_path)
            
            assert result is not None
            assert len(result) == 0
            assert list(result.columns) == ['col1', 'col2']
            mock_logger.info.assert_called_with("Wczytano plik: %s posiada %d lini", csv_path, 0)
        finally:
            os.unlink(csv_path) 