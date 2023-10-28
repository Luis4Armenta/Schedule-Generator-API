from typing import Optional
from functools import cache

from models.teacher import Teacher
from repositories.subjects_repository import SubjectRepository
      
from services.scraper import WebScraper
from models.course import Subject

from utils.text import clean_name

from typing import List


class SubjectService:
  def __init__(self, subject_repository: SubjectRepository):
    self.subject_repository = subject_repository
  
  def upload_subjects(self, subjects: List[Subject]) -> None:
    for subject in subjects:
      self.subject_repository.add_subject(subject.dict())