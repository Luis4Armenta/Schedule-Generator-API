from abc import ABC, abstractclassmethod
from typing import List, TypedDict
from comments.domain.comment import Comment

class PageCommentIdentifiers(TypedDict):
  comment: str
  comment_subject: str
  comment_text: str
  comment_dislikes: str
  comment_likes: str
  comment_date: str

class CommentsWebSource:
  def __init__(
    self,
    name: str,
    url: str,
    identifiers: PageCommentIdentifiers
  ):
    self.name = name
    self.url = url
    self.identifiers: PageCommentIdentifiers = identifiers

class CommentsWebScraper(ABC):
  
  @abstractclassmethod
  def scrape_comments(self, teacher: str) -> List[Comment]:
    pass