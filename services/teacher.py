from repositories.teachers_repository import TeacherRepository
from typing import Optional, List
from models.teacher import Teacher
from services.scraper import WebScraper
import functools

class TeacherService:
  def __init__(self, repository: TeacherRepository, web_scraper: WebScraper):
    self.repository = repository
    self.webscraper = web_scraper
  
  @functools.lru_cache(maxsize=None)
  def get_teacher(self, name: str) -> Optional[Teacher]:
    name = name.strip().upper()
    
    if name == 'SIN ASIGNAR':
      return Teacher(
        id=None,
        name='SIN ASIGNAR',
        comments=[],
        subjects=[],
        polarity=0.5,
        url='https://foroupiicsa.net/diccionario/'
      )
    
    teacher = self.repository.get_teacher(name)
    
    if teacher:
      return teacher
    else:
      scraped_teacher = self.webscraper.find_teacher(name)
      
      if scraped_teacher:
        self.repository.add_teacher(scraped_teacher)
        
        return self.repository.get_teacher(name)
      else: 
        return None
      
