from typing import Annotated

from fastapi import Query
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from models.teacher import Teacher

from services.scraper import BS4WebScraper
from services.teacher import TeacherService
from services.text_analyzer.text_analyzer import TextAnalyzer
from services.text_analyzer.azure_text_analyzer import AzureTextAnalyzer

router = APIRouter()

@router.get(
  '/teachers/',
  summary='Obtener profesor',
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
  teacher_evaluator: TextAnalyzer = AzureTextAnalyzer()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(teacher_evaluator))
  teacher = teacher_service.get_teacher(teacher_name)

  if teacher:
    return JSONResponse(content=jsonable_encoder(teacher), status_code=202)
  else:
    return JSONResponse(content={"message": "Teacher not found..."}, status_code=404)
