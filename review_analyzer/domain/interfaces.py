# domain/interfaces.py

from abc import ABC, abstractmethod
from typing import List, Dict
from review_analyzer.domain.models import Review
import pandas as pd

class ReviewRepository(ABC):
    @abstractmethod
    def load_reviews(self) -> List[Review]:
        pass

class AspectExtractor(ABC):
    @abstractmethod
    def extract_aspects(self, reviews: List[Review]) -> Dict[str, List[str]]:
        """
        Zwraca słownik:
        {
            "grafika": ["amazing visuals", "great textures"],
            "cena": ["too expensive", "worth every penny"]
        }
        """
        ...

class ReviewAspectExtractor(ABC):
    @abstractmethod
    def extract_sentence_sentiment(self, review: Review) -> dict:
        pass

class ReviewAnalyzer(ABC):
    @abstractmethod
    def analyze_data(self, data: pd.DataFrame) -> Dict:
        ...

class DataFrameSaver(ABC):
    @abstractmethod
    def save(self, dataframe: pd.DataFrame, csv_path: str) -> None:
        ...

class DataFrameLoader(ABC):
    @abstractmethod
    def load(self, csv_path: str) -> None:
        ...