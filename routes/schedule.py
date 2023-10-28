import time
from typing import List

from fastapi import APIRouter

from models.course import Course
from models.schedule import Schedule
from schemas.schedule import ScheduleGeneratorRequest

from services.scraper import BS4WebScraper
from services.course import CourseService
from services.teacher import TeacherService
from services.schedule import ScheduleService
from services.text_analyzer.azure_text_analyzer import AzureTextAnalyzer
from services.subject import SubjectService
from repositories.subjects_repository import SubjectRepository
from repositories.mongo_subjects_repository import MongoSubjectsRepository

router = APIRouter()

@router.get(
  '/schedules/',
  summary='Generar horarios',
  response_description="Una lista ordenada de 20 horarios generados de mejor puntuados a peor puntuados."
)
async def generate_schedules(request: ScheduleGeneratorRequest) -> List[Schedule]:
  '''
  Apartir de los parámetros dados genera una colección de horarios que cumplan con ellos.
  
  - **career**: letra asignada a la carrera para la que se generara el horario.
  - **levels**: niveles de los cursos que se tendrán en cuenta para formar los horarios.
  - **semesters**: semestres que se tendrán en cuenta para formar los horarios.
  - **start_time**: hora apartir de la que iniciaran los horarios.
  - **end_time**: hora máxima a la que finalizarán los horarios.
  - **shifts**: turnos que podrán integrar los horarios.
  - **length**: número de asignaturas con las que cumplicara cada horario.
  - **excluded_teachers**: profesores que serán excluidos de los horarios generados.
  - **excluded_subjects**: nombres de asignaturas que serán excluidas de los horarios generados.
  - **required_subjects**: asginaturas que tienen que aparecen el los horarios obligatoriamente.
  - **extra_subjects**: asignaturas opcionales que amplian el conjunto de asignaturas posibles en un horario.
  '''
  start = time.time()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(AzureTextAnalyzer()))
  subject_service = SubjectService(router.subjects)
  course_service = CourseService(router.courses, teacher_service, subject_service)
  schedule_service = ScheduleService(teacher_service)

  courses: List[Course] = course_service.get_courses(
      request.career,
      request.levels,
      request.semesters,
      request.shifts
    )
   
  for required_subject in request.required_subjects:
    required_subject_sequence = required_subject[0]
    required_subject = required_subject[1]
    
    
    required_subject_level = required_subject_sequence[0]
    required_subject_shift = required_subject_sequence[2]
    required_subject_semester = required_subject_sequence[3]
    
    if (
        not any(required_subject_level == level for level in request.levels) or
        not any(required_subject_shift == shift for shift in request.shifts) or
        not any(required_subject_semester == semester for semester in request.semesters)
      ):
        courses = courses + course_service.get_courses_by_subject(
          sequence=required_subject_sequence,
          subject=required_subject,
          shifts=[required_subject_shift]
        )
    
  for extra_subject in request.extra_subjects:
    extra_subject_sequence = extra_subject[0]
    extra_subject = extra_subject[1]
    
    
    extra_subject_level = extra_subject_sequence[0]
    extra_subject_shift = extra_subject_sequence[2]
    extra_subject_semester = extra_subject_sequence[3]
    extra_subject_career = extra_subject_sequence[1]
    
    if (
        not any(extra_subject_level == level for level in request.levels) or
        not any(extra_subject_shift == shift for shift in request.shifts) or
        not any(extra_subject_semester == semester for semester in request.semesters)
      ):
        courses = courses + course_service.get_courses_by_subject(
          sequence=extra_subject_sequence,
          subject=extra_subject,
          shifts=[required_subject_shift]
        )
  
  print(f'Número de cursos sin filtrar: {len(courses)}')
  courses = course_service.filter_coruses(
      courses=courses,
      start_time=request.start_time,
      end_time=request.end_time,
      excluded_teachers=request.excluded_teachers,
      excluded_subjects=request.excluded_subjects,
      min_course_availability=request.available_uses
    )
  print(f'Número de cursos después de filtrar {len(courses)}')
  
  print('Geneerado horarios...')
  schedules = schedule_service.generate_schedules(
      courses=courses,
      n = request.length,
      credits=request.credits,
      required_subjects=[required_subject[1] for required_subject in request.required_subjects]
    )
  
  print('Ordenadno horarios...')
  schedules = sorted(schedules, key=lambda x: x.popularity, reverse=True)
  print(f'Número de horarios generados: {len(schedules)}')
  
  end = time.time()
  print("Time Taken: {:.6f}s".format(end-start))

  return schedules[:20]