from abc import ABC, abstractmethod
from typing import List, Dict

class AspectLabeler(ABC):
    @abstractmethod
    def label_aspect(self, aspect: str) -> List[str]:
        ...