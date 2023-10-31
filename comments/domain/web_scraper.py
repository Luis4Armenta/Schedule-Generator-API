from abc import ABC, abstractclassmethod
from typing import List
from comments.domain.comment import Comment

class WebScraper(ABC):
  
  @abstractclassmethod
  def scrape_comments(self, teacher: str) -> List[Comment]:
    pass