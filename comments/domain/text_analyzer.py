from typing import Tuple
from abc import ABC, abstractclassmethod
from typing import List

from comments.domain.comment import SentimentAnalysis

class TextAnalyzer(ABC):

  @abstractclassmethod
  def analyze_sentiment(self, text: str) -> SentimentAnalysis:
    pass
  
  def analyze_sentiment_by_block(self, texts: List[str]) -> List[SentimentAnalysis]:
    pass