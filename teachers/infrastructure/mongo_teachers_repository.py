from pymongo import MongoClient
from typing import TypedDict, Optional

from teachers.domain.model.teacher import Teacher
from teachers.domain.ports.teachers_repository import TeacherRepository

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
class MongoTeachersRepository(TeacherRepository):
  def __init__(self, config: MongoConfig):
    self.config = config
    
  def connect(self) -> None:
    self.mongo_client = MongoClient(host=self.config['host'], port=self.config['port'])
    self.database = self.mongo_client[self.config['database']]
    self.teachers_collection = self.database['teachers']
    self.subjects_collection = self.database['subjects']
    
  def get_teacher(self, teacher_name: str) -> Optional[Teacher]:
    teacher = self.teachers_collection.find_one({'name': teacher_name})

    if teacher:
      subject_ids = teacher.get('subjects', [])
      subjects = self.subjects_collection.find({'_id': {'$in': subject_ids}})
      subjects = [subject.get('name', '') for subject in list(subjects)]
      
      return Teacher(
        id=teacher['_id'],
        name=teacher['name'],
        url=teacher['url'],
        subjects=subjects,
        comments=teacher['comments'],
        positive_score=teacher['positive_score']
      )
    else:
      return None
  
  def add_teacher(self, teacher: Teacher) -> None:
    subjects = teacher.subjects
    
    teacher.subjects = []
    
    teacher_id = self.teachers_collection.insert_one(teacher.dict()).inserted_id
    
    for subject in subjects:
      self._add_subject_to_teacher(teacher_id, subject)
      

  def _add_subject_to_teacher(self, teacher_id, subject_name: str):
    # Verificar si la asignatura ya existe en la colección
    subject = self.subjects_collection.find_one({"name": subject_name})
    
    # Si la asignatura no existe, crearla y obtener su ID
    if subject is None:
        subject = {"name": subject_name, "teachers": [teacher_id]}
        subject_id = self.subjects_collection.insert_one(subject).inserted_id
    else:
        subject_id = subject["_id"]

        # Verificar si el profesor ya está en la lista de profesores de la asignatura
        if teacher_id not in subject["teachers"]:
            # Agregar el profesor a la lista de profesores de la asignatura
            self.subjects_collection.update_one({"_id": subject_id}, {"$addToSet": {"teachers": teacher_id}})
    
    # Agregar la referencia de la asignatura al profesor
    self.teachers_collection.update_one({"_id": teacher_id}, {"$addToSet": {"subjects": subject_id}})  
    
  def disconnect(self) -> None:
    self.mongo_client.close()
    