import uuid
from pydantic import BaseModel, Field
from typing import List, TypedDict, Optional
from bson import ObjectId


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
  text: str
  date: str
  likes: int
  dislikes: int
  polarity: float
  

class Teacher(BaseModel):
  id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
  name: str = Field(...)
  url: str = Field(...)
  subjects: List[str] = Field(...)
  polarity: float = Field(...)
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
            "polarity": 0.5
          }],
          "polarity": 0.22
        }
    }