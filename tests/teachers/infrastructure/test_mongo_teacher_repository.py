import unittest
from unittest.mock import MagicMock, patch
from teachers.domain.model.teacher import Teacher, PyObjectId
from teachers.infrastructure.mongo_teachers_repository import MongoTeachersRepository, MongoConfig
from comments.domain.comment import Comment
from bson import ObjectId

class TestMongoTeachersRepository(unittest.TestCase):
  def setUp(self) -> None:
    config = MongoConfig(host='localhost', port=27017, database='test_database')
    self.repository = MongoTeachersRepository(config)
    self.mock_teacher = Teacher(
        id=PyObjectId(ObjectId()),
        name='John Doe',
        url='http://example.com',
        subjects=['Math'],
        comments=[Comment(
            teacher='John Doe',
            text="Good doctor",
            likes=0,
            dislikes=0,
            date='11 Dic 2022',
            subject='Math',
            positive_score=0.8,
            neutral_score=0.2,
            negative_score=0.0,
          )],
        positive_score=0.8
      )
    
  def tearDown(self):
    self.repository.disconnect()

  @patch('teachers.infrastructure.mongo_teachers_repository.MongoClient')
  def test_connect(self, mock_mongo_client: MagicMock):
    self.repository.connect()
    
    mock_mongo_client.assert_called_once_with(host='localhost', port=27017)
    self.assertIsNotNone(self.repository.mongo_client)
    self.assertIsNotNone(self.repository.database)
    self.assertIsNotNone(self.repository.teachers_collection)
    self.assertIsNotNone(self.repository.subjects_collection)

  @patch('teachers.infrastructure.mongo_teachers_repository.MongoClient')
  def test_get_teacher(self, mock_mongo_client):
    self.repository.connect()
    teacher_name = 'John Doe'
    
    teacher_data = {
      '_id': '64b350e30cb4efbc9e08937a',
      'name': 'John Doe',
      'url': 'http://example.com',
      'subjects': ['Math'],
      'comments': [{
          'teacher': 'John Doe',
          'text': "Good doctor",
          'likes': 0,
          'dislikes': 0,
          'date': '11 Dic 2022',
          'subject': 'Math',
          'positive_score': 0.8,
          'neutral_score': 0.2,
          'negative_score': 0.0,
      }],
      'positive_score':0.8
    }
    self.repository.teachers_collection.find_one = MagicMock(return_value=teacher_data)
    
    teacher = self.repository.get_teacher(teacher_name)
    self.assertEqual(teacher.name, teacher_name)

    self.repository.disconnect()
  
  @patch('teachers.infrastructure.mongo_teachers_repository.MongoClient')
  def test_get_nonexistent_teacher(self, mock_mongo_client):
    self.repository.connect()
    teacher_name = 'Nonexistent Teacher'
    self.repository.teachers_collection.find_one = MagicMock(return_value=None)
    teacher = self.repository.get_teacher(teacher_name)
    
    self.assertIsNone(teacher)
    self.repository.disconnect()
    
    
