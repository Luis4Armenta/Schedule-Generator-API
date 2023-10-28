from typing import Optional, TypedDict, Tuple, List
from pydantic import BaseModel, Field

session = Optional[Tuple[str, str]]

class ScheduleCourse(TypedDict):
  monday: session
  tuesday: session
  wednesday: session
  thursday: session
  friday: session

class CourseAvailability(BaseModel):
  sequence: str
  subject: str
  course_availability: int

class Course(BaseModel):
  id: Optional[str]
  
  sequence: str = Field(title="Secuencia", description="Grupo al que pertenece el curso")
  teacher: str = Field(title="Instrictor", description="Nombre del instructor que imparte el curso")
  subject: str = Field(title="Asignatura", description="Nombre de la asignatura")
  course_availability: Optional[int] = Field(title="Disponibilidad", description="Número de lugares disponibles", default=40)
  teacher_popularity: Optional[float] = Field(title="Puntaje positivo del profesor", description="Puntaje positivo promedio del profesor calculado por el sistema.")
  
  required_credits: Optional[float] = Field(title="Creditos requeridos")
  schedule: ScheduleCourse = Field(title="Horario")

  