from typing import List, Tuple
from dotenv import dotenv_values
from teachers.infrastructure.text_analyzer.text_analyzer import TextAnalyzer
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, AnalyzeSentimentResult

class AzureTextAnalyzer(TextAnalyzer):
  def __init__(self):
    config = dotenv_values('.env')
    
    self.endpoint = config['AZURE_LANGUAGE_ENDPOINT']
    self.key = config["AZURE_LANGUAGE_KEY"]

    self.text_analytics_client = TextAnalyticsClient(self.endpoint, AzureKeyCredential(self.key))

  def analyze_sentiment(self, text: str) -> Tuple[float, float, float]:
    response = self.text_analytics_client.analyze_sentiment([text], language='es')
    docs: List[AnalyzeSentimentResult] = [doc for doc in response if not doc.is_error]
    
    positive_score = docs[0].confidence_scores['positive']
    neutral_score = docs[0].confidence_scores['neutral']
    negative_score = docs[0].confidence_scores['negative']
    return (positive_score, neutral_score, negative_score)
  
  
  def analyze_sentiment_by_block(self, texts: List[str]) -> List[Tuple[float, float, float]]:
    requests: List[List[str]] = split_into_blocks(texts, 10)
    response: List[Tuple[float, float, float]]  = []
    
    for request in requests:
      res = self.text_analytics_client.analyze_sentiment(request, language='es')
      
      for doc in res:
        if not doc.is_error:
          scores = (
            doc.confidence_scores['positive'],
            doc.confidence_scores['neutral'],
            doc.confidence_scores['negative'],
          )
        
          response.append(scores)
        else:
          scores = (
            0.33,
            0.33,
            0.34
          )
    
    return response
    
def split_into_blocks(strings: List[str], block_size: int) -> List[List[str]]:
  blocks = []
  current_block = []

  for string in strings:
      current_block.append(string)

      if len(current_block) == block_size:
          blocks.append(current_block)
          current_block = []

  if current_block:
      blocks.append(current_block)

  return blocks
