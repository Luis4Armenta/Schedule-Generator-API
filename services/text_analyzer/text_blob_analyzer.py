from typing import Optional,Tuple
from textblob import TextBlob
from services.translator import Translator
from services.text_analyzer.text_analyzer import TextAnalyzer

# class TextBlobEvaluator(TextAnalyzer):
#   def __init__(self, translator: Optional[Translator]):
#     if translator:
#       self.translator = translator
#   
#   def analyze_sentiment(self, text: str) -> Tuple[float, float flaot]:
#     blob: TextBlob
#     
#     if self.translator:
#       trans_text = self.translator.translate(text)
#       blob = TextBlob(trans_text)
#     else:
#       blob = TextBlob(text)
# 
#     polarity = blob.sentiment.polarity
#     if polarity:
#       return polarity
#     else:
#       return 0.0
    