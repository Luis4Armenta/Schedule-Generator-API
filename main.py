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
  courses_service = CoursesService()
  teacher_service = TeacherService(app.teachers, BS4WebScraper(AzureEvaluator()))
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
