import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from routes.course import router as course_router
from routes.teacher import router as teacher_router
from routes.schedule import router as schedule_router
from courses.domain.ports.courses_repository import CourseRepository
from teachers.domain.ports.teachers_repository import TeacherRepository
from subjects.domain.ports.subjects_repository import SubjectRepository
from teachers.infrastructure.mongo_teachers_repository import MongoTeachersRepository
from courses.infrastructure.mongo_courses_repository import MongoCourseRepository
from subjects.infrastructure.mongo_subjects_repository import MongoSubjectsRepository

from utils.enums import Tags

app = FastAPI()
app.title = 'Profesores-API'
app.version = '0.0.1'

@app.on_event('startup')
def startup_db_clients():
  app.teachers: TeacherRepository = MongoTeachersRepository({
    'host': os.environ['MONGODB_HOST'],
    'port': int(os.environ['MONGODB_PORT']),
    'database': os.environ['MONGODB_DATABASE']
  })
  
  app.teachers.connect()
  
  app.courses: CourseRepository = MongoCourseRepository({
    'host': os.environ['MONGODB_HOST'],
    'port': int(os.environ['MONGODB_PORT']),
    'database': os.environ['MONGODB_DATABASE']
  })
  
  app.courses.connect()
  
  app.subjects: SubjectRepository = MongoSubjectsRepository({
    'host': os.environ['MONGODB_HOST'],
    'port': int(os.environ['MONGODB_PORT']),
    'database': os.environ['MONGODB_DATABASE']
  })
  
  app.subjects.connect()
  
  teacher_router.teachers = app.teachers  
  course_router.teachers = app.teachers
  schedule_router.teachers = app.teachers
    
  course_router.courses = app.courses  
  schedule_router.courses = app.courses  
  
  course_router.subjects = app.subjects
  schedule_router.subjects = app.subjects

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
  app.subjects.disconnect()
