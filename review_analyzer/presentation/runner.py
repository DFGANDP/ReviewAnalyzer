from pathlib import Path

from ollama import Client

# ASPECT
from review_analyzer.infrastructure.json_loader import JsonReviewLoader
from review_analyzer.infrastructure.mistral_extractor import MistralSentimentAspectExtractor
from review_analyzer.infrastructure.json_saver import JsonlSaver
from review_analyzer.service.review_sentence_processing_service import ReviewProcessingService

# LABEL
from review_analyzer.infrastructure.aspect_labeler import MistralAspectLabeler
from review_analyzer.service.aspect_labeling_service import AspectLabelingService
from review_analyzer.infrastructure.sentence_loader import SentenceLoader
from review_analyzer.infrastructure.dataframe_saver import DataFrameSaverCsv

# Analysis
from review_analyzer.infrastructure.utils import analyze_and_save

# LOGGER
from review_analyzer.infrastructure.log_handlers.console_handler import get_console_handler
from review_analyzer.infrastructure.log_handlers.file_handler import get_file_handler
from review_analyzer.infrastructure.log_handlers.setup_logging import setup_logger 

def sentence_batch(client, logger, PATHS, MODEL_ID, workers=6, language='english', limit=None):
    logger.info('Batch Sentence')
    with open(PATHS['sentence_prompt'], encoding="utf-8") as f:
        prompt_sentence = f.read()

    loader = JsonReviewLoader(PATHS['raw_reviews'], logger)
    extractor = MistralSentimentAspectExtractor(client, MODEL_ID, prompt_sentence, logger)
    saver = JsonlSaver(PATHS['sentence_output'], logger)

    service = ReviewProcessingService(extractor, loader, saver, logger, workers, limit)  
    service.run(language)

def label_batch(client, logger, PATHS, MODEL_ID, workers=6, limit=None):
    logger.info('Batch Label')

    with open(PATHS['label_prompt'], encoding="utf-8") as f:
        prompt_label = f.read()

    loader = SentenceLoader(PATHS['sentence_output'], logger)
    reviews, liked_df, disliked_df = loader.load_dataframes()

    logger.debug("Liked preview:\n%s", liked_df.head(5).copy().to_string(index=False))
    logger.debug("Disliked preview:\n%s", disliked_df.head(5).copy().to_string(index=False))

    
    labeler = MistralAspectLabeler(
        client=client,
        model_name=MODEL_ID,
        prompt_template=prompt_label,
        logger=logger
    )

    saver = DataFrameSaverCsv(logger)

    service = AspectLabelingService(labeler, liked_df, logger, workers)
    df_liked_labeled = service.run()
    saver.save(df_liked_labeled, csv_path=PATHS['liked_csv'])

    service = AspectLabelingService(labeler, disliked_df, logger, workers, limit)
    df_disliked_labeled = service.run()
    saver.save(df_disliked_labeled, csv_path=PATHS['disliked_csv'])

    saver.save(reviews, PATHS['review_csv'])

def analysis_batch(logger, PATHS):
    logger.info("Batch Analysis")

    analyze_and_save(
        label="liked",
        csv_path=PATHS['liked_csv'],
        output_path=PATHS['liked_analysis'],
        logger=logger,
        charts_dir=PATHS['charts']
    )

    analyze_and_save(
        label="disliked",
        csv_path=PATHS['disliked_csv'],
        output_path=PATHS['disliked_analysis'],
        logger=logger,
        charts_dir=PATHS['charts']
    )

def run(PATHS, MODEL_ID, workers=6, language='english', limit=None) -> int:
    logger = setup_logger(name = "review-analyzer", handlers=[get_console_handler('INFO'), get_file_handler(PATHS['log'], 'DEBUG')])
    logger.info("Start przetwarzania…")
    logger.info('ARG CONFIG: %s, %s, %d,%s, %s',PATHS, MODEL_ID, workers, language, limit)

    client = Client()

    sentence_batch(client, logger, PATHS, MODEL_ID, workers=6, language='english', limit=limit)
    label_batch(client, logger, PATHS, MODEL_ID, workers=6, limit=limit)
    analysis_batch(logger, PATHS)

    logger.info("Zakończono.")
    return 0