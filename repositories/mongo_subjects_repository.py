from pymongo import MongoClient
from typing import TypedDict, Optional
from models.course import Subject


from repositories.subjects_repository import SubjectRepository


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper

class MongoConfig(TypedDict):
  host: str
  port: int
  database: str

@singleton
class MongoSubjectsRepository(SubjectRepository):
  def __init__(self, config: MongoConfig):
    self.config = config
    
  def connect(self) -> None:
    self.mongo_client = MongoClient(host=self.config['host'], port=self.config['port'])
    self.database = self.mongo_client[self.config['database']]
    self.subjects_collection = self.database['subjects1']
    
  def add_subject(self, subject: Subject) -> None:
    print(subject)
    self.subjects_collection.insert_one(subject).inserted_id
  
  def get_subject(self, career: str, name: str) -> Optional[Subject]:
    subject = self.subjects_collection.find_one({'career': career, 'name': name})

    if subject:
      return Subject(
        career=subject['career'],
        key=subject['key'],
        level=subject['level'],
        name=subject['name'],
        plan=subject['plan'],
        required=subject['required'],
        credits_required=subject['credits_required']
      )
    else:
      return None

  def disconnect(self) -> None:
    self.mongo_client.close()
    