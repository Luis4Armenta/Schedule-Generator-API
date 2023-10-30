from typing import List
from comments.domain.comment import Comment, Teacher, ScrapedComment
# from teachers.infrastructure.text_analyzer.text_analyzer import TextAnalyzer
from comments.domain.web_scraper import WebScraper
from comments.domain.text_analyzer import TextAnalyzer

class CommentService:
  def __init__(
    self,
    web_scraper: WebScraper,
    text_analyzer: TextAnalyzer
  ):
    self.web_scraper = web_scraper
    self.text_analyzer = text_analyzer
  
  def find_comments(self, teacher: Teacher):
    scraped_comments: List[ScrapedComment] = self.web_scraper.scrape_comments(teacher)
    
    if len(scraped_comments) == 0:
      return []
    
    comment_texts: List[str] = [comment.text for comment in scraped_comments]
    sentiments = self.text_analyzer.analyze_sentiment_by_block(comment_texts)
    
    comments: List[Comment] = []
    for scraped_comment, analisis in zip(scraped_comments, sentiments):
      comment = Comment(
          teacher=teacher,
          subject=scraped_comment.subject,
          text=scraped_comment.text,
          likes=scraped_comment.likes,
          dislikes=scraped_comment.dislikes,
          date=scraped_comment.date,
          positive_score=analisis.positive_score,
          neutral_score=analisis.neutral_score,
          negative_score=analisis.negative_score,
        )
      comments.append(
        comment
      )
    return comments
    
    