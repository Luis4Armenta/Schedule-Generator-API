from abc import ABC

from lxml import etree
from bs4 import BeautifulSoup

from models.course import Course, session, ScheduleCourse, CourseAvailability
from services.teacher import TeacherService
from typing import List

class SAESService(ABC):
  def get_courses(self, document) -> List[Course]:
    pass
  
  
class SaesService(SAESService):
  def __init__(self, teacher_service: TeacherService):
    self.teacher_service = teacher_service
    
  def get_courses(self, document) -> List[Course]:
    courses: List[Course] = []

    dom = etree.HTML(str(BeautifulSoup(document, 'html.parser', from_encoding='utf8')))
    raw_courses = dom.xpath('//table[@id="ctl00_mainCopy_dbgHorarios"]//tr')[1:]


    for idx, raw_course in enumerate(raw_courses):
      sequence = raw_course.xpath('./td/text()')[0].strip().upper()
      teacher_name = raw_course.xpath('./td/text()')[2]

      sessions = get_sessions(raw_course)
      
      schedule_course: ScheduleCourse = ScheduleCourse()
      schedule_course['monday'] = sessions[0]
      schedule_course['tuesday'] = sessions[1]
      schedule_course['wednesday'] = sessions[2]
      schedule_course['thursday'] = sessions[3]
      schedule_course['friday'] = sessions[4]
      
      teacher = self.teacher_service.get_teacher(teacher_name)
      
      popularity: float = 0.0
      if teacher:
        popularity = teacher.positive_score
      else:
        popularity = 0.5
        

      course = Course(
        id=idx,
        sequence=sequence,
        subject=raw_course.xpath('./td/text()')[1],
        teacher=teacher_name,
        schedule=schedule_course,
        teacher_popularity=popularity
      )

      courses.append(course)

    return courses
  
  def get_course_availability(self, document) -> List[CourseAvailability]:
    availabilities: List[CourseAvailability] = []
    
    dom = etree.HTML(str(BeautifulSoup(document, 'html.parser', from_encoding='utf8')))
    raw_courses = dom.xpath('//table[@id="ctl00_mainCopy_GrvOcupabilidad"]//tr')[1:]
    
    for raw_course in raw_courses:
      sequence: str = raw_course.xpath('./td/text()')[0].strip().upper()
      subject: str = raw_course.xpath('./td/text()')[2].strip().upper()
      course_avalibility = int(raw_course.xpath('./td/text()')[6].strip())
    
    
      a = CourseAvailability(
        sequence=sequence,
        subject=subject,
        course_availability=course_avalibility
      )
      availabilities.append(a)
      
    return availabilities
  
def get_sessions(raw_course) -> session:
  sessions: List[session] = []
  
  days = raw_course.xpath('./td/text()')[5:-1]
  for day in days:
    day: str = day.strip()
    if day:
      sessions.append(tuple(day.split('-')))
    else:
      sessions.append(None)
      
  return sessions
