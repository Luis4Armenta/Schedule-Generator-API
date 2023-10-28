from unittest import TestCase
from unittest.mock import patch, Mock, call

from services.text_analyzer.azure_text_analyzer import AzureTextAnalyzer, AnalyzeSentimentResult, split_into_blocks

from typing import List, Tuple, Dict



class TestAzureTextAnalyzer(TestCase):
    @patch('services.text_analyzer.azure_text_analyzer.TextAnalyticsClient')
    def test_analyze_sentiment(self, mock_text_analytics_client):
        # Configurar el comportamiento del mock del cliente de Text Analytics
        mock_instance = mock_text_analytics_client.return_value

        mock_instance.analyze_sentiment.return_value = [
          AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1})
        ]

        # print(mock_instance.analyze_sentiment.return_value[0].confidence_scores['positive'])

        analyzer = AzureTextAnalyzer()

        # Llamar al método analyze_sentiment
        positive, neutral, negative = analyzer.analyze_sentiment('Sample text')

        # Verificar que el método del cliente de Text Analytics se llamó correctamente
        mock_instance.analyze_sentiment.assert_called_once_with(['Sample text'], language='es')

        # Verificar los resultados
        self.assertEqual(positive, 0.8)
        self.assertEqual(neutral, 0.1)
        self.assertEqual(negative, 0.1)
        
    def test_split_into_blocks(self):
        # Probar la función split_into_blocks
        strings = ['1', '2', '3', '4', '5', '6']
        blocks = split_into_blocks(strings, 2)
        expected_blocks = [['1', '2'], ['3', '4'], ['5', '6']]
        self.assertEqual(blocks, expected_blocks)
        
    @patch('services.text_analyzer.azure_text_analyzer.split_into_blocks')
    @patch('services.text_analyzer.azure_text_analyzer.TextAnalyticsClient')
    def test_analyze_sentiment_by_block(self, mock_text_analytics_client, mock_split_into_blocks):
        # Configurar el comportamiento del mock del cliente de Text Analytics
        mock_instance = mock_text_analytics_client.return_value
        mock_instance.analyze_sentiment.side_effect = [
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            AnalyzeSentimentResult(confidence_scores={'positive': 0.8, 'neutral': 0.1, 'negative': 0.1}),
            # ... asegúrate de que haya suficientes objetos AnalyzeSentimentResult para cubrir las llamadas
        ]

        # Configurar el comportamiento del mock de split_into_blocks
        mock_split_into_blocks.return_value = [
            ['text1', 'text2', 'text3', 'text4', 'text5', 'text6', 'text7', 'text8', 'text9', 'text10'],
            ['text11', 'text12', 'text13', 'text14', 'text15']
        ]

        # Crear una instancia del analizador de texto de Azure
        analyzer = AzureTextAnalyzer()

        # Llamar al método analyze_sentiment_by_block
        result = analyzer.analyze_sentiment_by_block(['text1', 'text2', 'text3', 'text4', 'text5', 'text6',
                                                      'text7', 'text8', 'text9', 'text10', 'text11', 'text12',
                                                      'text13', 'text14', 'text15'])

        # Verificar que el método del cliente de Text Analytics se llamó correctamente
        mock_instance.analyze_sentiment.assert_has_calls([
            call(['text1', 'text2', 'text3', 'text4', 'text5', 'text6', 'text7', 'text8', 'text9', 'text10'], language='es'),
            call(['text11', 'text12', 'text13', 'text14', 'text15'], language='es')
        ])

        # Verificar los resultados
        expected_results = [(0.8, 0.1, 0.1) for _ in range(15)]  # Lista de tuplas con los resultados esperados
        self.assertEqual(result, expected_results)
