from typing import List
from comments.domain.comments_web_scraper import CommentsWebScraper
from comments.domain.text_analyzer import TextAnalyzer

from comments.domain.comment import Comment

class CommentService:
  def __init__(
    self,
    web_scraper: CommentsWebScraper,
    text_analyzer: TextAnalyzer
  ):
    self.web_scraper = web_scraper
    self.text_analyzer = text_analyzer
  
  def seach_comments(self, teacher_name: str) -> List[Comment]:
    scraped_comments: List[Comment] = self.web_scraper.scrape_comments(teacher_name)
    
    if len(scraped_comments) == 0:
      return []
    
    comment_texts: List[str] = [comment.text for comment in scraped_comments]
    sentiments = self.text_analyzer.analyze_sentiment_by_block(comment_texts)
    
    comments: List[Comment] = []
    for scraped_comment, analisis in zip(scraped_comments, sentiments):
      scraped_comment.positive_score = analisis.positive_score
      scraped_comment.neutral_score = analisis.neutral_score
      scraped_comment.negative_score = analisis.negative_score
      
      comments.append(scraped_comment)
    return comments
