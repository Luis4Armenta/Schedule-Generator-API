import os

from typing import List, Tuple

from comments.domain.comment import SentimentAnalysis
from comments.domain.text_analyzer import TextAnalyzer

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, AnalyzeSentimentResult


class AzureTextAnalyzer(TextAnalyzer):
  def __init__(self):    
    self.endpoint = os.environ['AZURE_LANGUAGE_ENDPOINT']
    self.key = os.environ["AZURE_LANGUAGE_KEY"]

    self.text_analytics_client = TextAnalyticsClient(self.endpoint, AzureKeyCredential(self.key))

  def analyze_sentiment(self, text: str) -> SentimentAnalysis:
    response = self.text_analytics_client.analyze_sentiment([text], language='es')
    docs: List[AnalyzeSentimentResult] = [doc for doc in response if not doc.is_error]
    
    sentiment_analysis: SentimentAnalysis = SentimentAnalysis(
      positive_score = float(docs[0].confidence_scores['positive']),
      neutral_score = float(docs[0].confidence_scores['neutral']),
      negative_score = float(docs[0].confidence_scores['negative']),
    )
    return sentiment_analysis
  
  
  def analyze_sentiment_by_block(self, texts: List[str]) -> List[SentimentAnalysis]:
    requests: List[List[str]] = split_into_blocks(texts, 10)
    response: List[SentimentAnalysis]  = []
    
    for request in requests:
      res = self.text_analytics_client.analyze_sentiment(request, language='es')
      
      for doc in res:
        scores: Tuple[float, float, float]= (0.0, 0.0, 0.0)
        if not doc.is_error:
          scores = (
            float(doc.confidence_scores['positive']),
            float(doc.confidence_scores['neutral']),
            float(doc.confidence_scores['negative']),
          )
        
        else:
          scores = (
            0.33,
            0.33,
            0.34
          )
      
        response.append(SentimentAnalysis(
          positive_score=scores[0],
          neutral_score=scores[1],
          negative_score=scores[2],
        ))

        
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
