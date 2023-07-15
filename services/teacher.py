from typing import Optional
from functools import cache

from models.teacher import Teacher
from repositories.teachers_repository import TeacherRepository
      
from services.scraper import WebScraper

from utils.text import clean_name


class TeacherService:
  def __init__(self, repository: TeacherRepository, web_scraper: WebScraper):
    self.teacher_repository = repository
    self.webscraper = web_scraper
  
  @cache
  def get_teacher(self, name: str) -> Optional[Teacher]:
    name = clean_name(name)
    
    if name == 'SIN ASIGNAR':
      return Teacher(
        id=None,
        name='SIN ASIGNAR',
        comments=[],
        subjects=[],
        polarity=0.5,
        url='https://foroupiicsa.net/diccionario/'
      )
    
    teacher = self.teacher_repository.get_teacher(name)
    
    if teacher:
      return teacher
    else:
      scraped_teacher = self.webscraper.find_teacher(name)
      
      if scraped_teacher:
        self.teacher_repository.add_teacher(scraped_teacher)
        
        return self.teacher_repository.get_teacher(name)
      else: 
        return None
