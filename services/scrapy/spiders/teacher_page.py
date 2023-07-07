import re
from statistics import mean
from models.teacher import Comment
from scrapy import Spider
from typing import List
from services.translator import Translator, GoogleTranslator
from services.polarity_evaluator import PolarityEvaluator, TextBlobEvaluator
from services.scrapy.items import TeacherItem

class TeacherPageSpider(Spider):
  name = 'teacher_page'
  
  def __init__(self, teacher_name=None, callback=None, *args, **kwargs):
    super(TeacherPageSpider, self).__init__(*args, **kwargs)
    self.start_urls = [f'https://foroupiicsa.net/diccionario/{self._parse_name(teacher_name)}']
    self.teacher_name = teacher_name
    self.callback = callback
    
    translator: Translator = GoogleTranslator()
    self.polarity_evaluator: PolarityEvaluator = TextBlobEvaluator(translator)
    
  def parse(self, response):
    name: str = response.xpath('//p[@class="encontrados"]/span[@class="txbuscado"]/text()').get()
    
    if not name:
      self.callback(None)
      return;
    
    polarities: List[float] = []
       
    if name:
      subjs: List[str] = response.xpath('//div[@class="row text-center top25 comentariosbox"]//h5/text()').getall()
      subjs = [subj.strip() for subj in subjs]
      subjs = list(set(subjs))
      subjects: List[str] = subjs
      
      comments: List[Comment] = []
      
      raw_comments = response.xpath('//div[@class="row text-center top25 comentariosbox"]/div[@class="panel1"]')
      for raw_comment in raw_comments:
        text: str = raw_comment.xpath('.//p[@class="comentariotx"]/text()').get().strip()
        likes: int = int(raw_comment.xpath('.//div[@class="col-md-3 text-right"]/button[@class="btn btn-default btn-comentario btn-ok tipo_enlace"]/span/text()').get().strip())
        dislikes: int = int(raw_comment.xpath('.//div[@class="col-md-3 text-right"]/button[@class="btn btn-default btn-comentario btn-nop"]/span/text()').get().strip())
        date: str = raw_comment.xpath('.//div[@class="date-comment col-md-6 text-left"]/i/text()').get().strip()
        polarity: float = self.polarity_evaluator.get_polarity(text)
        
        polarities.append((polarity+1)/2)
        
        comment: Comment = {
          'text': text,
          'date': date,
          'likes': likes,
          'dislikes': dislikes,
          'polarity': polarity
        }

        comments.append(comment)
      
      
      teacher: TeacherItem = TeacherItem()
      teacher['name'] = name
      teacher['url'] = response.url
      teacher['subjects'] = subjects
      teacher['comments'] = comments
      teacher['polarity'] = mean(polarities)
      
      self.callback(teacher)
      return
      
  def _parse_name(self, name: str) -> str:
    name_without_especial_characters = re.sub(r'[^a-zA-ZñÑáéíóúÁÉÍÓÚ\s]', '', name.strip())
    name_without_spaces = name_without_especial_characters.replace(' ', '+')
    
    return name_without_spaces