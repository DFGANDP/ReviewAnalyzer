from pathlib import Path
import pandas as pd
from review_analyzer.infrastructure.sentence_loader import SentenceLoader
from review_analyzer.infrastructure.sentence_analyzer import ValidReviewAspectAnalyzer, ErrorReviewAnalyzer, FullReviewAnalyzer

from review_analyzer.infrastructure.log_handlers.console_handler import get_console_handler
from review_analyzer.infrastructure.log_handlers.file_handler import get_file_handler
from review_analyzer.infrastructure.log_handlers.setup_logging import setup_logger 

if __name__ == "__main__":
    data_path = r"review_analyzer\output\output_solid.jsonl"
    log_path = Path("review_analyzer/output/logs/my_prod_label_logs.txt")

    logger = setup_logger(name = "review-analyzer", handlers=[get_console_handler('INFO'), get_file_handler(str(log_path), 'DEBUG')])
    logger.info("Start przetwarzania…")

    loader = SentenceLoader(data_path, logger)
    reviews_df, liked_df, disliked_df = loader.load_dataframes()

    logger.debug("Liked preview:\n%s", liked_df.head(5).copy().to_string(index=False))
    logger.debug("Liked preview:\n%s", liked_df.head(5).copy().to_string(index=False))
    logger.debug("Liked preview:\n%s", liked_df.head(5).copy().to_string(index=False))

    full_analyzer = FullReviewAnalyzer(
            liked_analyzer=ValidReviewAspectAnalyzer(label="liked"),
            disliked_analyzer=ValidReviewAspectAnalyzer(label="disliked"),
            error_analyzer=ErrorReviewAnalyzer(),
        )

    full_analyzer.run(liked_df=liked_df, disliked_df=disliked_df, error_df=reviews_df)