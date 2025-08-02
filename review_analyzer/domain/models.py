# domain/models.py

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Review:
    appid: int # wycaigane z filename nie z json
    recommendationid: int
    language: str 
    review: str # tekst review
    votes_funny: int 
    voted_up: bool # jesli true - gra sie podobala 

@dataclass
class ExtractedAspects:
    appid: int
    aspects: Dict[str, List[str]]  # np. {"grafika": ["ładna", "płynna"]}
    