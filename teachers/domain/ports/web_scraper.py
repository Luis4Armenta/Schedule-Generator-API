from abc import ABC
from typing import Optional
from teachers.domain.model.teacher import Teacher

class WebScraper(ABC):
  def find_teacher(self, name: str) -> Optional[Teacher]:
    pass