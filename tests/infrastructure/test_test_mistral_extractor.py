from unittest.mock import MagicMock, Mock
from review_analyzer.infrastructure.mistral_extractor import MistralSentimentAspectExtractor

def test_extractor_parses_response():
    mock_client = MagicMock()
    mock_logger = Mock()
    mock_client.chat.return_value = {
        "message": {"content": '{"liked": ["fun"], "disliked": ["bugs"]}'}
    }

    extractor = MistralSentimentAspectExtractor(
        client=mock_client,
        model_name="dummy-model",
        prompt="Extract from: {INSERT_REVIEW_HERE}",
        logger=mock_logger
    )

    review = MagicMock()
    review.review = "I liked the gameplay but there were bugs."
    review.appid = 101
    review.recommendationid = "abc"

    result = extractor.extract_sentence_sentiment(review)

    assert result["liked"] == ["fun"]
    assert result["disliked"] == ["bugs"]
    assert result["appid"] == 101
    assert result["recommendationid"] == "abc"
