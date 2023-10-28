from typing import Tuple
from abc import ABC, abstractclassmethod
from typing import List

class TextAnalyzer(ABC):
  
  @abstractclassmethod
  def analyze_sentiment(self, text: str) -> Tuple[float, float, float]:
    pass
  
  def analyze_sentiment_by_block(self, texts: List[str]) -> List[Tuple[float, float, float]]:
    pass