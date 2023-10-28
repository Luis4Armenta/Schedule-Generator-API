from abc import ABC, abstractmethod

from subjects.domain.model.subject import Subject

class SubjectRepository(ABC):
  @abstractmethod
  def connect(self, options) -> None:
    pass

  @abstractmethod
  def add_subject(self, subject: Subject) -> None:
    pass
  
  @abstractmethod
  def get_subject(self, career: str, name: str) -> Subject:
    pass
  
  @abstractmethod
  def disconnect(self) -> None:
    pass
  
  