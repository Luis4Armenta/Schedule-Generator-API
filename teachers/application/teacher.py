from typing import Optional, List
from functools import cache

from teachers.domain.model.teacher import Teacher
from teachers.domain.ports.web_scraper import WebScraper
from teachers.domain.ports.teachers_repository import TeacherRepository
from comments.application.comment import CommentService
from comments.domain.comment import Comment

from utils.text import clean_name, get_url_for_teacher
from utils.metrics import get_positive_score


class TeacherService:
  def __init__(
      self,
      repository: TeacherRepository,
      comment_service: CommentService
    ):
    self.teacher_repository = repository
    self.comment_service = comment_service
  
  @cache
  def get_teacher(self, teacher_name: str) -> Optional[Teacher]:
    teacher_name = clean_name(teacher_name)
    
    
    # If the teacher is Unassigned
    if teacher_name == 'SIN ASIGNAR':
      return Teacher(
        name='SIN ASIGNAR',
        comments=[],
        subjects=[],
        positive_score=0.5,
        url='https://foroupiicsa.net/diccionario/'
      )
    else:
      # else find in the teacher repo
      teacher = self.teacher_repository.get_teacher(teacher_name)
      
      # if teacher was found in the teacher repo
      if teacher is not None:
        return teacher
      else:
        # else teacher was not found in the teacher repo
        
        # Search comments about him
        comments: List[Comment] = self.comment_service.seach_comments(teacher_name)
        
        # if there are comments
        if len(comments) != 0:
          # build teacher entity
          subjects: List[str] = [c.subject for c in comments]
          positive_scores: List[float] = [c.positive_score for c in comments]
          positive_score = get_positive_score(positive_scores)
          teacher_url = get_url_for_teacher(teacher_name)
          teacher: Teacher = Teacher(
            name=teacher_name,
            comments=comments,
            subjects=subjects,
            url=teacher_url,
            positive_score=positive_score
          )
          
          # save the teacher
          self.teacher_repository.add_teacher(teacher)
          
          return self.teacher_repository.get_teacher(teacher_name)
        else:
          teacher_url = get_url_for_teacher(teacher_name)
          return Teacher(
            name=teacher_name,
            subjects=[],
            comments=[],
            positive_score=0.5,
            url=teacher_url
          )
          
