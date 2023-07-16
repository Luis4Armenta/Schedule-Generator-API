from typing import List, Tuple
from dotenv import dotenv_values
from services.text_analyzer.text_analyzer import TextAnalyzer
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, AnalyzeSentimentResult

class AzureTextAnalyzer(TextAnalyzer):
  def __init__(self):
    config = dotenv_values('.env')
    
    self.endpoint = config['AZURE_LANGUAGE_ENDPOINT']
    self.key = config["AZURE_LANGUAGE_KEY"]

    self.text_analytics_client = TextAnalyticsClient(self.endpoint, AzureKeyCredential(self.key))

  def analyze_sentiment(self, text: str) -> Tuple[float, float, float]:
    response = self.text_analytics_client.analyze_sentiment([text])
    docs: List[AnalyzeSentimentResult] = [doc for doc in response if not doc.is_error]
    
    positive_score = docs[0].confidence_scores.positive
    neutral_score = docs[0].confidence_scores.neutral
    negative_score = docs[0].confidence_scores.negative
    return (positive_score, neutral_score, negative_score)
    