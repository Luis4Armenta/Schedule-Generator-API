from typing import List
from abc import ABC, abstractmethod

from models.course import Subject

class SubjectRepository(ABC):
  @abstractmethod
  def connect(self, options) -> None:
    pass

  @abstractmethod
  def add_subject(subject: Subject) -> None:
    pass
  
  @abstractmethod
  def disconnect(self) -> None:
    pass
  
  