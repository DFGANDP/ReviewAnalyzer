from pathlib import Path
import logging

from ollama import Client
from review_analyzer.infrastructure.json_loader import JsonReviewLoader
from review_analyzer.infrastructure.mistral_extractor import MistralSentimentAspectExtractor
from review_analyzer.infrastructure.json_saver import JsonlSaver
from review_analyzer.service.review_sentence_processing_service import ReviewProcessingService

from review_analyzer.infrastructure.log_handlers.console_handler import get_console_handler
from review_analyzer.infrastructure.log_handlers.file_handler import get_file_handler
from review_analyzer.infrastructure.log_handlers.setup_logging import setup_logger  # zakładam że konfiguruje root

MODEL_ID = "MHKetbi/Mistral-Small3.1-24B-Instruct-2503:q5_K_L"

def main() -> int:
    # Konfiguracja logowania TYLKO raz, na starcie
    log_path = Path("review_analyzer/output/logs/my_dev_logs.txt")
    prompt_path = Path(r"D:/Programowanie/SteamReviewAnalyzer/review_analyzer/prompts/prompt_extract.txt")
    data_path = r"D:/Programowanie/SteamReviewAnalyzer/review_analyzer/input/105600_20250209173825.json"
    output_path = r"review_analyzer/output/output_debug_logger.jsonl"

    logger = setup_logger(name = "review-analyzer", handlers=[get_console_handler('INFO'), get_file_handler(str(log_path), 'DEBUG')])
    logger.info("Start przetwarzania…")
    client = Client()
    
    with prompt_path.open(encoding="utf-8") as f:
        prompt = f.read()

    loader = JsonReviewLoader(data_path, logger)
    extractor = MistralSentimentAspectExtractor(client, MODEL_ID, prompt, logger)
    saver = JsonlSaver(output_path, logger)

    service = ReviewProcessingService(extractor, loader, saver, logger, limit=10)

    service.run(language="english")
    logger.info("Zakończono.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
