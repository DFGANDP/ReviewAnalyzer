# config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent / 'review_analyzer' # bo odpalam z dir wczesniej

INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
PROMPT_DIR = BASE_DIR / "prompts"
LOG_DIR = OUTPUT_DIR / "logs"
ANALYSIS_DIR = OUTPUT_DIR / "analysis"

MODEL_ID = "MHKetbi/Mistral-Small3.1-24B-Instruct-2503:q5_K_L"

PATHS = {
    "raw_reviews": INPUT_DIR / "105600_20250209173825.json",
    "sentence_prompt": PROMPT_DIR / "prompt_extract.txt",
    "label_prompt": PROMPT_DIR / "prompt_label.txt",
    "sentence_output": OUTPUT_DIR / "output_solid_logger.jsonl",
    "liked_csv": OUTPUT_DIR / "final_label_aspect_logger_liked.csv",
    "disliked_csv": OUTPUT_DIR / "final_label_aspect_logger_disliked.csv",
    "review_csv": OUTPUT_DIR / "reviews.csv",
    "log": LOG_DIR / "my_prod_logs.txt",
    "liked_analysis": ANALYSIS_DIR / "analysis_liked.json",
    "disliked_analysis": ANALYSIS_DIR / "analysis_disliked.json",
}

# Funkcja tworząca wszystkie foldery nadrzędne, jeśli nie istnieją
def ensure_directories_exist():
    for path in PATHS.values():
        path.parent.mkdir(parents=True, exist_ok=True)

# Uruchamiamy ją przy imporcie modułu
ensure_directories_exist()