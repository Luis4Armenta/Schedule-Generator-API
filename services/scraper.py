import bs4
import requests
from abc import ABC
from lxml import etree
from statistics import mean
from typing import Optional
from requests import Response
from typing import Optional, List
from models.teacher import Teacher, Comment
from services.evaluator.evaluator import PolarityEvaluator

class WebScraper(ABC):
  def find_teacher(self, name: str) -> Optional[Teacher]:
    pass

# name: '//h5//span/text()'
# subjects: '//span[@class="bluetx negritas"]/text()'
# raw_comments: '//div[@class="p-4 box-profe bordeiz"]'
  # text: './/p[@class="comentario"]/text()'
  # date: './/p[@class="fecha"]/text()'
  # likes: './/a[@rel="like"]//span/text()'
  # dislikes: './/a[@rel="nolike"]//span/text()' 

class BS4WebScraper(WebScraper):
  def __init__(self, polarity_evaluator: PolarityEvaluator):
    self.polarity_evaluator = polarity_evaluator
  
  def find_teacher(self, name: str) -> Optional[Teacher]:
    if name == 'SIN ASIGNAR':
      return Teacher(
        id=None,
        name='SIN ASIGNAR',
        comments=[],
        subjects=[],
        polarity=0.5,
        url='https://foroupiicsa.net/diccionario/'
      )
    
    url = self._get_url_for_teacher(name.upper())
    response: Response = requests.get(url)
    response.raise_for_status()

    if response.status_code == 200:
      soup = bs4.BeautifulSoup(response.content, 'html.parser')
      dom = etree.HTML(str(soup))
      
      name = dom.xpath('//h5//span/text()')[0].upper()
      
      subjs: List[str] = dom.xpath('//span[@class="bluetx negritas"]/text()')
      subjs = [subj.strip().upper() for subj in subjs]
      subjs = list(set(subjs))
      subjects: List[str] = subjs
      
      if len(subjects) == 0:
        return None


      polarities: List[float] = []
      comments: List[Comment] = []
      
      
      raw_comments = dom.xpath('//div[@class="p-4 box-profe bordeiz"]')
      
      for raw_comment in raw_comments:
        text: str = raw_comment.xpath('.//p[@class="comentario"]/text()')[0]
        likes: int = int(raw_comment.xpath('.//a[@rel="like"]//span/text()')[0])
        dislikes: int = int(raw_comment.xpath('.//a[@rel="nolike"]//span/text()')[0])
        date: str = raw_comment.xpath('.//p[@class="fecha"]/text()')[0]
        polarity: float = self.polarity_evaluator.get_polarity(text)
        
        polarities.append((polarity+1)/2)
        
        comment: Comment = {
          'text': text,
          'likes': likes,
          'dislikes': dislikes,
          'date': date,
          'polarity': polarity
        }
        
        comments.append(comment)
        
      
      teacher: Teacher = Teacher(
        _id=None,
        name=name,
        url=url,
        subjects=subjects,
        comments=comments,
        polarity=mean(polarities)
      )
      
      return teacher
    else:
      return None
    

  def _get_url_for_teacher(self, teacher: str) -> str:
    parsed_name: str = teacher.replace(' ', '+')
    
    url = f'https://foroupiicsa.net/diccionario/buscar/{parsed_name}'
    return url
