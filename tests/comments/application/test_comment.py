import unittest
from unittest.mock import Mock
from comments.domain.comments_web_scraper import CommentsWebScraper
from comments.domain.text_analyzer import TextAnalyzer
from comments.domain.comment import Comment
from comments.application.comment import CommentService  # Asegúrate de importar correctamente tu módulo


class TestCommentService(unittest.TestCase):
  def setUp(self) -> None:
    # Configura objetos mock para el web scraper y el text analyzer
    self.web_scraper_mock = Mock(spec=CommentsWebScraper)
    self.text_analyzer_mock = Mock(spec=TextAnalyzer)
    self.comment_service = CommentService(
        web_scraper=self.web_scraper_mock,
        text_analyzer=self.text_analyzer_mock
    )
    
  def test_search_comments_with_scraped_comments(self):
    # Configura el mock del web scraper para devolver comentarios simulados
    simulated_comments = [Comment(
      teacher='JOSE JUAN TENORIO',
      date='12-11-2022',
      dislikes=0,
      likes=0,
      subject='Programación Orientada a Objetos',
      text='Es un buen profesor. ;)'
    ),
    Comment(
      teacher='JOSE LUIS TABOADA',
      date='12-11-2022',
      dislikes=0,
      likes=0,
      subject='Estructuras de datos',
      text='Es un mal profesor. :('
    )]
    self.web_scraper_mock.scrape_comments.return_value = simulated_comments

    # Configura el mock del text analyzer para devolver análisis simulados
    simulated_analysis_1 = Mock(positive_score=0.8, neutral_score=0.1, negative_score=0.1)
    simulated_analysis_2 = Mock(positive_score=0.0, neutral_score=0.2, negative_score=0.8)
    self.text_analyzer_mock.analyze_sentiment_by_block.return_value = [simulated_analysis_1, simulated_analysis_2]

    # Llama al método search_comments con el nombre de un profesor
    result_comments = self.comment_service.seach_comments('JOSE JUAN TENORIO')

    # Verifica que el resultado sea una lista de comentarios con los valores esperados
    self.assertEqual(result_comments, simulated_comments)
    self.assertEqual(result_comments[0].positive_score, simulated_analysis_1.positive_score)
    self.assertEqual(result_comments[1].positive_score, simulated_analysis_2.positive_score)
    # Puedes agregar más verificaciones según sea necesario
    
  def test_search_comments_with_no_scraped_comments(self):
    # Configura el mock del web scraper para devolver una lista vacía
    self.web_scraper_mock.scrape_comments.return_value = []

    # Llama al método search_comments con el nombre de un profesor
    result_comments = self.comment_service.seach_comments('Teacher with no comments')

    # Verifica que el resultado sea una lista vacía
    self.assertEqual(result_comments, [])