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
        
        teacher: Optional[Teacher] = self.find_teacher(teacher_name)
        
        if teacher:
          return teacher
        else:
          return None
          
  def find_teacher(self, teacher_name: str) -> Optional[Teacher]:
    # Search comments about him
    comments: List[Comment] = self.comment_service.seach_comments(teacher_name)
    more_comments: List[Comment] = []
    
    other_name: str = ""
    name_parts = teacher_name.split()
    if len(name_parts) == 3:
        # Reorganizar el nombre si tiene 3 partes
        other_name = name_parts[2] + " " + name_parts[0] + " " + name_parts[1]
    elif len(name_parts) == 4:
        # Reorganizar el nombre si tiene 4 partes
        other_name = " ".join(name_parts[-2:] + name_parts[:-2])
    else:
        other_name = ""
    
    if other_name != "":
      more_comments = self.comment_service.seach_comments(other_name)
      comments = comments + more_comments
    
    
    # if there are comments
    if len(comments) > 0:
      # build teacher entity
      positive_scores: List[float] = [c.positive_score for c in comments]
      positive_score = get_positive_score(positive_scores)
      teacher_url = get_url_for_teacher(teacher_name)

      teacher: Teacher = Teacher(
        name=teacher_name,
        comments=comments,
        url=teacher_url,
        positive_score=positive_score
      )
      
      # save the teacher
      self.add_teacher(teacher)
      return self.teacher_repository.get_teacher(teacher_name)
    else:
      teacher_url = get_url_for_teacher(teacher_name)
      return Teacher(
        name=teacher_name,
        comments=[],
        positive_score=0.5,
        url=teacher_url
      )
      
      
#   def find_teacher(self, teacher_name: str) -> Optional[Teacher]:
#     # Search comments about him
#     comments: List[Comment] = self.comment_service.seach_comments(teacher_name)
#     
#     # if there are comments
#     if len(comments) > 0:
#       # build teacher entity
#       positive_scores: List[float] = [c.positive_score for c in comments]
#       positive_score = get_positive_score(positive_scores)
#       teacher_url = get_url_for_teacher(teacher_name)
# 
#       teacher: Teacher = Teacher(
#         name=teacher_name,
#         comments=comments,
#         url=teacher_url,
#         positive_score=positive_score
#       )
#       
#       # save the teacher
#       self.add_teacher(teacher)
#       return self.teacher_repository.get_teacher(teacher_name)
#     else:
#       teacher_url = get_url_for_teacher(teacher_name)
#       return Teacher(
#         name=teacher_name,
#         comments=[],
#         positive_score=0.5,
#         url=teacher_url
#       )
      
  def add_teacher(self, new_teacher: Teacher) -> None:
    teacher = self.teacher_repository.get_teacher(new_teacher.name)
    if teacher is None:
      self.teacher_repository.add_teacher(new_teacher)
    