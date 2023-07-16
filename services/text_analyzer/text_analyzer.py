from typing import Tuple
from abc import ABC, abstractclassmethod

class TextAnalyzer(ABC):
  
  @abstractclassmethod
  def analyze_sentiment(self, text: str) -> Tuple[float, float, float]:
    pass