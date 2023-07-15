from pydantic import BaseModel
from typing import List, Optional, Tuple

class ScheduleGeneratorRequest(BaseModel):
  levels: List[str]
  semesters: List[str]
  start_time: Optional[str] = '07:00'
  end_time: Optional[str] = '22:00'
  career: str
  shifts: List[str] = ['M', 'V']
  length: int = 7
  excluded_teachers: List[str] = []
  excluded_subjects: List[str] = []
  # subjects_required: List[Tuple[str, str]] = []
  
class CoursesRequest(BaseModel):
  career: str
  levels: List[str]
  semesters: List[str]
  shifts: List[str] = ['M', 'V']