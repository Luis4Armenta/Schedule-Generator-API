from typing import Optional, TypedDict, Tuple, List
from pydantic import BaseModel

session = Optional[Tuple[str, str]]

class ScheduleCourse(TypedDict):
  monday: session
  tuesday: session
  wednesday: session
  thursday: session
  friday: session

class Course(BaseModel):
  id: Optional[str]
  
  sequence: str
  teacher: str
  subject: str
  teacher_popularity: Optional[float]
  
  level: str
  career:str
  shift: str
  semester: str
  consecutive: str
  
  schedule: ScheduleCourse
  
class Schedule(BaseModel):
  courses: List[Course]
  popularity: float
  