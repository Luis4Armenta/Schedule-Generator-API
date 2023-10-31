from typing import Annotated

from fastapi import Query
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from teachers.domain.model.teacher import Teacher
from teachers.application.teacher import TeacherService

from comments.application.comment import CommentService
from comments.infrastructure.bs4_comments_web_scraper import BS4CommentsWebScraper
from comments.infrastructure.azure_text_analyzer import AzureTextAnalyzer
from comments.domain.text_analyzer import TextAnalyzer
from comments.domain.comments_web_scraper import CommentsWebScraper

router = APIRouter()

@router.get(
  '/teachers/',
  summary='Obtener profesor',
  response_description="Un profesor que coincide con el nombre dado.",
  description='Ve la información disponible de un profesor dando su nombre.'
)
def get_teacher_by_name(
    teacher_name: Annotated[
        str,
        Query(
          min_length=5,
          max_length=50,
          pattern='^[A-Za-zÁ-Úá-ú]+ [A-Za-zÁ-Úá-ú]+ [A-Za-zÁ-Úá-ú]+$',
          title='Nombre del profesor',
          description='Nombre del profesor que se desea buscar.'
          )
      ]
  ) -> Teacher:
  comment_service = CommentService(BS4CommentsWebScraper(), AzureTextAnalyzer())
  teacher_service = TeacherService(router.teachers, comment_service)
  
  teacher = teacher_service.get_teacher(teacher_name)

  if teacher:
    return JSONResponse(content=jsonable_encoder(teacher), status_code=202)
  else:
    return JSONResponse(content={"message": "Teacher not found..."}, status_code=404)
