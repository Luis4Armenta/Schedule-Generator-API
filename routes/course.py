from fastapi import Query
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from fastapi import Query, UploadFile
from schemas.schedule import CoursesRequest
from services.courses import CoursesService
from fastapi.responses import JSONResponse
from services.teacher import TeacherService
from services.scraper import BS4WebScraper
from services.evaluator.evaluator import TeacherEvaluator
from services.evaluator.azure_evaluator import AzureEvaluator
from models.course import Course
from typing import List

router = APIRouter()

@router.post('/courses/', tags=['Courses'])
async def upload_schedules(file: UploadFile):
  teacher_evaluator: TeacherEvaluator = AzureEvaluator()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(teacher_evaluator))
  course_service = CoursesService(router.courses, teacher_service)
  
  courses: List[Course] = course_service.parse_courses(await file.read())
  course_service.upload_courses(courses)
  
  return JSONResponse(content={"message": "Schedules uploaded!"}, status_code=202)

@router.get('/courses/', tags=['Courses'])
def get_courses(request: CoursesRequest):
  teacher_evaluator: TeacherEvaluator = AzureEvaluator()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(teacher_evaluator))
  course_service = CoursesService(router.courses, teacher_service)
  
  filtered_courses = course_service.get_courses(request.career, request.levels, request.semesters, request.shifts)
  
  return filtered_courses
  