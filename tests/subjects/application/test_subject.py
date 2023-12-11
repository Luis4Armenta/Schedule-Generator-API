import unittest
from unittest.mock import Mock
from subjects.domain.model.subject import Subject
from subjects.domain.ports.subjects_repository import SubjectRepository
from subjects.application.subject import SubjectService


class TestSubjectService(unittest.TestCase):
    def setUp(self):
        # Configura un objeto mock para el repositorio
        self.repository_mock = Mock(spec=SubjectRepository)
        self.subject_service = SubjectService(
            subject_repository=self.repository_mock)

    def test_upload_subjects(self):
        # Configura un conjunto de sujetos simulados
        simulated_subjects = [Subject(
            career='Ciencias de la informática',
            plan='2021',
            level=4,
            key='C404',
            name='Construcción de software',
            required=True,
            credits_required=5.0
          ),
        Subject(
            career='Ciencias de la informática',
            plan='2021',
            level=4,
            key='C405',
            name='Comunicación de datos',
            required=True,
            credits_required=6.0
          )
        ]

        # Llama al método upload_subjects con los sujetos simulados
        self.subject_service.upload_subjects(simulated_subjects)

        # Verifica que el método add_subject del repositorio se llamó con cada sujeto simulado
        for subject in simulated_subjects:
            self.repository_mock.add_subject.assert_any_call(subject.dict())
            
    def test_get_subject_with_existing_subject(self):
        # Configura el mock del repositorio para devolver un sujeto existente
        existing_subject = Subject(
            career='Ciencias de la informática',
            plan='2021',
            level=4,
            key='C405',
            name='Comunicación de datos',
            required=True,
            credits_required=6.0
          )
        self.repository_mock.get_subject.return_value = existing_subject

        # Llama al método get_subject con un conjunto de datos simulado
        result_subject = self.subject_service.get_subject('Ciencias de la informática', 'Comunicación de datos')

        # Verifica que el resultado sea el sujeto existente del repositorio
        self.assertEqual(result_subject, existing_subject)
        
    def test_get_subject_with_nonexistent_subject(self):
        # Configura el mock del repositorio para devolver None
        self.repository_mock.get_subject.return_value = None

        # Llama al método get_subject con un conjunto de datos simulado
        result_subject = self.subject_service.get_subject('Ciencias de la informática', 'Química')

        # Verifica que el resultado sea None ya que el sujeto no existe
        self.assertIsNone(result_subject)
