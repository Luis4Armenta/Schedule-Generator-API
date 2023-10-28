from pymongo import MongoClient
from typing import TypedDict, List

from courses.domain.model.course import Course
from courses.domain.ports.courses_repository import CourseRepository

from utils.text import generate_regex

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

  def get_courses(
      self,
      levels: List[str],
      career: str,
      semesters: List[str],
      shifts: List[str] = ['M', 'V'],
      subjects: List[str] = []
    ) -> List[Course]:
    expression = generate_regex(levels, career, shifts, semesters)
    query = {
      "sequence": {
        "$regex": expression,
        "$options": 'i'
      }
    }
    
    if subjects:
      query['subject'] = {
        "$in": subjects
      }
    

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
    
  def update_course_availability(self, sequence: str, subject: str, new_course_availability: int):
    course = self.course_collection.find_one({
      'sequence': sequence,
      'subject': subject
    })
    
    if course:
      self.course_collection.update_one(
        {'_id': course['_id']},
        {'$set': {'course_availability': new_course_availability}}
      )
  
  def disconnect(self) -> None:
    self.mongo_client.close()
    