from pydantic import BaseModel
from models.course import Course
from typing import List

class Schedule(BaseModel):
  courses: List[Course]
  # start_time: str
  # end_time:str
  popularity: float