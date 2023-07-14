import time
from fastapi import APIRouter

from services.scraper import BS4WebScraper
from services.courses import CoursesService
from services.teacher import TeacherService
from services.schedule import SchedulesService
from schemas.schedule import ScheduleGeneratorRequest
from services.evaluator.azure_evaluator import AzureEvaluator

router = APIRouter()

@router.get('/schedules/', tags=['Schedules'])
async   def generate_schedules(request: ScheduleGeneratorRequest):
  start = time.time()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(AzureEvaluator()))
  courses_service = CoursesService(router.courses, teacher_service)
  schedules_service = SchedulesService(teacher_service)

  courses = courses_service.get_courses(
      request.career,
      request.levels,
      request.semesters,
      request.shifts
    )
  
  print(f'Número de cursos sin filtrar: {len(courses)}')
  courses = courses_service.filter_coruses(
      courses,
      request.start_time,
      request.end_time,
      request.unwanted_teachers
    )
  print(f'Número de cursos después de filtrar {len(courses)}')
  
  print('Geneerado horarios...')
  schedules = schedules_service.generate_schedules(courses, request.length)
  
  print('Ordenadno horarios...')
  schedules = sorted(schedules, key=lambda x: x.popularity, reverse=True)
  print(f'Número de horarios generados: {len(schedules)}')
  
  end = time.time()
  print("Time Taken: {:.6f}s".format(end-start))

  return schedules[:10]