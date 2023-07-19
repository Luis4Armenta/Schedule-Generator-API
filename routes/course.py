from typing import List, Annotated

from fastapi import APIRouter
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse

from models.course import Course
from schemas.schedule import CoursesRequest

from services.course import CourseService
from services.teacher import TeacherService
from services.scraper import BS4WebScraper
from services.text_analyzer.text_analyzer import TextAnalyzer
from services.text_analyzer.azure_text_analyzer import AzureTextAnalyzer

router = APIRouter()

@router.post('/courses/')
async def upload_schedules(
  file: Annotated[
      UploadFile,
      File(
        title="Horarios de clases", 
        description="Documento .html del horario de clases con los cursos a cargar (Se puede encontrar en la sección 'Horarios de clases' en la pestaña de 'Académia' del SAES)."
      )
    ]
  ):
  teacher_evaluator: TextAnalyzer = AzureTextAnalyzer()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(teacher_evaluator))
  course_service = CourseService(router.courses, teacher_service)
  
  courses: List[Course] = course_service.parse_courses(await file.read())
  course_service.upload_courses(courses)
  
  return JSONResponse(content={"message": "Schedules uploaded!"}, status_code=202)

@router.get('/courses/')
def get_courses(request: CoursesRequest) -> List[Course]:
  teacher_evaluator: TextAnalyzer = AzureTextAnalyzer()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(teacher_evaluator))
  course_service = CourseService(router.courses, teacher_service)
  
  filtered_courses = course_service.get_courses(request.career, request.levels, request.semesters, request.shifts)
  
  return filtered_courses
  