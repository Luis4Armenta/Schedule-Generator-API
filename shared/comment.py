from abc import ABC

class IComment(ABC):
  subject: str
  text: str
  date: str
  likes: int
  dislikes: int