from pydantic import BaseModel, Field
from typing import Optional

from shared.comment import IComment
from shared.teacher import ITeacher

class ScrapedComment(IComment, BaseModel):
  subject: str = Field(title="Nombre de la asignatura")
  text: str = Field(title="Comentario")
  date: str = Field(title="Fecha de publicación")
  likes: int = Field(title="Número de likes", ge=0)
  dislikes: int = Field(title='Número de dislikes', ge=0)

class SentimentAnalysis(BaseModel):
  positive_score: float
  neutral_score: float
  negative_score: float

class Teacher(ITeacher, BaseModel):
  name: str
  
  def __str__(self):
    return self.name

class Comment(IComment, BaseModel):
  subject: str = Field(title="Nombre de la asignatura")
  text: str = Field(title="Comentario")
  date: str = Field(title="Fecha de publicación")
  likes: int = Field(title="Número de likes", ge=0)
  dislikes: int = Field(title='Número de dislikes', ge=0)
  teacher: Teacher = Field(title="Nombre del profesor")
  positive_score: float = Field(title="Puntuación positiva", description="Sentimiento positivo percibido en el comentario por el sistema.")
  neutral_score: float = Field(title="Puntuación neutra", description="Sentimiento neutro percibido en el comentario por el sistema.")
  negative_score: float = Field(title="Puntuación negativa", description="Sentimiento negativo percibido en el comentario por el sistema.")
  