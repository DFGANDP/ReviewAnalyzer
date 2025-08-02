from logging import Logger
import pandas as pd
import json
from typing import Tuple, List

class SentenceLoader:
    def __init__(self, jsonl_path: str, logger: Logger):
        self.jsonl_path = jsonl_path
        self.logger = logger

    def _load_jsonl_lines(self) -> List[dict]:
        rows = []
        with open(self.jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                except json.JSONDecodeError as e:
                    self.logger.warning("Błąd dekodowania JSON: %s", e)
                    data = {
                        "original_review": line.strip(),
                        "error": str(e)
                    }
                rows.append(data)
        return rows
    
    def load_dataframes(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        rows = self._load_jsonl_lines()
        df = pd.DataFrame(rows)

        # Główna tabela recenzji
        reviews_df = df[["appid", "recommendationid", "original_review", "error"]].copy()

        # Tabela liked
        liked_df = (
            df.explode("liked")[["appid", "recommendationid", "liked"]]
            .dropna()
            .rename(columns={"liked": "aspect"})
        )

        # Tabela disliked
        disliked_df = (
            df.explode("disliked")[["appid", "recommendationid", "disliked"]]
            .dropna()
            .rename(columns={"disliked": "aspect"})
        )

        self.logger.info("Created liked_df with %d rows", len(liked_df))
        self.logger.info("Created disliked_df with %d rows", len(disliked_df))

        return reviews_df, liked_df, disliked_df