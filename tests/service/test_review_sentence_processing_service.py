from unittest.mock import MagicMock, Mock
from review_analyzer.service.review_sentence_processing_service import ReviewProcessingService

def test_processing_service_runs():
    # Mock components
    mock_logger = Mock()
    mock_loader = MagicMock()
    mock_saver = MagicMock()
    mock_extractor = MagicMock()

    review_obj = MagicMock()
    review_obj.review = "Good game"
    review_obj.appid = 123
    review_obj.recommendationid = 35131

    mock_loader.load_reviews.return_value = [review_obj]
    mock_extractor.extract_sentence_sentiment.return_value = {
        "appid": 123, "recommendationid": 35131, "liked": ["good"], "disliked": [], "original_review": "Good game"
    }

    service = ReviewProcessingService(
        extractor=mock_extractor,
        loader=mock_loader,
        saver=mock_saver,
        logger=mock_logger,
        workers=1
    )

    service.run(language="english")

    mock_loader.load_reviews.assert_called_once_with("english")
    mock_extractor.extract_sentence_sentiment.assert_called_once()
    mock_saver.save.assert_called_once()
