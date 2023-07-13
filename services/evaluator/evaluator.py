from abc import ABC, abstractclassmethod

class TeacherEvaluator(ABC):
  
  @abstractclassmethod
  def get_polarity(self, text: str) -> float:
    pass