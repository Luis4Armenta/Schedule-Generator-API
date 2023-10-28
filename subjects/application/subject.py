from typing import Optional, List

from subjects.domain.model.subject import Subject
from subjects.domain.ports.subjects_repository import SubjectRepository

class SubjectService:
  def __init__(self, subject_repository: SubjectRepository):
    self.subject_repository = subject_repository
  
  def upload_subjects(self, subjects: List[Subject]) -> None:
    for subject in subjects:
      self.subject_repository.add_subject(subject.dict())
      
  def get_subject(self, career: str, name: str) -> Optional[Subject]:
    return self.subject_repository.get_subject(career, name)