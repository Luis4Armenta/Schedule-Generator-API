from typing import Optional, List

from courses.domain.model.course import Course, CourseAvailability
from courses.domain.ports.courses_repository import CourseRepository

from subjects.application.subject import SubjectService
from teachers.application.teacher import TeacherService

from courses.application.course_filter.filter import CourseFilter, CourseChecker
from courses.application.course_filter.checkers import SubjectChecker, TeacherChecker, TimeChecker, AvailabilityChecker

class CourseService:
  def __init__(
      self,
      course_repository: CourseRepository,
      teacher_service: TeacherService,
      subject_service: SubjectService
    ):
    self.course_repository = course_repository
    self.teacher_service = teacher_service
    self.subject_service = subject_service
  
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

  def upload_courses(self, courses: List[Course]):
    for course in courses:
      teacher = self.teacher_service.get_teacher(course.teacher)
      sequence = course.sequence
      print(sequence[1], course.subject)
      subject = self.subject_service.get_subject(sequence[1], course.subject)
      popularity: float = 0.0
      if teacher:
        popularity = teacher.positive_score
      else:
        popularity = 0.5
      
      course.teacher_popularity = popularity
      print("Nombre de la materia:", course.subject)
      print("sequencia de la materia:", course.sequence)
      print("subject:", subject)
      course.required_credits = subject.credits_required
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



