# infrastructure/json_loader.py

import json
import os
import re
from typing import List
from logging import Logger

from review_analyzer.domain.models import Review
from review_analyzer.domain.interfaces import ReviewRepository


class JsonReviewLoader(ReviewRepository):
    def __init__(self, filepath: str, logger: Logger):
        self.filepath = filepath
        self.logger = logger
        self.appid = self._extract_appid(filepath)
        
    def _extract_appid(self, filename: str) -> int:
        # Zakładamy że plik nazywa się w formacie: {appid}_{timestamp}.json
        match = re.match(r"(\d+)_\d+\.json$", os.path.basename(filename))
        if not match:
            self.logger.error("Nieprawidłowa nazwa pliku: %s", filename)
            raise ValueError(f"Nieprawidłowa nazwa pliku: {filename}")
        return int(match.group(1))

    def load_reviews(self, language: str = None) -> List[Review]:
        '''
        Zwraca listę Review. Jeśli `language` jest podane, filtruje po nim.
        '''
        self.logger.info("Wczytywanie recenzji z pliku: %s", self.filepath)
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        reviews = data.get("reviews", [])
        result = []

        if language:
            self.logger.debug("Filtrowanie recenzji po języku: %s", language)

        for r in reviews:
            if language and r.get("language") != language:
                continue

            result.append(Review(
                appid=self.appid,
                recommendationid=r.get("recommendationid", ""),
                language=r.get("language", ""),
                review=r.get("review", ""),
                votes_funny=r.get("votes_funny", 0),
                voted_up=r.get("voted_up", False)
            ))
            
        self.logger.info("Załadowano %d recenzji (z %d oryginalnych)", len(result), len(reviews))
        return result
