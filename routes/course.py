from typing import List, Annotated

from fastapi import APIRouter
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse

from models.course import Course, CourseAvailability
from schemas.schedule import CoursesRequest

from services.course import CourseService
from services.teacher import TeacherService
from services.scraper import BS4WebScraper
from services.text_analyzer.text_analyzer import TextAnalyzer
from services.text_analyzer.azure_text_analyzer import AzureTextAnalyzer

router = APIRouter()

@router.post(
    '/courses/',
    summary='Subir horarios de clases',
    description='Sube diferentes horarios de clases mediante un archivo html del SAES para proveer de cursos la aplicación.'
)
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

@router.post(
  '/courses/occupancy',
  summary='Actualiza la disponibilidad de los cursos',
  description='Actualiza la disponibilidad de los cursos mediante un archivo html del SAES.'
)
async def upload_schedule_occupancy(
  file: Annotated[
    UploadFile,
    File(
      title="Ocupabilidad de horarios",
      description="Documento .html de la ocupabilidad de horarios (se puede encontrar en la sección 'Ocupabilidad horario' en la pestaña 'Académia'.)"
    )
  ]
):
  teacher_evaluator: TextAnalyzer = AzureTextAnalyzer()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(teacher_evaluator))
  course_service = CourseService(router.courses, teacher_service)
  
  availabilities: List[CourseAvailability] = course_service.parse_availabilities(await file.read())
  course_service.update_course_availability(availabilities=availabilities)
  return availabilities
  

@router.get(
  '/courses/',
  summary='Obtener cursos',
  response_description="Una lista de cursos se encuentran dentro de los parámetros dados.",
  description='Obten una lista de cursos que cumplan con los parámetros dados.'
)
def get_courses(request: CoursesRequest) -> List[Course]:
  teacher_evaluator: TextAnalyzer = AzureTextAnalyzer()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(teacher_evaluator))
  course_service = CourseService(router.courses, teacher_service)
  
  filtered_courses = course_service.get_courses(request.career, request.levels, request.semesters, request.shifts)
  
  return filtered_courses
  