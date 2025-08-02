from pathlib import Path
from ollama import Client

from review_analyzer.infrastructure.aspect_labeler import MistralAspectLabeler
from review_analyzer.service.aspect_labeling_service import AspectLabelingService
from review_analyzer.infrastructure.sentence_loader import SentenceLoader
from review_analyzer.infrastructure.dataframe_saver import DataFrameSaverCsv

from review_analyzer.infrastructure.log_handlers.console_handler import get_console_handler
from review_analyzer.infrastructure.log_handlers.file_handler import get_file_handler
from review_analyzer.infrastructure.log_handlers.setup_logging import setup_logger 

MODEL_ID = "MHKetbi/Mistral-Small3.1-24B-Instruct-2503:q5_K_L"

if __name__ == "__main__":
    log_path = Path("review_analyzer/output/logs/my_prod_label_logs.txt")
    prompt_path = Path(r"D:\Programowanie\SteamReviewAnalyzer\review_analyzer\prompts\prompt_label.txt")
    data_path = r"review_analyzer\output\output_solid_logger.jsonl"
    csv_liked_path = r'review_analyzer\output\final_label_aspect_logger_liked.csv'
    csv_disliked_path = r'review_analyzer\output\final_label_aspect_logger_disliked.csv'
    logger = setup_logger(name = "review-analyzer", handlers=[get_console_handler('INFO'), get_file_handler(str(log_path), 'DEBUG')])
    logger.info("Start przetwarzania…")

    client = Client()

    with open(prompt_path, encoding="utf-8") as f:
        prompt = f.read()

    loader = SentenceLoader(data_path, logger)
    _, liked_df, disliked_df = loader.load_dataframes()

    logger.debug("Liked preview:\n%s", liked_df.head(5).copy().to_string(index=False))
    logger.debug("Disliked preview:\n%s", disliked_df.head(5).copy().to_string(index=False))

    
    labeler = MistralAspectLabeler(
        client=client,
        model_name="MHKetbi/Mistral-Small3.1-24B-Instruct-2503:q5_K_L",
        prompt_template=prompt,
        logger=logger
    )

    saver = DataFrameSaverCsv(logger)

    service = AspectLabelingService(labeler, liked_df, logger, workers=6)
    df_liked_labeled = service.run()
    saver.save(df_liked_labeled, csv_path=csv_liked_path)

    service = AspectLabelingService(labeler, disliked_df, logger, workers=6)
    df_disliked_labeled = service.run()
    saver.save(df_disliked_labeled, csv_path=csv_disliked_path)
