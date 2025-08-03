import pytest
import json
from unittest.mock import Mock, patch
from review_analyzer.infrastructure.aspect_labeler import MistralAspectLabeler


class TestMistralAspectLabeler:
    """Test suite for MistralAspectLabeler"""

    def test_initialization(self):
        """Test labeler initialization"""
        mock_client = Mock()
        mock_logger = Mock()
        
        labeler = MistralAspectLabeler(
            client=mock_client,
            model_name="test-model",
            prompt_template="Test prompt {INSERT_ASPECT_HERE}",
            logger=mock_logger
        )
        
        assert labeler.client == mock_client
        assert labeler.model == "test-model"
        assert labeler.prompt_template == "Test prompt {INSERT_ASPECT_HERE}"
        assert labeler.logger == mock_logger

    def test_extract_json_success(self):
        """Test successful JSON extraction"""
        mock_client = Mock()
        mock_logger = Mock()
        
        labeler = MistralAspectLabeler(
            client=mock_client,
            model_name="test-model",
            prompt_template="Test prompt {INSERT_ASPECT_HERE}",
            logger=mock_logger
        )
        
        test_text = 'Some text {"labels": ["label1", "label2"]} more text'
        result = labeler._extract_json(test_text)
        
        assert result == {"labels": ["label1", "label2"]}

    def test_extract_json_failure(self):
        """Test JSON extraction failure"""
        mock_client = Mock()
        mock_logger = Mock()
        
        labeler = MistralAspectLabeler(
            client=mock_client,
            model_name="test-model",
            prompt_template="Test prompt {INSERT_ASPECT_HERE}",
            logger=mock_logger
        )
        
        test_text = 'Some text without JSON'
        
        with pytest.raises(json.JSONDecodeError):
            labeler._extract_json(test_text)

    @patch('review_analyzer.infrastructure.aspect_labeler.MistralAspectLabeler._extract_json')
    def test_label_aspect_success(self, mock_extract_json):
        """Test successful aspect labeling"""
        mock_client = Mock()
        mock_logger = Mock()
        
        mock_response = {
            "message": {"content": '{"labels": ["visuals", "rendering"]}'}
        }
        mock_client.chat.return_value = mock_response
        mock_extract_json.return_value = {"labels": ["visuals", "rendering"]}
        
        labeler = MistralAspectLabeler(
            client=mock_client,
            model_name="test-model",
            prompt_template="Test prompt {INSERT_ASPECT_HERE}",
            logger=mock_logger
        )
        
        result = labeler.label_aspect("graphics")
        
        assert result == ["visuals", "rendering"]
        mock_client.chat.assert_called_once()
        mock_extract_json.assert_called_once()

    def test_label_aspect_exception_handling(self):
        """Test exception handling during labeling"""
        mock_client = Mock()
        mock_logger = Mock()
        
        mock_client.chat.side_effect = Exception("API error")
        
        labeler = MistralAspectLabeler(
            client=mock_client,
            model_name="test-model",
            prompt_template="Test prompt {INSERT_ASPECT_HERE}",
            logger=mock_logger
        )
        
        result = labeler.label_aspect("graphics")
        
        assert result == []
        mock_logger.warning.assert_called()

    def test_prompt_template_replacement(self):
        """Test that prompt template correctly replaces placeholder"""
        mock_client = Mock()
        mock_logger = Mock()
        
        mock_response = {
            "message": {"content": '{"labels": ["test"]}'}
        }
        mock_client.chat.return_value = mock_response
        
        labeler = MistralAspectLabeler(
            client=mock_client,
            model_name="test-model",
            prompt_template="Label this aspect: {INSERT_ASPECT_HERE}",
            logger=mock_logger
        )
        
        with patch.object(labeler, '_extract_json') as mock_extract:
            mock_extract.return_value = {"labels": ["test"]}
            labeler.label_aspect("graphics")
            
            # Check that the prompt was called with replaced template
            call_args = mock_client.chat.call_args
            messages = call_args[1]['messages']
            assert "Label this aspect: graphics" in messages[0]['content'] 