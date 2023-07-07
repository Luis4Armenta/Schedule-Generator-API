from repositories.teachers_repository import TeacherRepository
from typing import Optional, List
from models.teacher import Teacher
from services.scraper import WebScraper

class TeacherService:
  def __init__(self, repository: TeacherRepository, web_scraper: WebScraper):
    self.repository = repository
    self.webscraper = web_scraper
  
  def get_teacher(self, name: str) -> Optional[Teacher]:
    teacher = self.repository.get_teacher(name)
    
    if teacher:
      return teacher
    else:
      scraped_teacher = self.webscraper.find_teacher(name)
      
      if scraped_teacher:
        self.repository.add_teacher(scraped_teacher)
        
        return self.get_teacher(name)
      else: 
        return None
      
