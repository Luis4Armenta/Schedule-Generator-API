import time
from fastapi import APIRouter

from typing import List
from models.schedule import Schedule
from services.scraper import BS4WebScraper
from services.courses import CoursesService
from services.teacher import TeacherService
from services.schedule import SchedulesService
from schemas.schedule import ScheduleGeneratorRequest
from services.evaluator.azure_evaluator import AzureEvaluator
from models.course import Course

router = APIRouter()

@router.get('/schedules/', tags=['Schedules'])
async   def generate_schedules(request: ScheduleGeneratorRequest):
  start = time.time()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(AzureEvaluator()))
  courses_service = CoursesService(router.courses, teacher_service)
  schedules_service = SchedulesService(teacher_service)

  courses: List[Course] = courses_service.get_courses(
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
        courses = courses + courses_service.get_courses_by_subject(
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
        courses = courses + courses_service.get_courses_by_subject(
          subject=extra_subject,
          level=extra_subject_level,
          career=extra_subject_career,
          shifts=[extra_subject_shift],
          semester=extra_subject_semester,
        )
  
  print(f'Número de cursos sin filtrar: {len(courses)}')
  courses = courses_service.filter_coruses(
      courses,
      request.start_time,
      request.end_time,
      request.excluded_teachers,
      request.excluded_subjects
    )
  print(f'Número de cursos después de filtrar {len(courses)}')
  
  print('Geneerado horarios...')
  schedules = schedules_service.generate_schedules(
      courses=courses,
      n = request.length,
      required_subjects=[required_subject[1] for required_subject in request.required_subjects]
    )
  
  print('Ordenadno horarios...')
  schedules = sorted(schedules, key=lambda x: x.popularity, reverse=True)
  print(f'Número de horarios generados: {len(schedules)}')
  
  end = time.time()
  print("Time Taken: {:.6f}s".format(end-start))

  return schedules[:20]