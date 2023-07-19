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

router = APIRouter()

@router.get(
  '/schedules/',
  summary='Generar horarios',
  description='Apartir de los parámetros dados genera una colección de horarios que cumplan con ellos.',
)
async def generate_schedules(request: ScheduleGeneratorRequest) -> List[Schedule]:
  start = time.time()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(AzureTextAnalyzer()))
  course_service = CourseService(router.courses, teacher_service)
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
          subject=extra_subject,
          level=extra_subject_level,
          career=extra_subject_career,
          shifts=[extra_subject_shift],
          semester=extra_subject_semester,
        )
  
  print(f'Número de cursos sin filtrar: {len(courses)}')
  courses = course_service.filter_coruses(
      courses,
      request.start_time,
      request.end_time,
      request.excluded_teachers,
      request.excluded_subjects
    )
  print(f'Número de cursos después de filtrar {len(courses)}')
  
  print('Geneerado horarios...')
  schedules = schedule_service.generate_schedules(
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