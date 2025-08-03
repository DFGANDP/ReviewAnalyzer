import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
import pandas as pd
from review_analyzer.presentation.runner import (
    sentence_batch, 
    label_batch, 
    analysis_batch, 
    run
)


class TestRunner:
    """Test suite for runner.py module"""

    @patch('review_analyzer.presentation.runner.setup_logger')
    @patch('review_analyzer.presentation.runner.Client')
    @patch('review_analyzer.presentation.runner.SentenceLoader')
    @patch('review_analyzer.presentation.runner.analyze_and_save')
    def test_run_function_success(self, mock_analyze_and_save, mock_loader_class, mock_client_class, mock_setup_logger):
        """Test the main run function executes all batches successfully"""
        # Arrange
        mock_logger = Mock()
        mock_client = Mock()
        mock_loader = Mock()
        mock_setup_logger.return_value = mock_logger
        mock_client_class.return_value = mock_client
        mock_loader_class.return_value = mock_loader
        
        # Mock the load_dataframes method to return proper dataframes
        mock_reviews_df = pd.DataFrame({
            'appid': [123, 123],
            'recommendationid': [35131, 35132],
            'original_review': ['Great game', 'Amazing graphics'],
            'error': [None, None]
        })
        mock_liked_df = pd.DataFrame({'aspect': ['aspect1', 'aspect2']})
        mock_disliked_df = pd.DataFrame({'aspect': ['aspect3', 'aspect4']})
        mock_loader.load_dataframes.return_value = (mock_reviews_df, mock_liked_df, mock_disliked_df)
        
        PATHS = {
            'sentence_prompt': 'test_prompt.txt',
            'label_prompt': 'test_label.txt',
            'raw_reviews': '12345_20250209173825.json',  # Proper filename format
            'sentence_output': 'test_output.jsonl',
            'liked_csv': 'test_liked.csv',
            'disliked_csv': 'test_disliked.csv',
            'review_csv': 'test_reviews.csv',
            'liked_analysis': 'test_liked_analysis',
            'disliked_analysis': 'test_disliked_analysis',
            'charts': 'test_charts',
            'log': 'test.log'
        }
        MODEL_ID = "test-model"

        # Mock different file contents for different files
        def mock_file_side_effect(filename, *args, **kwargs):
            if 'prompt' in filename:
                return mock_open(read_data="test prompt")()
            elif filename.endswith('.json'):
                return mock_open(read_data='{"reviews": []}')()
            else:
                return mock_open(read_data="test content")()

        # Act
        with patch('builtins.open', side_effect=mock_file_side_effect):
            result = run(PATHS, MODEL_ID, workers=4, language='english')

        # Assert
        assert result == 0
        mock_setup_logger.assert_called_once()
        mock_client_class.assert_called_once()
        mock_logger.info.assert_called()

    @patch('review_analyzer.presentation.runner.setup_logger')
    @patch('review_analyzer.presentation.runner.Client')
    @patch('review_analyzer.presentation.runner.SentenceLoader')
    @patch('review_analyzer.presentation.runner.analyze_and_save')
    def test_run_function_with_custom_parameters(self, mock_analyze_and_save, mock_loader_class, mock_client_class, mock_setup_logger):
        """Test run function with custom workers and language parameters"""
        # Arrange
        mock_logger = Mock()
        mock_client = Mock()
        mock_loader = Mock()
        mock_setup_logger.return_value = mock_logger
        mock_client_class.return_value = mock_client
        mock_loader_class.return_value = mock_loader
        
        # Mock the load_dataframes method to return proper dataframes
        mock_reviews_df = pd.DataFrame({
            'appid': [123, 123],
            'recommendationid': [35131, 35132],
            'original_review': ['Great game', 'Amazing graphics'],
            'error': [None, None]
        })
        mock_liked_df = pd.DataFrame({'aspect': ['aspect1', 'aspect2']})
        mock_disliked_df = pd.DataFrame({'aspect': ['aspect3', 'aspect4']})
        mock_loader.load_dataframes.return_value = (mock_reviews_df, mock_liked_df, mock_disliked_df)
        
        PATHS = {
            'sentence_prompt': 'test_prompt.txt',
            'label_prompt': 'test_label.txt',
            'raw_reviews': '12345_20250209173825.json',  # Proper filename format
            'sentence_output': 'test_output.jsonl',
            'liked_csv': 'test_liked.csv',
            'disliked_csv': 'test_disliked.csv',
            'review_csv': 'test_reviews.csv',
            'liked_analysis': 'test_liked_analysis',
            'disliked_analysis': 'test_disliked_analysis',
            'charts': 'test_charts',
            'log': 'test.log'
        }
        MODEL_ID = "test-model"

        # Mock different file contents for different files
        def mock_file_side_effect(filename, *args, **kwargs):
            if 'prompt' in filename:
                return mock_open(read_data="test prompt")()
            elif filename.endswith('.json'):
                return mock_open(read_data='{"reviews": []}')()
            else:
                return mock_open(read_data="test content")()

        # Act
        with patch('builtins.open', side_effect=mock_file_side_effect):
            result = run(PATHS, MODEL_ID, workers=8, language='polish')

        # Assert
        assert result == 0

    @patch('review_analyzer.presentation.runner.ReviewProcessingService')
    @patch('review_analyzer.presentation.runner.JsonlSaver')
    @patch('review_analyzer.presentation.runner.MistralSentimentAspectExtractor')
    @patch('review_analyzer.presentation.runner.JsonReviewLoader')
    def test_sentence_batch(self, mock_loader_class, mock_extractor_class, 
                           mock_saver_class, mock_service_class):
        """Test sentence_batch function"""
        # Arrange
        mock_client = Mock()
        mock_logger = Mock()
        mock_loader = Mock()
        mock_extractor = Mock()
        mock_saver = Mock()
        mock_service = Mock()
        
        mock_loader_class.return_value = mock_loader
        mock_extractor_class.return_value = mock_extractor
        mock_saver_class.return_value = mock_saver
        mock_service_class.return_value = mock_service
        
        PATHS = {
            'sentence_prompt': 'test_prompt.txt',
            'raw_reviews': '12345_20250209173825.json',  # Proper filename format
            'sentence_output': 'test_output.jsonl'
        }
        MODEL_ID = "test-model"

        # Act
        with patch('builtins.open', mock_open(read_data="test prompt")):
            sentence_batch(mock_client, mock_logger, PATHS, MODEL_ID, workers=4, language='english')

        # Assert
        mock_loader_class.assert_called_once_with(PATHS['raw_reviews'], mock_logger)
        mock_extractor_class.assert_called_once_with(mock_client, MODEL_ID, "test prompt", mock_logger)
        mock_saver_class.assert_called_once_with(PATHS['sentence_output'], mock_logger)
        mock_service_class.assert_called_once_with(mock_extractor, mock_loader, mock_saver, mock_logger, 4, None)
        mock_service.run.assert_called_once_with('english')

    @patch('review_analyzer.presentation.runner.AspectLabelingService')
    @patch('review_analyzer.presentation.runner.DataFrameSaverCsv')
    @patch('review_analyzer.presentation.runner.MistralAspectLabeler')
    @patch('review_analyzer.presentation.runner.SentenceLoader')
    def test_label_batch(self, mock_loader_class, mock_labeler_class, 
                        mock_saver_class, mock_service_class):
        """Test label_batch function"""
        # Arrange
        mock_client = Mock()
        mock_logger = Mock()
        mock_loader = Mock()
        mock_labeler = Mock()
        mock_saver = Mock()
        mock_service = Mock()
        
        # Mock dataframes
        mock_reviews_df = pd.DataFrame({'review': ['test1', 'test2']})
        mock_liked_df = pd.DataFrame({'aspect': ['aspect1', 'aspect2']})
        mock_disliked_df = pd.DataFrame({'aspect': ['aspect3', 'aspect4']})
        
        mock_loader.load_dataframes.return_value = (mock_reviews_df, mock_liked_df, mock_disliked_df)
        mock_loader_class.return_value = mock_loader
        mock_labeler_class.return_value = mock_labeler
        mock_saver_class.return_value = mock_saver
        mock_service_class.return_value = mock_service
        
        PATHS = {
            'label_prompt': 'test_label.txt',
            'sentence_output': 'test_output.jsonl',
            'liked_csv': 'test_liked.csv',
            'disliked_csv': 'test_disliked.csv',
            'review_csv': 'test_reviews.csv'
        }
        MODEL_ID = "test-model"

        # Act
        with patch('builtins.open', mock_open(read_data="test label prompt")):
            label_batch(mock_client, mock_logger, PATHS, MODEL_ID, workers=4)

        # Assert
        mock_loader_class.assert_called_once_with(PATHS['sentence_output'], mock_logger)
        mock_loader.load_dataframes.assert_called_once()
        mock_labeler_class.assert_called_once_with(
            client=mock_client,
            model_name=MODEL_ID,
            prompt_template="test label prompt",
            logger=mock_logger
        )
        assert mock_service_class.call_count == 2  # Called for both liked and disliked
        assert mock_saver.save.call_count == 3  # Called for liked, disliked, and reviews

    @patch('review_analyzer.presentation.runner.analyze_and_save')
    def test_analysis_batch(self, mock_analyze_and_save):
        """Test analysis_batch function"""
        # Arrange
        mock_logger = Mock()
        PATHS = {
            'liked_csv': 'test_liked.csv',
            'disliked_csv': 'test_disliked.csv',
            'liked_analysis': 'test_liked_analysis',
            'disliked_analysis': 'test_disliked_analysis',
            'charts': 'test_charts'
        }

        # Act
        analysis_batch(mock_logger, PATHS)

        # Assert
        assert mock_analyze_and_save.call_count == 2
        
        # Check first call (liked)
        first_call = mock_analyze_and_save.call_args_list[0]
        assert first_call[1]['label'] == "liked"
        assert first_call[1]['csv_path'] == PATHS['liked_csv']
        assert first_call[1]['output_path'] == PATHS['liked_analysis']
        assert first_call[1]['logger'] == mock_logger
        assert first_call[1]['charts_dir'] == PATHS['charts']
        
        # Check second call (disliked)
        second_call = mock_analyze_and_save.call_args_list[1]
        assert second_call[1]['label'] == "disliked"
        assert second_call[1]['csv_path'] == PATHS['disliked_csv']
        assert second_call[1]['output_path'] == PATHS['disliked_analysis']
        assert second_call[1]['logger'] == mock_logger
        assert second_call[1]['charts_dir'] == PATHS['charts']

    @patch('review_analyzer.presentation.runner.setup_logger')
    @patch('review_analyzer.presentation.runner.Client')
    @patch('review_analyzer.presentation.runner.SentenceLoader')
    @patch('review_analyzer.presentation.runner.analyze_and_save')
    def test_run_function_logging(self, mock_analyze_and_save, mock_loader_class, mock_client_class, mock_setup_logger):
        """Test that run function logs start and end messages"""
        # Arrange
        mock_logger = Mock()
        mock_client = Mock()
        mock_loader = Mock()
        mock_setup_logger.return_value = mock_logger
        mock_client_class.return_value = mock_client
        mock_loader_class.return_value = mock_loader
        
        # Mock the load_dataframes method to return proper dataframes
        mock_reviews_df = pd.DataFrame({
            'appid': [123, 123],
            'recommendationid': [35131, 35132],
            'original_review': ['Great game', 'Amazing graphics'],
            'error': [None, None]
        })
        mock_liked_df = pd.DataFrame({'aspect': ['aspect1', 'aspect2']})
        mock_disliked_df = pd.DataFrame({'aspect': ['aspect3', 'aspect4']})
        mock_loader.load_dataframes.return_value = (mock_reviews_df, mock_liked_df, mock_disliked_df)
        
        PATHS = {
            'sentence_prompt': 'test_prompt.txt',
            'label_prompt': 'test_label.txt',
            'raw_reviews': '12345_20250209173825.json',  # Proper filename format
            'sentence_output': 'test_output.jsonl',
            'liked_csv': 'test_liked.csv',
            'disliked_csv': 'test_disliked.csv',
            'review_csv': 'test_reviews.csv',
            'liked_analysis': 'test_liked_analysis',
            'disliked_analysis': 'test_disliked_analysis',
            'charts': 'test_charts',
            'log': 'test.log'
        }
        MODEL_ID = "test-model"

        # Mock different file contents for different files
        def mock_file_side_effect(filename, *args, **kwargs):
            if 'prompt' in filename:
                return mock_open(read_data="test prompt")()
            elif filename.endswith('.json'):
                return mock_open(read_data='{"reviews": []}')()
            else:
                return mock_open(read_data="test content")()

        # Act
        with patch('builtins.open', side_effect=mock_file_side_effect):
            run(PATHS, MODEL_ID)

        # Assert
        mock_logger.info.assert_any_call("Start przetwarzania…")
        mock_logger.info.assert_any_call("Zakończono.")

    @patch('review_analyzer.presentation.runner.setup_logger')
    @patch('review_analyzer.presentation.runner.Client')
    @patch('review_analyzer.presentation.runner.SentenceLoader')
    @patch('review_analyzer.presentation.runner.analyze_and_save')
    def test_run_function_logger_setup(self, mock_analyze_and_save, mock_loader_class, mock_client_class, mock_setup_logger):
        """Test that logger is set up with correct parameters"""
        # Arrange
        mock_logger = Mock()
        mock_client = Mock()
        mock_loader = Mock()
        mock_setup_logger.return_value = mock_logger
        mock_client_class.return_value = mock_client
        mock_loader_class.return_value = mock_loader
        
        # Mock the load_dataframes method to return proper dataframes
        mock_reviews_df = pd.DataFrame({
            'appid': [123, 123],
            'recommendationid': [35131, 35132],
            'original_review': ['Great game', 'Amazing graphics'],
            'error': [None, None]
        })
        mock_liked_df = pd.DataFrame({'aspect': ['aspect1', 'aspect2']})
        mock_disliked_df = pd.DataFrame({'aspect': ['aspect3', 'aspect4']})
        mock_loader.load_dataframes.return_value = (mock_reviews_df, mock_liked_df, mock_disliked_df)
        
        PATHS = {
            'sentence_prompt': 'test_prompt.txt',
            'label_prompt': 'test_label.txt',
            'raw_reviews': '12345_20250209173825.json',  # Proper filename format
            'sentence_output': 'test_output.jsonl',
            'liked_csv': 'test_liked.csv',
            'disliked_csv': 'test_disliked.csv',
            'review_csv': 'test_reviews.csv',
            'liked_analysis': 'test_liked_analysis',
            'disliked_analysis': 'test_disliked_analysis',
            'charts': 'test_charts',
            'log': 'test.log'
        }
        MODEL_ID = "test-model"

        # Mock different file contents for different files
        def mock_file_side_effect(filename, *args, **kwargs):
            if 'prompt' in filename:
                return mock_open(read_data="test prompt")()
            elif filename.endswith('.json'):
                return mock_open(read_data='{"reviews": []}')()
            else:
                return mock_open(read_data="test content")()

        # Act
        with patch('builtins.open', side_effect=mock_file_side_effect):
            run(PATHS, MODEL_ID)

        # Assert - just check that setup_logger was called with correct name
        mock_setup_logger.assert_called_once()
        call_args = mock_setup_logger.call_args
        assert call_args[1]['name'] == "review-analyzer"
        assert 'handlers' in call_args[1] 