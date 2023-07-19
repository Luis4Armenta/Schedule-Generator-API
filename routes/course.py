from typing import List

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi.responses import JSONResponse

from models.course import Course
from schemas.schedule import CoursesRequest

from services.course import CourseService
from services.teacher import TeacherService
from services.scraper import BS4WebScraper
from services.text_analyzer.text_analyzer import TextAnalyzer
from services.text_analyzer.azure_text_analyzer import AzureTextAnalyzer

router = APIRouter()

@router.post('/courses/', tags=['Courses'])
async def upload_schedules(file: UploadFile):
  teacher_evaluator: TextAnalyzer = AzureTextAnalyzer()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(teacher_evaluator))
  course_service = CourseService(router.courses, teacher_service)
  
  courses: List[Course] = course_service.parse_courses(await file.read())
  course_service.upload_courses(courses)
  
  return JSONResponse(content={"message": "Schedules uploaded!"}, status_code=202)

@router.get('/courses/', tags=['Courses'])
def get_courses(request: CoursesRequest):
  teacher_evaluator: TextAnalyzer = AzureTextAnalyzer()
  teacher_service = TeacherService(router.teachers, BS4WebScraper(teacher_evaluator))
  course_service = CourseService(router.courses, teacher_service)
  
  filtered_courses = course_service.get_courses(request.career, request.levels, request.semesters, request.shifts)
  
  return filtered_courses
  