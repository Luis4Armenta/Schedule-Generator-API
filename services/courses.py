import re
from lxml import etree
from bs4 import BeautifulSoup
from unidecode import unidecode
from typing import Optional, List
from models.course import Course, session, ScheduleCourse
from repositories.courses_repository import CourseRepository
from repositories.teachers_repository import TeacherRepository
from services.teacher import TeacherService

class CoursesService:
  def __init__(self, course_repository: CourseRepository, teacher_service: TeacherService):
    self.course_repository = course_repository
    self.teacher_repository = teacher_service
  
  def filter_coruses(
    self,
    courses: List[Course],
    start_time: Optional[str],
    end_time: Optional[str],
    excluded_teachers: List[str] = [],
    excluded_subjects: List[str] = []
  ) -> List[Course]:
    excluded_teachers = [clean_name(unwanted_teacher) for unwanted_teacher in excluded_teachers]
    excluded_subjects = [clean_name(excluded_subject) for excluded_subject in excluded_subjects]

    filtered_courses: List[Course] = []
    
    for course in courses:
      # excluding teachers
      if clean_name(course.teacher) in excluded_teachers:
        continue
      
      # excluding subjects
      if clean_name(course.subject) in excluded_subjects:
        continue
      
      # filter courses by time
      if start_time or end_time:
        start_time = start_time if start_time else '07:00'
        end_time = end_time if end_time else '22:00'
        
        out_time = False
        
        for _, session in course.schedule.items():
          if session is not None:
            session_start, session_end = session
            
            if session_start < start_time or session_end > end_time:
              out_time = True
              break
        
        if out_time:
          continue
            
      
      
      filtered_courses.append(course)
    return filtered_courses
  
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
      
      teacher = self.teacher_repository.get_teacher(teacher_name)
      
      popularity: float = 0.0
      if teacher:
        popularity = teacher.polarity
      else:
        popularity = 0.5
        

      course = Course(
        id=idx,
        sequence=sequence,
        subject=raw_course.xpath('./td/text()')[1],
        teacher=teacher_name,
        schedule=schedule_course,

        level=sequence[0],
        career=sequence[1],
        shift=sequence[2],
        semester=sequence[3],
        consecutive=sequence[4],
        teacher_popularity=popularity
      )

      courses.append(course)

    return courses

  def upload_courses(self, courses: List[Course]):
    for course in courses:
      teacher = self.teacher_repository.get_teacher(course.teacher)
      
      popularity: float = 0.0
      if teacher:
        popularity = teacher.polarity
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
    ):
    
    expression = generate_regex(levels, career, shifts, semesters)
    query = {
      "sequence": {
        "$regex": expression,
        "$options": 'i'
      }
    }
    
    return self.course_repository.get_courses(query)
  

def generate_regex(levels: List[str], career, shifts: List[str], semesters: List[str]):
    level_regex = '|'.join(levels)
    career_regex = re.escape(career)
    shift_regex = '|'.join(shifts)
    semester_regex = '|'.join(semesters)
    
    regex_pattern = r'^[' + level_regex + r'][' + career_regex + r'][' + shift_regex + r'][' + semester_regex + r'][0-9]+$'
    return regex_pattern

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

def clean_name(name: str) -> str:
    # Convertir caracteres especiales a su equivalente sin acentos
    cleaned_name = unidecode(name)
    # Eliminar caracteres no alfabéticos y convertir a mayúsculas
    cleaned_name = re.sub(r'[^a-zA-Z\s]', '', cleaned_name).upper()
    # Eliminar espacios innecesarios
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name)
    # Eliminar espacios al inicio y al final de la cadena
    cleaned_name = cleaned_name.strip()
    return cleaned_name