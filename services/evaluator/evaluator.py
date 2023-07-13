from abc import ABC, abstractclassmethod

class PolarityEvaluator(ABC):
  
  @abstractclassmethod
  def get_polarity(self, text: str) -> float:
    pass