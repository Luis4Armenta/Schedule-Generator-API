import unittest
from unittest.mock import Mock
from courses.domain.model.course import CourseAvailability
from courses.application.course import CourseService

class TestCourseService(unittest.TestCase):
    def setUp(self):
        # Configura un objeto mock para el repositorio y servicios relacionados
        self.repository_mock = Mock()
        self.teacher_service_mock = Mock()
        self.subject_service_mock = Mock()
        self.course_service = CourseService(
            course_repository=self.repository_mock,
            teacher_service=self.teacher_service_mock,
            subject_service=self.subject_service_mock
        )

    def test_update_course_availability(self):
        # Configura un conjunto de disponibilidades simuladas
        simulated_availabilities = [
            CourseAvailability(sequence='4CM40', subject='Costrucción de software', course_availability=20),
            CourseAvailability(sequence='4CM40', subject='Comunicación de datos', course_availability=15),
        ]

        # Llama al método update_course_availability con las disponibilidades simuladas
        self.course_service.update_course_availability(simulated_availabilities)

        # Verifica que el método update_course_availability del repositorio se llamó con cada disponibilidad simulada
        for availability in simulated_availabilities:
            self.repository_mock.update_course_availability.assert_any_call(
                sequence=availability.sequence,
                subject=availability.subject,
                new_course_availability=availability.course_availability
            )

