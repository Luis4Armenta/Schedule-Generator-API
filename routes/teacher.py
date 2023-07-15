from fastapi import Query
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from services.scraper import BS4WebScraper
from services.teacher import TeacherService
from services.evaluator.evaluator import TeacherEvaluator
from services.evaluator.azure_evaluator import AzureEvaluator

router = APIRouter()

@router.get('/teachers/', tags=['Teachers'])
def get_teacher_by_name(teacher_name: str = Query(min_length=5)):
  teacher_evaluator: TeacherEvaluator = AzureEvaluator()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(teacher_evaluator))
  teacher = teacher_service.get_teacher(teacher_name)

  if teacher:
    return JSONResponse(content=jsonable_encoder(teacher), status_code=202)
  else:
    return JSONResponse(content={"message": "Teacher not found..."}, status_code=404)
