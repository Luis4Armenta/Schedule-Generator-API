from requests import Response
from typing import List, TypedDict, Optional

import bs4
import requests
from lxml import etree

from comments.domain.comment import Comment
from teachers.domain.model.teacher import Teacher
from comments.domain.comments_web_scraper import CommentsWebScraper
from comments.domain.comments_web_scraper import PageCommentIdentifiers, CommentsWebSource

from utils.text import get_url_for_teacher


class BS4CommentsWebScraper(CommentsWebScraper):
  def __init__(self, source: Optional[CommentsWebSource] = None):
    if source is not None:
      self.source = source
      
    else:
      self.source = CommentsWebSource(
          name='Diccionario de maestros',
          url='https://foroupiicsa.net/diccionario/buscar/',
          identifiers={
            'comment': '//div[@class="p-4 box-profe bordeiz"]',
            'comment_subject': './/span[@class="bluetx negritas"]/text()',
            'comment_text': './/p[@class="comentario"]/text()',
            'comment_likes': './/a[@rel="like"]//span/text()',
            'comment_dislikes': './/a[@rel="nolike"]//span/text()',
            'comment_date': './/p[@class="fecha"]/text()'
          }
        )
    
    self.page_identifiers: PageCommentIdentifiers = self.source.identifiers
    
  def scrape_comments(self, teacher: str) -> List[Comment]:
    url = get_url_for_teacher(teacher.upper())
    response: Response = requests.get(url)
    response.raise_for_status()

    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    dom = etree.HTML(str(soup))
    
    raw_comments = dom.xpath(self.page_identifiers['comment'])
    comments: List[Comment] = []
    
    for raw_comment in raw_comments:
      subject: str = raw_comment.xpath(self.page_identifiers['comment_subject'])[0]
      text: str = raw_comment.xpath(self.page_identifiers['comment_text'])[0]
      likes: int = int(raw_comment.xpath(self.page_identifiers['comment_likes'])[0])
      dislikes: int = int(raw_comment.xpath(self.page_identifiers['comment_dislikes'])[0])
      date: str = raw_comment.xpath(self.page_identifiers['comment_date'])[0]

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


