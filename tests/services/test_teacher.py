from unittest import TestCase
from unittest.mock import Mock

from models.teacher import Teacher, PyObjectId
from services.teacher import TeacherService

class TestTeacherService(TestCase):
  def setUp(self) -> None:
    self.mock_repository = Mock()
    self.mock_scraper = Mock()
    self.teacher_service = TeacherService(self.mock_repository, self.mock_scraper)
    
    
  def test_get_teacher_with_valid_name(self):
    self.mock_repository.get_teacher.return_value = Teacher(
        _id = PyObjectId('64b350e30cb4efbc9e08937a'),
        name="JOSE LUIS PEREZ",
        url='https://foroupiicsa.net/diccionario/buscar/JOSE+LUIS+PEREZ',
        subjects=[],
        positive_score=0,
        comments=[]
      )
    
    result = self.teacher_service.get_teacher('JOSE LUIS PEREZ')
    
    self.mock_repository.get_teacher.assert_called_once_with('JOSE LUIS PEREZ')

    self.assertEqual(str(result.id), '64b350e30cb4efbc9e08937a'),
    self.assertEqual(result.name, 'JOSE LUIS PEREZ')
    
  def test_get_teacher_with_invalid_name(self):
    self.mock_repository.get_teacher.return_value = None
    self.mock_scraper.find_teacher.return_value = None
    
    invalid_teacher_name: str = 'Invalid Teacher'
    
    result = self.teacher_service.get_teacher(invalid_teacher_name)
    
    self.mock_repository.get_teacher.assert_called_once_with(invalid_teacher_name.upper())
    self.mock_scraper.find_teacher.assert_called_once_with(invalid_teacher_name.upper())
    
    self.assertIsNone(result)

