import pytest
from unittest.mock import Mock, MagicMock, patch
from review_analyzer.service.review_sentence_processing_service import ReviewProcessingService


class TestReviewProcessingService:
    """Test suite for ReviewProcessingService"""

    def test_service_initialization(self):
        """Test service initialization with correct parameters"""
        # Arrange
        mock_extractor = Mock()
        mock_loader = Mock()
        mock_saver = Mock()
        mock_logger = Mock()

        # Act
        service = ReviewProcessingService(
            extractor=mock_extractor,
            loader=mock_loader,
            saver=mock_saver,
            logger=mock_logger,
            workers=4,
            limit=100
        )

        # Assert
        assert service.extractor == mock_extractor
        assert service.loader == mock_loader
        assert service.saver == mock_saver
        assert service.logger == mock_logger
        assert service.workers == 4
        assert service.limit == 100

    def test_service_initialization_default_values(self):
        """Test service initialization with default values"""
        # Arrange
        mock_extractor = Mock()
        mock_loader = Mock()
        mock_saver = Mock()
        mock_logger = Mock()

        # Act
        service = ReviewProcessingService(
            extractor=mock_extractor,
            loader=mock_loader,
            saver=mock_saver,
            logger=mock_logger
        )

        # Assert
        assert service.workers == 4
        assert service.limit is None

    @patch('review_analyzer.service.review_sentence_processing_service.Pool')
    def test_run_successful_processing(self, mock_pool_class):
        """Test successful processing of reviews"""
        # Arrange
        mock_extractor = Mock()
        mock_loader = Mock()
        mock_saver = Mock()
        mock_logger = Mock()
        mock_pool = Mock()

        # Mock review objects
        review1 = Mock()
        review1.review = "Great game"
        review1.appid = 123
        review1.recommendationid = 35131

        review2 = Mock()
        review2.review = "Amazing graphics"
        review2.appid = 123
        review2.recommendationid = 35132

        mock_loader.load_reviews.return_value = [review1, review2]
        mock_pool_class.return_value.__enter__.return_value = mock_pool
        mock_pool.imap_unordered.return_value = [
            {"appid": 123, "recommendationid": 35131, "liked": ["great"], "disliked": [], "original_review": "Great game"},
            {"appid": 123, "recommendationid": 35132, "liked": ["amazing"], "disliked": [], "original_review": "Amazing graphics"}
        ]

        service = ReviewProcessingService(
            extractor=mock_extractor,
            loader=mock_loader,
            saver=mock_saver,
            logger=mock_logger,
            workers=2
        )

        # Act
        result = service.run(language="english")

        # Assert
        mock_loader.load_reviews.assert_called_once_with("english")
        mock_pool_class.assert_called_once_with(processes=2)
        mock_saver.save.assert_called_once()
        mock_logger.info.assert_called()
        assert len(result) == 2

    @patch('review_analyzer.service.review_sentence_processing_service.Pool')
    def test_run_with_limit(self, mock_pool_class):
        """Test processing with limit parameter"""
        # Arrange
        mock_extractor = Mock()
        mock_loader = Mock()
        mock_saver = Mock()
        mock_logger = Mock()
        mock_pool = Mock()

        # Mock review objects
        reviews = [Mock() for _ in range(10)]
        for i, review in enumerate(reviews):
            review.review = f"Review {i}"
            review.appid = 123
            review.recommendationid = 35130 + i

        mock_loader.load_reviews.return_value = reviews
        mock_pool_class.return_value.__enter__.return_value = mock_pool
        mock_pool.imap_unordered.return_value = [
            {"appid": 123, "recommendationid": 35130 + i, "liked": [f"good{i}"], "disliked": [], "original_review": f"Review {i}"}
            for i in range(5)
        ]

        service = ReviewProcessingService(
            extractor=mock_extractor,
            loader=mock_loader,
            saver=mock_saver,
            logger=mock_logger,
            workers=2,
            limit=5
        )

        # Act
        result = service.run(language="english")

        # Assert
        assert len(result) == 5
        mock_logger.debug.assert_called_with("Przetwarzanie %d recenzji", 5)

    @patch('review_analyzer.service.review_sentence_processing_service.Pool')
    def test_run_processing_exception(self, mock_pool_class):
        """Test handling of processing exceptions"""
        # Arrange
        mock_extractor = Mock()
        mock_loader = Mock()
        mock_saver = Mock()
        mock_logger = Mock()
        mock_pool = Mock()

        mock_loader.load_reviews.return_value = [Mock()]
        mock_pool_class.return_value.__enter__.return_value = mock_pool
        mock_pool.imap_unordered.side_effect = Exception("Processing error")

        service = ReviewProcessingService(
            extractor=mock_extractor,
            loader=mock_loader,
            saver=mock_saver,
            logger=mock_logger,
            workers=1
        )

        # Act
        result = service.run(language="english")

        # Assert
        assert result is None
        mock_logger.error.assert_called_with("Błąd podczas przetwarzania recenzji: %s", "Processing error", exc_info=True)

    @patch('review_analyzer.service.review_sentence_processing_service.Pool')
    def test_run_save_exception(self, mock_pool_class):
        """Test handling of save exceptions"""
        # Arrange
        mock_extractor = Mock()
        mock_loader = Mock()
        mock_saver = Mock()
        mock_logger = Mock()
        mock_pool = Mock()

        # Mock review objects
        review = Mock()
        review.review = "Great game"
        review.appid = 123
        review.recommendationid = 35131

        mock_loader.load_reviews.return_value = [review]
        mock_pool_class.return_value.__enter__.return_value = mock_pool
        mock_pool.imap_unordered.return_value = [
            {"appid": 123, "recommendationid": 35131, "liked": ["great"], "disliked": [], "original_review": "Great game"}
        ]
        mock_saver.save.side_effect = Exception("Save error")

        service = ReviewProcessingService(
            extractor=mock_extractor,
            loader=mock_loader,
            saver=mock_saver,
            logger=mock_logger,
            workers=1
        )

        # Act
        result = service.run(language="english")

        # Assert
        assert len(result) == 1
        mock_logger.error.assert_called_with("Błąd podczas zapisu wyników: %s", "Save error", exc_info=True)

    @patch('review_analyzer.service.review_sentence_processing_service.Pool')
    def test_run_without_language_filter(self, mock_pool_class):
        """Test processing without language filter"""
        # Arrange
        mock_extractor = Mock()
        mock_loader = Mock()
        mock_saver = Mock()
        mock_logger = Mock()
        mock_pool = Mock()

        mock_loader.load_reviews.return_value = []
        mock_pool_class.return_value.__enter__.return_value = mock_pool
        mock_pool.imap_unordered.return_value = []

        service = ReviewProcessingService(
            extractor=mock_extractor,
            loader=mock_loader,
            saver=mock_saver,
            logger=mock_logger,
            workers=1
        )

        # Act
        service.run()

        # Assert
        mock_loader.load_reviews.assert_called_once_with(None)
