from typing import Optional, List

from lxml import etree
from bs4 import BeautifulSoup

from models.course import Course, session, ScheduleCourse, CourseAvailability

from repositories.courses_repository import CourseRepository
from repositories.teachers_repository import TeacherRepository

from services.teacher import TeacherService
from services.course_filter.filter import CourseFilter, CourseChecker
from services.course_filter.checkers import SubjectChecker, TeacherChecker, TimeChecker, AvailabilityChecker


class CourseService:
  def __init__(self, course_repository: CourseRepository, teacher_service: TeacherService):
    self.course_repository = course_repository
    self.teacher_service = teacher_service
  
  def filter_coruses(
    self,
    courses: List[Course],
    start_time: Optional[str],
    end_time: Optional[str],
    min_course_availability: int = 1,
    excluded_teachers: List[str] = [],
    excluded_subjects: List[str] = [],
  ) -> List[Course]:
    checkers: List[CourseChecker] = [
      SubjectChecker(
        excluded_subjects=excluded_subjects
      ),
      TeacherChecker(
        excluded_teachers=excluded_teachers
      ),
      TimeChecker(
        start_time=start_time,
        end_time=end_time
      ),
      AvailabilityChecker(
        min_availability=min_course_availability
      )
    ]
    
    course_filter = CourseFilter(checkers)
    
    return course_filter.filter_courses(courses)
    

  def parse_courses(self, document) -> List[Course]:
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


  def parse_availabilities(self, document) -> List[CourseAvailability]:
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

  def upload_courses(self, courses: List[Course]):
    for course in courses:
      teacher = self.teacher_service.get_teacher(course.teacher)
      
      popularity: float = 0.0
      if teacher:
        popularity = teacher.positive_score
      else:
        popularity = 0.5
      
      course.teacher_popularity = popularity
      self.course_repository.add_course_if_not_exist(course)
  
  def get_courses(
      self,
      career: str,
      levels: List[str],
      semesters: List[str],
      shifts: List[str]
    ) -> List[Course]:
    
    return self.course_repository.get_courses(
      levels=levels,
      career=career,
      semesters=semesters,
      shifts=shifts
    )
  
  def get_courses_by_subject(
      self,
      sequence: str,
      subject: str,
      shifts: List[str] = ['M', 'V']
    ) -> List[Course]:
    level = sequence[0]
    career = sequence[1]
    semester = sequence[3]
    
    return self.course_repository.get_courses(
      levels=[level],
      shifts=shifts,
      career=career,
      semesters=[semester],
      subjects=[subject]
    )
  
  def update_course_availability(
    self,
    availabilities: List[CourseAvailability]
  ) -> None:
    for avalability in availabilities:
      self.course_repository.update_course_availability(
        sequence=avalability.sequence,
        subject=avalability.subject,
        new_course_availability=avalability.course_availability
      )


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

