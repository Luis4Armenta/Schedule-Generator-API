import unittest
from unittest.mock import Mock
from teachers.application.teacher import TeacherService
from teachers.domain.ports.teachers_repository import TeacherRepository
from teachers.domain.model.teacher import Teacher
from comments.application.comment import CommentService
from comments.domain.comment import Comment

class TestTeacherService(unittest.TestCase):
    def setUp(self):
        # Configura objetos mock para el repositorio y el servicio de comentarios
        self.repository_mock = Mock(spec=TeacherRepository)
        self.comment_service_mock = Mock(spec=CommentService)
        self.teacher_service = TeacherService(
            repository=self.repository_mock,
            comment_service=self.comment_service_mock
        )

    def test_get_teacher_with_existing_teacher(self):
        # Configura el mock del repositorio para devolver un maestro existente
        existing_teacher = Teacher(name='Existing Teacher', subjects=[], comments=[], positive_score=0.5, url='https://example.com')
        self.repository_mock.get_teacher.return_value = existing_teacher

        # Llama al método get_teacher con el nombre de un maestro existente
        result_teacher = self.teacher_service.get_teacher('Existing Teacher')

        # Verifica que el resultado sea el maestro existente del repositorio
        self.assertEqual(result_teacher, existing_teacher)
        
    def test_get_teacher_unassigned(self):
      result_teacher = self.teacher_service.get_teacher('SIN ASIGNAR')
      
      self.assertEqual(result_teacher.name, 'SIN ASIGNAR')
      self.assertEqual(len(result_teacher.comments), 0)
      self.assertEqual(len(result_teacher.subjects), 0)
      self.assertEqual(result_teacher.positive_score, 0.5)
      
    def test_get_teacher_with_nonexistent_teacher(self):
        # Configura el mock del repositorio para devolver None
        self.repository_mock.get_teacher.return_value = None

        # Configura el mock del servicio de comentarios para devolver comentarios simulados
        simulated_comments = []
        self.comment_service_mock.seach_comments.return_value = simulated_comments

        # Llama al método get_teacher con el nombre de un maestro inexistente
        result_teacher = self.teacher_service.get_teacher('Nonexistent Teacher')

        # Verifica que el resultado sea un nuevo maestro construido a partir de comentarios simulados
        self.assertIsNotNone(result_teacher)
        self.assertEqual(result_teacher.name, 'NONEXISTENT TEACHER')
        self.assertEqual(result_teacher.comments, simulated_comments)
        self.assertEqual(result_teacher.positive_score, 0.5)
        self.assertEqual(result_teacher.url, 'https://foroupiicsa.net/diccionario/buscar/NONEXISTENT+TEACHER')

