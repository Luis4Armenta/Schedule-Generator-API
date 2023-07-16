from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, TypedDict, Optional


class PyObjectId(ObjectId):
  @classmethod
  def __get_validators__(cls):
    yield cls.validate

  @classmethod
  def validate(cls, v):
    if not ObjectId.is_valid(v):
      raise ValueError("Invalid objectid")
    return ObjectId(v)

  @classmethod
  def __modify_schema__(cls, field_schema):
    field_schema.update(type="string")

class Comment(TypedDict):
  subject: str
  text: str
  date: str
  likes: int
  dislikes: int
  positive_score: Optional[float]
  neutral_score: Optional[float]
  negative_score: Optional[float]
  

class Teacher(BaseModel):
  id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
  name: str = Field(...)
  url: str = Field(...)
  subjects: List[str] = Field(...)
  positive_score: float = Field(...)
  comments: List[Comment] = Field(...)
  
  class Config:
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}
    schema_extra = {
      "example": {
          "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
          "name": "José Pérez",
          "subjects": ["Probabilidad"],
          "comments": [{
            "text": "Este es un buen profesor.",
            "date": "21-11-2019",
            "likes": 5,
            "dislikes": 0,
            "positive_score": 0.5,
            "neutral_score": 0.3,
            "negative_score": 0.2
          }],
          "positive_score": 0.22
        }
    }