from requests import Response
from typing import Optional, List, Tuple

import bs4
import requests
from lxml import etree

from teachers.domain.model.teacher import Teacher, Comment
from teachers.domain.ports.web_scraper import WebScraper
from teachers.infrastructure.text_analyzer.text_analyzer import TextAnalyzer

from utils.text import get_url_for_teacher
from utils.metrics import get_positive_score

class BS4WebScraper(WebScraper):
  def __init__(self, text_analyzer: TextAnalyzer):
    self.text_analyzer = text_analyzer
  
  def find_teacher(self, name: str) -> Optional[Teacher]:
    if name == 'SIN ASIGNAR':
      return Teacher(
        id=None,
        name='SIN ASIGNAR',
        comments=[],
        subjects=[],
        positive_score=0.5,
        url='https://foroupiicsa.net/diccionario/'
      )
    
    url = get_url_for_teacher(name.upper())
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


      positive_scores: List[float] = []
      comments: List[Comment] = []
      
      
      raw_comments = dom.xpath('//div[@class="p-4 box-profe bordeiz"]')
      
      texts: List[str] = dom.xpath('//p[@class="comentario"]/text()') 
      scores: List[Tuple[float, float, float]] = self.text_analyzer.analyze_sentiment_by_block(texts)
      
      for raw_comment, score in zip(raw_comments, scores):
        subject: str = raw_comment.xpath('.//span[@class="bluetx negritas"]/text()')[0]
        text: str = raw_comment.xpath('.//p[@class="comentario"]/text()')[0]
        likes: int = int(raw_comment.xpath('.//a[@rel="like"]//span/text()')[0])
        dislikes: int = int(raw_comment.xpath('.//a[@rel="nolike"]//span/text()')[0])
        date: str = raw_comment.xpath('.//p[@class="fecha"]/text()')[0]

        neutral_score_rate = 0.85
        positive_scores.append(score[0] + (score[1] * neutral_score_rate))
        
        comment: Comment = {
          'subject': subject,
          'text': text,
          'likes': likes,
          'dislikes': dislikes,
          'date': date,
          'positive_score': score[0],
          'neutral_score': score[1],
          'negative_score': score[2],
        }
        
        comments.append(comment)
        
      
      teacher: Teacher = Teacher(
        _id=None,
        name=name,
        url=url,
        subjects=subjects,
        comments=comments,
        positive_score=get_positive_score(positive_scores)
      )
      
      return teacher
    else:
      return None


