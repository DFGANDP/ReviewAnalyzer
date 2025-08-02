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

MODEL_ID = "MHKetbi/Mistral-Small3.1-24B-Instruct-2503:q5_K_L"

def main() -> int:
    log_path = Path("review_analyzer/output/logs/testtesttest_my_prod_logs.txt")
    prompt_path_sentence = Path(r"D:/Programowanie/SteamReviewAnalyzer/review_analyzer/prompts/prompt_extract.txt")
    prompt_path_label = Path(r"D:\Programowanie\SteamReviewAnalyzer\review_analyzer\prompts\prompt_label.txt")

    original_data_path = r"D:/Programowanie/SteamReviewAnalyzer/review_analyzer/input/105600_20250209173825.json"
    original_data_transformed_path = r"review_analyzer/output/output_solid_logger.jsonl"
    csv_liked_path = r'review_analyzer\output\final_label_aspect_logger_liked.csv'
    csv_disliked_path = r'review_analyzer\output\final_label_aspect_logger_disliked.csv'
    reviews_path = r'review_analyzer\output\reviews.csv'

    logger = setup_logger(name = "review-analyzer", handlers=[get_console_handler('INFO'), get_file_handler(str(log_path), 'DEBUG')])
    logger.info("Start przetwarzania…")


    logger.info('Batch Sentence')
    client = Client()

    with open(prompt_path_sentence, encoding="utf-8") as f:
        prompt_sentence = f.read()

    loader = JsonReviewLoader(original_data_path, logger)
    extractor = MistralSentimentAspectExtractor(client, MODEL_ID, prompt_sentence, logger)
    saver = JsonlSaver(original_data_transformed_path, logger)

    service = ReviewProcessingService(extractor, loader, saver, logger)  
    service.run(language="english")

    logger.info('Batch Label')

    with open(prompt_path_label, encoding="utf-8") as f:
        prompt_label = f.read()

    loader = SentenceLoader(original_data_transformed_path, logger)
    reviews, liked_df, disliked_df = loader.load_dataframes()

    logger.debug("Liked preview:\n%s", liked_df.head(5).copy().to_string(index=False))
    logger.debug("Disliked preview:\n%s", disliked_df.head(5).copy().to_string(index=False))

    
    labeler = MistralAspectLabeler(
        client=client,
        model_name="MHKetbi/Mistral-Small3.1-24B-Instruct-2503:q5_K_L",
        prompt_template=prompt_label,
        logger=logger
    )

    saver = DataFrameSaverCsv(logger)

    service = AspectLabelingService(labeler, liked_df, logger, workers=6)
    df_liked_labeled = service.run()
    saver.save(df_liked_labeled, csv_path=csv_liked_path)

    service = AspectLabelingService(labeler, disliked_df, logger, workers=6)
    df_disliked_labeled = service.run()
    saver.save(df_disliked_labeled, csv_path=csv_disliked_path)

    saver.save(reviews)


    logger.info("Batch Analysis")

    analyze_and_save(
        label="liked",
        csv_path=r"review_analyzer\output\final_label_aspect_logger_liked.csv",
        output_path=r"review_analyzer\output\analysis\analysis_liked.json",
        logger=logger,
    )

    analyze_and_save(
        label="disliked",
        csv_path=r"review_analyzer\output\final_label_aspect_logger_disliked.csv",
        output_path=r"review_analyzer\output\analysis\analysis_disliked.json",
        logger=logger,
    )

    logger.info("Zakończono.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())