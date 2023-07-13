import os
from typing import List
from services.evaluator.evaluator import PolarityEvaluator
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, AnalyzeSentimentResult

class AzureEvaluator(PolarityEvaluator):
  def __init__(self):
    self.endpoint = os.environ['AZURE_LANGUAGE_ENDPOINT']
    self.key = os.environ["AZURE_LANGUAGE_KEY"]

    self.text_analytics_client = TextAnalyticsClient(self.endpoint, AzureKeyCredential(self.key))

  def get_polarity(self, text: str) -> float:
    response = self.text_analytics_client.analyze_sentiment([text])
    docs: List[AnalyzeSentimentResult] = [doc for doc in response if not doc.is_error]
    
    return docs[0].confidence_scores.positive  
    