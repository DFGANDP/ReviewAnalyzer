import pytest
import pandas as pd
from unittest.mock import Mock, patch
from review_analyzer.infrastructure.utils import analyze_and_save


class TestUtils:
    """Test suite for utils module"""

    @patch('review_analyzer.infrastructure.utils.JsonSaver')
    @patch('review_analyzer.infrastructure.utils.GlobalAspectAnalyzer')
    @patch('review_analyzer.infrastructure.utils.DataFrameLoaderCsv')
    def test_analyze_and_save_success(self, mock_loader_class, mock_analyzer_class, mock_saver_class):
        """Test successful analyze and save operation"""
        mock_logger = Mock()
        mock_loader = Mock()
        mock_analyzer = Mock()
        mock_saver = Mock()
        
        # Mock dataframe
        test_df = pd.DataFrame({
            'labels': ['label1', 'label2', 'label3'],
            'other_col': ['val1', 'val2', 'val3']
        })
        
        mock_loader.load.return_value = test_df
        mock_analyzer.analyze_data.return_value = {"analysis": "result"}
        
        mock_loader_class.return_value = mock_loader
        mock_analyzer_class.return_value = mock_analyzer
        mock_saver_class.return_value = mock_saver
        
        analyze_and_save(
            label="liked",
            csv_path="test.csv",
            output_path="test_output.json",
            logger=mock_logger,
            charts_dir="test_charts"
        )
        
        # Verify calls
        mock_loader_class.assert_called_once_with(mock_logger)
        mock_loader.load.assert_called_once_with("test.csv")
        mock_analyzer_class.assert_called_once_with(label="liked")
        mock_analyzer.analyze_data.assert_called_once()
        mock_analyzer.generate_charts.assert_called_once_with(output_dir="test_charts")
        mock_saver_class.assert_called_once_with("test_output.json", mock_logger)
        mock_saver.save.assert_called_once_with({"analysis": "result"})

    @patch('review_analyzer.infrastructure.utils.JsonSaver')
    @patch('review_analyzer.infrastructure.utils.GlobalAspectAnalyzer')
    @patch('review_analyzer.infrastructure.utils.DataFrameLoaderCsv')
    def test_analyze_and_save_with_empty_dataframe(self, mock_loader_class, mock_analyzer_class, mock_saver_class):
        """Test analyze and save with empty dataframe"""
        mock_logger = Mock()
        mock_loader = Mock()
        mock_analyzer = Mock()
        mock_saver = Mock()
        
        # Mock empty dataframe
        empty_df = pd.DataFrame({'labels': []})
        
        mock_loader.load.return_value = empty_df
        mock_analyzer.analyze_data.return_value = {"analysis": "empty"}
        
        mock_loader_class.return_value = mock_loader
        mock_analyzer_class.return_value = mock_analyzer
        mock_saver_class.return_value = mock_saver
        
        analyze_and_save(
            label="disliked",
            csv_path="empty.csv",
            output_path="empty_output.json",
            logger=mock_logger,
            charts_dir="empty_charts"
        )
        
        # Verify that labels column is processed correctly
        mock_analyzer.analyze_data.assert_called_once()
        called_df = mock_analyzer.analyze_data.call_args[0][0]
        assert 'labels' in called_df.columns
        assert called_df['labels'].dtype == 'object'  # Should be string type after processing 