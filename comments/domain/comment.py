from pydantic import BaseModel, Field
from typing import Optional

class SentimentAnalysis(BaseModel):
  positive_score: float
  neutral_score: float
  negative_score: float

class Comment(BaseModel):
  teacher: str = Field(title="Nombre del profesor")
  subject: str = Field(title="Nombre de la asignatura")
  text: str = Field(title="Comentario")
  date: str = Field(title="Fecha de publicación")
  likes: int = Field(title="Número de likes", ge=0)
  dislikes: int = Field(title='Número de dislikes', ge=0)
  positive_score: Optional[float] = Field(title="Puntuación positiva", description="Sentimiento positivo percibido en el comentario por el sistema.")
  neutral_score: Optional[float] = Field(title="Puntuación neutra", description="Sentimiento neutro percibido en el comentario por el sistema.")
  negative_score: Optional[float] = Field(title="Puntuación negativa", description="Sentimiento negativo percibido en el comentario por el sistema.")
  