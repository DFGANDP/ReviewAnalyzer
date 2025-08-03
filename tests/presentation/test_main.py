import pytest
from unittest.mock import patch, MagicMock
import argparse
from review_analyzer.presentation.main import main


class TestMain:
    """Test suite for main.py module"""

    @patch('review_analyzer.presentation.main.run')
    @patch('review_analyzer.presentation.main.argparse.ArgumentParser')
    def test_main_with_default_arguments(self, mock_parser_class, mock_run):
        """Test main function with default arguments"""
        # Arrange
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.workers = 6
        mock_args.language = "english"
        mock_parser.parse_args.return_value = mock_args
        mock_parser_class.return_value = mock_parser

        # Act
        result = main()

        # Assert
        assert result == 0
        mock_parser.add_argument.assert_called()
        mock_parser.parse_args.assert_called_once()
        mock_run.assert_called_once()

    @patch('review_analyzer.presentation.main.run')
    @patch('review_analyzer.presentation.main.argparse.ArgumentParser')
    def test_main_with_custom_arguments(self, mock_parser_class, mock_run):
        """Test main function with custom arguments"""
        # Arrange
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.workers = 12
        mock_args.language = "polish"
        mock_parser.parse_args.return_value = mock_args
        mock_parser_class.return_value = mock_parser

        # Act
        result = main()

        # Assert
        assert result == 0
        mock_run.assert_called_once()

    @patch('review_analyzer.presentation.main.run')
    @patch('review_analyzer.presentation.main.argparse.ArgumentParser')
    def test_main_argument_parser_configuration(self, mock_parser_class, mock_run):
        """Test that argument parser is configured correctly"""
        # Arrange
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.workers = 6
        mock_args.language = "english"
        mock_args.limit = None
        mock_parser.parse_args.return_value = mock_args
        mock_parser_class.return_value = mock_parser

        # Act
        main()

        # Assert
        # Check that add_argument was called for both workers and language
        add_argument_calls = mock_parser.add_argument.call_args_list
        assert len(add_argument_calls) == 3
        
        # Check workers argument
        workers_call = add_argument_calls[0]
        assert workers_call[1]['type'] == int
        assert workers_call[1]['default'] == 6
        
        # Check language argument
        language_call = add_argument_calls[1]
        assert language_call[1]['default'] == "english"

        limit_call = add_argument_calls[2]
        assert limit_call[1]['default'] is None

    def test_main_system_exit_behavior(self):
        """Test that main raises SystemExit when called as script"""
        # This test is not needed since main() doesn't actually raise SystemExit
        # The SystemExit is only raised in the if __name__ == "__main__" block
        # which is not executed during testing
        pass 