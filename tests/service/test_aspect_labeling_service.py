import pytest
import pandas as pd
from unittest.mock import Mock, MagicMock, patch
from review_analyzer.service.aspect_labeling_service import AspectLabelingService


class TestAspectLabelingService:
    """Test suite for AspectLabelingService"""

    def test_service_initialization(self):
        """Test service initialization with correct parameters"""
        # Arrange
        mock_labeler = Mock()
        mock_logger = Mock()
        test_df = pd.DataFrame({'aspect': ['test1', 'test2']})

        # Act
        service = AspectLabelingService(
            labeler=mock_labeler,
            aspect_df=test_df,
            logger=mock_logger,
            workers=4,
            limit=100
        )

        # Assert
        assert service.labeler == mock_labeler
        assert service.aspect_df.equals(test_df)
        assert service.logger == mock_logger
        assert service.workers == 4
        assert service.limit == 100

    def test_service_initialization_default_values(self):
        """Test service initialization with default values"""
        # Arrange
        mock_labeler = Mock()
        mock_logger = Mock()
        test_df = pd.DataFrame({'aspect': ['test1', 'test2']})

        # Act
        service = AspectLabelingService(
            labeler=mock_labeler,
            aspect_df=test_df,
            logger=mock_logger
        )

        # Assert
        assert service.workers == 4
        assert service.limit is None

    @patch('review_analyzer.service.aspect_labeling_service.Pool')
    def test_run_successful_processing(self, mock_pool_class):
        """Test successful processing of aspects"""
        # Arrange
        mock_labeler = Mock()
        mock_logger = Mock()
        mock_pool = Mock()

        test_df = pd.DataFrame({
            'aspect': ['graphics', 'gameplay', 'story'],
            'other_column': ['value1', 'value2', 'value3']
        })

        mock_pool_class.return_value.__enter__.return_value = mock_pool
        mock_pool.imap_unordered.return_value = [
            ['visuals', 'rendering'],
            ['mechanics', 'controls'],
            ['narrative', 'plot']
        ]

        service = AspectLabelingService(
            labeler=mock_labeler,
            aspect_df=test_df,
            logger=mock_logger,
            workers=2
        )

        # Act
        result = service.run()

        # Assert
        assert len(result) == 6  # 3 aspects * 2 labels each
        assert 'labels' in result.columns
        assert 'aspect' in result.columns
        assert 'other_column' in result.columns
        mock_logger.debug.assert_called_with("Parametry: workers=%d, limit=%s", 2, None)
        mock_logger.info.assert_called_with("Przetwarzanie %d aspektów", 3)

    @patch('review_analyzer.service.aspect_labeling_service.Pool')
    def test_run_with_limit(self, mock_pool_class):
        """Test processing with limit parameter"""
        # Arrange
        mock_labeler = Mock()
        mock_logger = Mock()
        mock_pool = Mock()

        test_df = pd.DataFrame({
            'aspect': [f'aspect{i}' for i in range(10)]
        })

        mock_pool_class.return_value.__enter__.return_value = mock_pool
        mock_pool.imap_unordered.return_value = [
            [f'label{i}_1', f'label{i}_2'] for i in range(5)
        ]

        service = AspectLabelingService(
            labeler=mock_labeler,
            aspect_df=test_df,
            logger=mock_logger,
            workers=2,
            limit=5
        )

        # Act
        result = service.run()

        # Assert
        assert len(result) == 10  # 5 aspects * 2 labels each
        mock_logger.debug.assert_called_with("Parametry: workers=%d, limit=%s", 2, 5)
        mock_logger.info.assert_called_with("Przetwarzanie %d aspektów", 5)

    @patch('review_analyzer.service.aspect_labeling_service.Pool')
    def test_run_with_empty_dataframe(self, mock_pool_class):
        """Test processing with empty dataframe"""
        # Arrange
        mock_labeler = Mock()
        mock_logger = Mock()
        mock_pool = Mock()

        test_df = pd.DataFrame({'aspect': []})

        mock_pool_class.return_value.__enter__.return_value = mock_pool
        mock_pool.imap_unordered.return_value = []

        service = AspectLabelingService(
            labeler=mock_labeler,
            aspect_df=test_df,
            logger=mock_logger,
            workers=2
        )

        # Act
        result = service.run()

        # Assert
        assert len(result) == 0
        mock_logger.info.assert_called_with("Przetwarzanie %d aspektów", 0)

    @patch('review_analyzer.service.aspect_labeling_service.Pool')
    def test_run_with_single_label_per_aspect(self, mock_pool_class):
        """Test processing when each aspect has only one label"""
        # Arrange
        mock_labeler = Mock()
        mock_logger = Mock()
        mock_pool = Mock()

        test_df = pd.DataFrame({
            'aspect': ['graphics', 'gameplay'],
            'other_column': ['value1', 'value2']
        })

        mock_pool_class.return_value.__enter__.return_value = mock_pool
        mock_pool.imap_unordered.return_value = [
            ['visuals'],
            ['mechanics']
        ]

        service = AspectLabelingService(
            labeler=mock_labeler,
            aspect_df=test_df,
            logger=mock_logger,
            workers=2
        )

        # Act
        result = service.run()

        # Assert
        assert len(result) == 2  # 2 aspects * 1 label each
        assert result['labels'].tolist() == ['visuals', 'mechanics']

    @patch('review_analyzer.service.aspect_labeling_service.Pool')
    def test_run_with_multiple_labels_per_aspect(self, mock_pool_class):
        """Test processing when each aspect has multiple labels"""
        # Arrange
        mock_labeler = Mock()
        mock_logger = Mock()
        mock_pool = Mock()

        test_df = pd.DataFrame({
            'aspect': ['graphics'],
            'other_column': ['value1']
        })

        mock_pool_class.return_value.__enter__.return_value = mock_pool
        mock_pool.imap_unordered.return_value = [
            ['visuals', 'rendering', 'textures', 'lighting']
        ]

        service = AspectLabelingService(
            labeler=mock_labeler,
            aspect_df=test_df,
            logger=mock_logger,
            workers=1
        )

        # Act
        result = service.run()

        # Assert
        assert len(result) == 4  # 1 aspect * 4 labels
        assert result['labels'].tolist() == ['visuals', 'rendering', 'textures', 'lighting']

    @patch('review_analyzer.service.aspect_labeling_service.Pool')
    def test_run_preserves_original_columns(self, mock_pool_class):
        """Test that original dataframe columns are preserved"""
        # Arrange
        mock_labeler = Mock()
        mock_logger = Mock()
        mock_pool = Mock()

        test_df = pd.DataFrame({
            'aspect': ['graphics', 'gameplay'],
            'sentiment': ['positive', 'negative'],
            'confidence': [0.9, 0.8]
        })

        mock_pool_class.return_value.__enter__.return_value = mock_pool
        mock_pool.imap_unordered.return_value = [
            ['visuals', 'rendering'],
            ['mechanics', 'controls']
        ]

        service = AspectLabelingService(
            labeler=mock_labeler,
            aspect_df=test_df,
            logger=mock_logger,
            workers=2
        )

        # Act
        result = service.run()

        # Assert
        assert 'aspect' in result.columns
        assert 'sentiment' in result.columns
        assert 'confidence' in result.columns
        assert 'labels' in result.columns
        assert len(result.columns) == 4

    @patch('review_analyzer.service.aspect_labeling_service.Pool')
    def test_run_logging_behavior(self, mock_pool_class):
        """Test that service logs appropriate messages"""
        # Arrange
        mock_labeler = Mock()
        mock_logger = Mock()
        mock_pool = Mock()

        test_df = pd.DataFrame({
            'aspect': ['graphics', 'gameplay']
        })

        mock_pool_class.return_value.__enter__.return_value = mock_pool
        mock_pool.imap_unordered.return_value = [
            ['visuals'],
            ['mechanics']
        ]

        service = AspectLabelingService(
            labeler=mock_labeler,
            aspect_df=test_df,
            logger=mock_logger,
            workers=3,
            limit=None
        )

        # Act
        service.run()

        # Assert
        mock_logger.debug.assert_called_with("Parametry: workers=%d, limit=%s", 3, None)
        mock_logger.info.assert_called_with("Przetwarzanie %d aspektów", 2)

    @patch('review_analyzer.service.aspect_labeling_service.Pool')
    def test_run_resets_index(self, mock_pool_class):
        """Test that result dataframe has reset index"""
        # Arrange
        mock_labeler = Mock()
        mock_logger = Mock()
        mock_pool = Mock()

        test_df = pd.DataFrame({
            'aspect': ['graphics', 'gameplay']
        })

        mock_pool_class.return_value.__enter__.return_value = mock_pool
        mock_pool.imap_unordered.return_value = [
            ['visuals'],
            ['mechanics']
        ]

        service = AspectLabelingService(
            labeler=mock_labeler,
            aspect_df=test_df,
            logger=mock_logger,
            workers=2
        )

        # Act
        result = service.run()

        # Assert
        # Check that index is reset (starts from 0)
        assert result.index.tolist() == [0, 1]

    def test_service_with_none_limit(self):
        """Test service behavior when limit is None"""
        # Arrange
        mock_labeler = Mock()
        mock_logger = Mock()
        test_df = pd.DataFrame({'aspect': ['test1', 'test2']})

        # Act
        service = AspectLabelingService(
            labeler=mock_labeler,
            aspect_df=test_df,
            logger=mock_logger,
            workers=4,
            limit=None
        )

        # Assert
        assert service.limit is None

    def test_service_with_zero_limit(self):
        """Test service behavior when limit is 0"""
        # Arrange
        mock_labeler = Mock()
        mock_logger = Mock()
        test_df = pd.DataFrame({'aspect': ['test1', 'test2']})

        # Act
        service = AspectLabelingService(
            labeler=mock_labeler,
            aspect_df=test_df,
            logger=mock_logger,
            workers=4,
            limit=0
        )

        # Assert
        assert service.limit == 0 