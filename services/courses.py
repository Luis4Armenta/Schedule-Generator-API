from typing import Optional, List
from models.course import Course, session, ScheduleCourse
from lxml import etree
from bs4 import BeautifulSoup

class CoursesService:
  def __init__(self):
    pass
  
  def filter_coruses(
    self,
    courses: List[Course],
    level: Optional[str],
    semester: Optional[str],
    start_time: Optional[str],
    end_time: Optional[str], 
  ) -> List[Course]:
    filtered_courses: List[Course] = []
    
    for course in courses:
      
      # filter courses by level
      if level:
        if course.sequence.upper()[0] != level.upper():
          continue
      
      # filter courses by semester
      if semester:
        if course.sequence.upper()[3] != semester.upper():
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
      sessions = get_sessions(raw_course)
      
      schedule_course: ScheduleCourse = ScheduleCourse()
      schedule_course['monday'] = sessions[0]
      schedule_course['tuesday'] = sessions[1]
      schedule_course['wednesday'] = sessions[2]
      schedule_course['thursday'] = sessions[3]
      schedule_course['friday'] = sessions[4]
      
      course = Course(
        id=idx,
        sequence=raw_course.xpath('./td/text()')[0],
        subject=raw_course.xpath('./td/text()')[1],
        teacher=raw_course.xpath('./td/text()')[2],
        schedule=schedule_course
      )

      courses.append(course)

    return courses
      
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