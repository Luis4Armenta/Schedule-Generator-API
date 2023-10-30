from abc import ABC, abstractclassmethod
from typing import List
from comments.domain.comment import Teacher, ScrapedComment

class WebScraper(ABC):
  
  @abstractclassmethod
  def scrape_comments(self, teacher: Teacher) -> List[ScrapedComment]:
    pass