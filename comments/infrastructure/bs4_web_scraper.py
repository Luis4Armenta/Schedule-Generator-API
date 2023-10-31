from requests import Response
from typing import Optional, List, Tuple

import bs4
import requests
from lxml import etree

from comments.domain.comment import Comment
from teachers.domain.model.teacher import Teacher
from comments.domain.web_scraper import WebScraper

from utils.text import get_url_for_teacher

class BS4WebScraper(WebScraper):
  def __init__(self):
    pass
  
  
  def scrape_comments(self, teacher: str) -> List[Comment]:
    if teacher == 'SIN ASIGNAR':
      return Teacher(
        id=None,
        name='SIN ASIGNAR',
        comments=[],
        subjects=[],
        positive_score=0.5,
        url='https://foroupiicsa.net/diccionario/'
      )
    
    url = get_url_for_teacher(teacher.upper())
    response: Response = requests.get(url)
    response.raise_for_status()

    if response.status_code == 200:
      soup = bs4.BeautifulSoup(response.content, 'html.parser')
      dom = etree.HTML(str(soup))
      
      raw_comments = dom.xpath('//div[@class="p-4 box-profe bordeiz"]')
      comments: List[Comment] = []
      
      for raw_comment in raw_comments:
        subject: str = raw_comment.xpath('.//span[@class="bluetx negritas"]/text()')[0]
        text: str = raw_comment.xpath('.//p[@class="comentario"]/text()')[0]
        likes: int = int(raw_comment.xpath('.//a[@rel="like"]//span/text()')[0])
        dislikes: int = int(raw_comment.xpath('.//a[@rel="nolike"]//span/text()')[0])
        date: str = raw_comment.xpath('.//p[@class="fecha"]/text()')[0]

        comment: Comment = Comment(
          teacher=teacher,
          subject= subject,
          text= text,
          likes= likes,
          dislikes= dislikes,
          date= date,
        )
        
        comments.append(comment)

      
      return comments
    else:
      return None


