from typing import List
from abc import ABC, abstractmethod

from courses.domain.model.course import Course

class CourseRepository(ABC):
  @abstractmethod
  def connect(self, options) -> None:
    pass
    
  @abstractmethod
  def get_courses(
      self,
      levels: List[str],
      career: str,
      semesters: List[str],
      subjects: List[str] = []
    ) -> List[Course]:
    pass
  
  @abstractmethod
  def update_course_availability(
    self,
    sequence: str,
    subject: str,
    new_course_availability: int
  ) -> None:
    pass
  
  @abstractmethod
  def add_course_if_not_exist(self, course: Course) -> None:
    pass
  
  @abstractmethod
  def disconnect(self) -> None:
    pass

