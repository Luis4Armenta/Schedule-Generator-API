from typing import Optional, TypedDict, Tuple, List
from pydantic import BaseModel, Field

session = Optional[Tuple[str, str]]

class ScheduleCourse(TypedDict):
  monday: session
  tuesday: session
  wednesday: session
  thursday: session
  friday: session

class Course(BaseModel):
  id: Optional[str]
  
  sequence: str = Field(title="Secuencia", description="Grupo al que pertenece el curso")
  teacher: str = Field(title="Instrictor", description="Nombre del instructor que imparte el curso")
  subject: str = Field(title="Asignatura", description="Nombre de la asignatura")
  teacher_popularity: Optional[float] = Field(title="Puntaje positivo del profesor", description="Puntaje positivo promedio del profesor calculado por el sistema.")
  
  schedule: ScheduleCourse = Field(title="Horario")
  
class Schedule(BaseModel):
  courses: List[Course]
  popularity: float
  