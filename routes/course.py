from typing import List, Annotated

from fastapi import APIRouter
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse

from courses.domain.model.course import Course, CourseAvailability
from schemas.schedule import CoursesRequest

from courses.application.course import CourseService
from teachers.application.teacher import TeacherService
from saes.application.saes import SaesService

from comments.infrastructure.azure_text_analyzer import AzureTextAnalyzer
from comments.infrastructure.bs4_comments_web_scraper import BS4CommentsWebScraper
from comments.application.comment import CommentService

from subjects.application.subject import SubjectService


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
  comment_service = CommentService(BS4CommentsWebScraper(), AzureTextAnalyzer())
  teacher_service = TeacherService(router.teachers, comment_service)
  subject_service = SubjectService(router.subjects)

  course_service = CourseService(router.courses, teacher_service, subject_service)
  saes_service = SaesService()
  
  courses: List[Course] = saes_service.get_courses(await file.read())
  course_service.upload_courses(courses)
  
  return JSONResponse(content={"message": "Schedules uploaded!"}, status_code=202)

@router.post(
  '/courses/occupancy',
  summary='Actualiza la disponibilidad de los cursos',
  description='Actualiza la disponibilidad de los cursos mediante un archivo html del SAES.'
)
async def upload_schedule_availability(
  file: Annotated[
    UploadFile,
    File(
      title="Ocupabilidad de horarios",
      description="Documento .html de la ocupabilidad de horarios (se puede encontrar en la sección 'Ocupabilidad horario' en la pestaña 'Académia'.)"
    )
  ]
):
  comment_service = CommentService(BS4CommentsWebScraper(), AzureTextAnalyzer())
  teacher_service = TeacherService(router.teachers, comment_service)
  subject_service = SubjectService(router.subjects)
  
  
  course_service = CourseService(router.courses, teacher_service, subject_service)
  saes_service = SaesService()
  
  availabilities: List[CourseAvailability] = saes_service.get_course_availability(await file.read())
  course_service.update_course_availability(availabilities=availabilities)
  return availabilities
  

@router.get(
  '/courses/',
  summary='Obtener cursos',
  response_description="Una lista de cursos se encuentran dentro de los parámetros dados.",
  description='Obten una lista de cursos que cumplan con los parámetros dados.'
)
def get_courses(request: CoursesRequest) -> List[Course]:
  comment_service = CommentService(BS4CommentsWebScraper(), AzureTextAnalyzer())
  teacher_service = TeacherService(router.teachers, comment_service)
  subject_service = SubjectService(router.subjects)

  course_service = CourseService(router.courses, teacher_service, subject_service)
  
  filtered_courses = course_service.get_courses(request.career, request.levels, request.semesters)
  
  return filtered_courses

@router.post('/subjects/')
async def upload_subjects(
  file: Annotated[
      UploadFile,
      File(
        title="Asignaturas", 
        description="Documento .html del SAES donde aparecen las asignaturas"
      )
    ]
  ):
  subject_service = SubjectService(router.subjects)
  saes_service = SaesService()
  
  
  subjects = saes_service.get_subjects(await file.read())
  subject_service.upload_subjects(subjects)
  
  return JSONResponse(content={"message": "subjects uploaded!"}, status_code=202)

  