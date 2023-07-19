from fastapi import FastAPI
from dotenv import dotenv_values
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from routes.course import router as course_router
from routes.teacher import router as teacher_router
from routes.schedule import router as schedule_router
from repositories.courses_repository import CourseRepository
from repositories.teachers_repository import TeacherRepository
from repositories.mongo_teachers_repository import MongoTeachersRepository
from repositories.mongo_courses_repository import MongoCourseRepository

from utils.enums import Tags

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
  
  teacher_router.teachers = app.teachers  
  course_router.teachers = app.teachers
  schedule_router.teachers = app.teachers
    
  course_router.courses = app.courses  
  schedule_router.courses = app.courses  

origins = ["*"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(teacher_router, tags=[Tags.teachers])
app.include_router(course_router, tags=[Tags.courses])
app.include_router(schedule_router, tags=[Tags.schedules])



@app.get('/', tags=['home'])
def message() -> HTMLResponse:
  return HTMLResponse('<h1>Profesores API</h1>')



@app.on_event('shutdown')
def shutdown_db_clients():
  app.teachers.disconnect()
  app.courses.disconnect()
