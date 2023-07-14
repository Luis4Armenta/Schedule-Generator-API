import re
from typing import Optional
from functools import cache
from unidecode import unidecode
from models.teacher import Teacher
from services.scraper import WebScraper
from repositories.teachers_repository import TeacherRepository
      


class TeacherService:
  def __init__(self, repository: TeacherRepository, web_scraper: WebScraper):
    self.repository = repository
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

def clean_name(name: str) -> str:
    # Convertir caracteres especiales a su equivalente sin acentos
    cleaned_name = unidecode(name)
    # Eliminar caracteres no alfabéticos y convertir a mayúsculas
    cleaned_name = re.sub(r'[^a-zA-Z\s]', '', cleaned_name).upper()
    # Eliminar espacios innecesarios
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name)
    # Eliminar espacios al inicio y al final de la cadena
    cleaned_name = cleaned_name.strip()
    return cleaned_name