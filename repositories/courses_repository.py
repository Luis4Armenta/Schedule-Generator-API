from typing import List
from abc import ABC, abstractmethod
from models.course import Course

class CourseRepository(ABC):
  @abstractmethod
  def connect(self, options) -> None:
    pass
    
  @abstractmethod
  def get_courses(self, query: dict) -> List[Course]:
    pass
  
  # @abstractmethod
  # def add_course(self, course: Course) -> None:
  #   pass
  
  @abstractmethod
  def add_course_if_not_exist(self, course: Course) -> None:
    pass
  
  @abstractmethod
  def disconnect(self) -> None:
    pass

