import time
from fastapi import FastAPI, Query, File, UploadFile, Form
from services.courses import CoursesService
from dotenv import dotenv_values
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from repositories.teachers_repository import TeacherRepository
from repositories.mongo_teachers_repository import MongoTeachersRepository
from models.teacher import Teacher
from services.teacher import TeacherService
from services.scraper import BS4WebScraper
from services.evaluator.evaluator import TeacherEvaluator
from services.evaluator.text_blob_evaluator import TextBlobEvaluator
from services.translator import GoogleTranslator, Translator
from services.evaluator.azure_evaluator import AzureEvaluator
from bs4 import BeautifulSoup
from lxml import etree
from models.course import Course, ScheduleCourse, session
from typing import List, Annotated
from services.schedule import SchedulesService
from repositories.courses_repository import CourseRepository
from repositories.mongo_courses_repository import MongoCourseRepository
from schemas.schedule import ScheduleGeneratorRequest

config = dotenv_values('.env')

app = FastAPI()
app.title = 'Profesores-API'
app.version = '0.0.1'

@app.on_event('startup')
def startup_db_clients():
  app.teachers: TeacherRepository = MongoTeachersRepository({
    'host': config['MONGODB_HOST'],
    'port': int(config['MONGODB_PORT']),
    'database': config['MONGODB_DATABASE']
  })
  
  app.teachers.connect()
  
  app.courses: CourseRepository = MongoCourseRepository({
    'host': config['MONGODB_HOST'],
    'port': int(config['MONGODB_PORT']),
    'database': config['MONGODB_DATABASE']
  })
  
  app.courses.connect()
  

@app.get('/', tags=['home'])
def message() -> HTMLResponse:
  return HTMLResponse('<h1>Profesores API</h1>')

@app.get('/teachers/', tags=['Teachers'])
def get_teacher_by_name(teacher_name: str = Query(min_length=5)):
  teacher_evaluator: TeacherEvaluator = AzureEvaluator()
  teacher_service = TeacherService(app.teachers, BS4WebScraper(teacher_evaluator))
  teacher = teacher_service.get_teacher(teacher_name)

  if teacher:
    return JSONResponse(content=jsonable_encoder(teacher), status_code=202)
  else:
    return JSONResponse(content={"message": "Teacher not found..."}, status_code=404)

@app.post('/courses/', tags=['Courses'])
async def upload_schedules(file: UploadFile):
  teacher_evaluator: TeacherEvaluator = AzureEvaluator()
  teacher_service = TeacherService(app.teachers, BS4WebScraper(teacher_evaluator))
  course_service = CoursesService(app.courses, teacher_service)
  
  courses: List[Course] = course_service.parse_courses(await file.read())
  course_service.upload_courses(courses)
  
  return JSONResponse(content={"message": "Schedules uploaded!"}, status_code=202)

@app.get('/courses/', tags=['Courses'])
def get_courses(
    level: str = Query(min_length= 1,max_length=1),
    career: str = Query(min_length=1, max_length=1),
    shift: str = Query(min_length=1, max_length=1, default=None),
    semester: str = Query(min_length=1, max_length=1, default=None),
  ):
  teacher_evaluator: TeacherEvaluator = AzureEvaluator()
  teacher_service = TeacherService(app.teachers, BS4WebScraper(teacher_evaluator))
  course_service = CoursesService(app.courses, teacher_service)
  
  filtered_courses = course_service.get_courses(career, level, semester, shift)
  
  return filtered_courses
  
  
@app.get('/schedules/', tags=['Schedules'])
async   def generate_schedules(request: ScheduleGeneratorRequest):
  start = time.time()
  teacher_service = TeacherService(app.teachers, BS4WebScraper(AzureEvaluator()))
  courses_service = CoursesService(app.courses, teacher_service)
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
  
  

@app.post('/upload/')
async def load(
    file: UploadFile,
    file2: UploadFile = None,
    level: Annotated[str, Form()] = None,
    semester: Annotated[str, Form()] = None,
    start_time: Annotated[str, Form()] = None,
    end_time: Annotated[str, Form()] = None,
    length: Annotated[int, Form] = 7
  ):
  
  start = time.time()
  teacher_service = TeacherService(app.teachers, BS4WebScraper(AzureEvaluator()))
  courses_service = CoursesService(app.courses, teacher_service)
  schedules_service = SchedulesService(teacher_service)
  
  courses: List[Course] = courses_service.parse_courses(await file.read())
  
  if file2:
    courses = courses + courses_service.parse_courses(await file2.read())
 
 
  print(f'Número de cursos sin filtrar: {len(courses)}')
  courses = courses_service.filter_coruses(courses, level, semester, start_time, end_time)
  print(f'Número de cursos después de filtrar {len(courses)}')
  
  print('Geneerado horarios...')
  schedules = schedules_service.generate_schedules(courses, length)
  
  print('Ordenadno horarios...')
  schedules = sorted(schedules, key=lambda x: x.popularity, reverse=True)
  print(f'Número de horarios generados: {len(schedules)}')
  
  end = time.time()
  print("Time Taken: {:.6f}s".format(end-start))

  return schedules[:25]
  
  

@app.on_event('shutdown')
def shutdown_db_clients():
  app.teachers.disconnect()
  app.courses.disconnect()
