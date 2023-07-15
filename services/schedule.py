from statistics import mean, median

from typing import List

from models.course import Course
from models.schedule import Schedule

from services.teacher import TeacherService

class ScheduleService:
  def __init__(self, teacher_service: TeacherService):
    self.teacher_service = teacher_service
  
  def select_a_course(self, courses: List[Course], selected_course: Course) -> List[Course]:
    filtered_courses: List[Course] = []
  
    for course in courses:
      if course == selected_course:
        filtered_courses.append(course)
        continue
      
      if course.subject == selected_course.subject:
        continue
      
      has_overlap: bool = False
      
      for day, day_session in course.schedule.items():
        if day_session and selected_course.schedule.get(day):
          session_start, session_end = day_session
          selected_session_start, selected_session_end = selected_course.schedule[day]
          
          if not (session_end <= selected_session_start or session_start >= selected_session_end):
            has_overlap = True
            break
      
      if not has_overlap:
        filtered_courses.append(course)
        
    return filtered_courses

  def generate_schedules(
      self,
      courses: List[Course],
      n: int,
      required_subjects: List[str] = [],
    ) -> List[Schedule]:
    def backtrack(schedule: List[Course], start_index: int):
      # Verificar si se ha alcanzado el tamaño objetivo del horario
      if len(schedule) == n:
        schedule_subjects = [course.subject for course in schedule]
        
        if all(required_subject in schedule_subjects for required_subject in required_subjects):
          # Calcular la polaridad promedio de los profesores en el horario
          teachers_polarity: List[float] = []
          for course in schedule:
            teachers_polarity.append(course.teacher_popularity)
          
          schedule_result = Schedule(
            popularity=mean(teachers_polarity),
            courses=schedule,
          )
          schedules.append(schedule_result)
          return
        else:
          return

      # Iterar sobre los cursos regulares, comenzando desde el índice de inicio
      for i in range(start_index, len(courses)):
        if is_valid(schedule, courses[i]):
          schedule.append(courses[i])
          backtrack(schedule, i + 1)
          schedule.pop()

    # Verificar si un curso es válido para agregar al horario actual
    def is_valid(schedule: List[Course], course: Course) -> bool:
      for existing_course in schedule:
        if has_overlap(existing_course, course) or existing_course.subject == course.subject:
          return False
      return True

    # Verificar si dos cursos tienen superposición en su horario
    def has_overlap(course1: Course, course2: Course) -> bool:
      for day, session1 in course1.schedule.items():
        session2 = course2.schedule.get(day)
        if session1 and session2:
          session1_start, session1_end = session1
          session2_start, session2_end = session2

          if not (session1_end <= session2_start or session1_start >= session2_end):
            return True
      return False

    schedules = []  # Lista para almacenar los horarios generados
    backtrack([], 0)  # Iniciar la generación de horarios desde un horario vacío y el índice de inicio 0
    return schedules

    