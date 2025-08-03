import argparse
from review_analyzer.config import MODEL_ID, PATHS
from review_analyzer.presentation.runner import run

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--language", default="english")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    run(PATHS, MODEL_ID, workers=args.workers, language=args.language, limit=args.limit)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
