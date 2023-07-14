from models.course import Course
from typing import Any, TypedDict, Optional, List
from pymongo import MongoClient
from repositories.courses_repository import CourseRepository


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper

class MongoConfig(TypedDict):
  host: str
  port: int
  database: str

@singleton
class MongoCourseRepository(CourseRepository):
  def __init__(self, config: MongoConfig):
    self.config = config
    
  def connect(self) -> None:
    self.mongo_client = MongoClient(host=self.config['host'], port=self.config['port'])
    self.database = self.mongo_client[self.config['database']]
    self.course_collection = self.database['courses']

  def get_courses(self, query: dict) -> List[Course]:
    
    filtered_courses = self.course_collection.find(query)
    courses = [Course(**course) for course in filtered_courses]
    
    return courses
    
  def add_course_if_not_exist(self, course: Course) -> None:
    self.course_collection.update_one(
      {
        'sequence': course.sequence,
        'teacher': course.teacher,
        'subject': course.subject
      }, {
        '$set': course.dict()
      },
      upsert=True
    )
  
  def add_course(self, course: Course) -> None:    
    teacher_id = self.course_collection.insert_one(course.dict())

  def disconnect(self) -> None:
    self.mongo_client.close()
    