from typing import Optional
from textblob import TextBlob
from services.translator import Translator

from services.evaluator.evaluator import PolarityEvaluator

class TextBlobEvaluator(PolarityEvaluator):
  def __init__(self, translator: Optional[Translator]):
    if translator:
      self.translator = translator
  
  def get_polarity(self, text: str) -> float:
    blob: TextBlob
    
    if self.translator:
      trans_text = self.translator.translate(text)
      blob = TextBlob(trans_text)
    else:
      blob = TextBlob(text)

    polarity = blob.sentiment.polarity
    if polarity:
      return polarity
    else:
      return 0.0
    