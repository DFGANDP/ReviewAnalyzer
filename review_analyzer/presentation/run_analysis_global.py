from pathlib import Path
import pandas as pd

from review_analyzer.infrastructure.global_analyzer import GlobalAspectAnalyzer
from review_analyzer.infrastructure.dataframe_loader import DataFrameLoaderCsv
from review_analyzer.infrastructure.json_saver import JsonSaver

from review_analyzer.infrastructure.log_handlers.console_handler import get_console_handler
from review_analyzer.infrastructure.log_handlers.file_handler import get_file_handler
from review_analyzer.infrastructure.log_handlers.setup_logging import setup_logger 

def analyze_and_save(label: str, csv_path: str, output_path: str, logger):
    loader = DataFrameLoaderCsv(logger)
    df = loader.load(csv_path)

    df["labels"] = df["labels"].astype(str).str.strip()

    logger.debug("%s preview:\n%s", label.capitalize(), df.head(5).copy().to_string(index=False))

    analyzer = GlobalAspectAnalyzer(label=label)
    analysis = analyzer.analyze_data(df)
    analyzer.generate_charts()

    saver = JsonSaver(output_path, logger)
    saver.save(analysis)


if __name__ == "__main__":
    log_path = Path("review_analyzer/output/logs/my_prod_label_logs_analiza.txt")

    logger = setup_logger(name = "review-analyzer", handlers=[get_console_handler('INFO'), get_file_handler(str(log_path), 'DEBUG')])
    logger.info("Start przetwarzania…")

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