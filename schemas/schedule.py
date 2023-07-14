from pydantic import BaseModel, Field
from typing import List, Optional

class ScheduleGeneratorRequest(BaseModel):
  levels: List[str]
  semesters: List[str]
  start_time: Optional[str] = '07:00'
  end_time: Optional[str] = '22:00'
  career: str
  unwanted_teachers: List[str] = []
  shifts: List[str] = ['M', 'V']
  length: int = 7
  
class CoursesRequest(BaseModel):
  career: str
  levels: List[str]
  semesters: List[str]
  shifts: List[str] = ['M', 'V']