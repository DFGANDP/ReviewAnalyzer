# config.py
from pathlib import Path
from datetime import datetime

# 1. Timestamp na poziomie całego runu
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M")

# 2. Bazowy katalog (tam, gdzie jest ten plik)
BASE_DIR = Path(__file__).resolve().parent

# 3. Foldery z TIMESTAMP
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output" / TIMESTAMP
PROMPT_DIR = BASE_DIR / "prompts"
LOG_DIR = OUTPUT_DIR / "logs"
ANALYSIS_DIR = OUTPUT_DIR / "analysis"

# 4. Ścieżki do plików
PATHS = {
    "raw_reviews": INPUT_DIR / "105600_20250209173825.json",
    "sentence_prompt": PROMPT_DIR / "prompt_extract.txt",
    "label_prompt": PROMPT_DIR / "prompt_label.txt",
    "sentence_output": OUTPUT_DIR / "output_solid_logger.jsonl",
    "liked_csv": OUTPUT_DIR / "final_label_aspect_logger_liked.csv",
    "disliked_csv": OUTPUT_DIR / "final_label_aspect_logger_disliked.csv",
    "review_csv": OUTPUT_DIR / "reviews.csv",
    "log": LOG_DIR / f"PROD_{TIMESTAMP}.log",
    "liked_analysis": ANALYSIS_DIR / "analysis_liked.json",
    "disliked_analysis": ANALYSIS_DIR / "analysis_disliked.json",
    "charts": ANALYSIS_DIR / "charts"
}

# 5. Model ID
MODEL_ID = "MHKetbi/Mistral-Small3.1-24B-Instruct-2503:q5_K_L"

# 6. Tworzenie katalogów
def ensure_directories_exist():
    for path in PATHS.values():
        path.parent.mkdir(parents=True, exist_ok=True)

ensure_directories_exist()
