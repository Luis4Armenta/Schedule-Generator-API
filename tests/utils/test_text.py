from unittest import TestCase
from utils.text import clean_name, get_url_for_teacher, generate_regex

from typing import List, Tuple

class TestCleanName(TestCase):
    def test_names_must_be_in_capital_letters (self) -> None:
      tests: List[Tuple[str, str]] = [
        ('jose', 'JOSE'),
        ('Jose', 'JOSE'),
        ('jOe', 'JOE'),
        ('Brenda', 'BRENDA'),
      ]
      
      for name, expected in tests:
        c_name: str = clean_name(name)
        self.assertEqual(c_name, expected)

    def test_special_characters_must_be_replaced(self) -> None:
      tests: List[Tuple[str, str]] = [
        ('josé', 'JOSE'),
        ('María', 'MARIA'),
        ('ÁNGEL', 'ANGEL'),
        ('pérez', 'PEREZ'),
        ('Niño', 'NINO')
      ]
      
      for name, expected in tests:
        c_name: str = clean_name(name)
        self.assertEqual(c_name, expected)
        
    def test_unnecessary_spaces_must_be_removed(self):
      tests: List[Tuple[str, str]] = [
        ('   josé', 'JOSE'),
        ('María    DE LOS ANGELES', 'MARIA DE LOS ANGELES'),
        (' ÁNGEL ', 'ANGEL'),
        (' pérez   ', 'PEREZ'),
        ('   Niño   ', 'NINO')
      ]
      
      for name, expected in tests:
        c_name: str = clean_name(name)
        self.assertEqual(c_name, expected)
        
class TestGetUrlForTeacher(TestCase):
  teacher_name: str = 'Susana Cuevas Escobar'
  teacher_profile_link: str = get_url_for_teacher(teacher_name)
  
  def test_should_be_a_link_to_the_teacher_dictionary(self):
    expected_prefix: str = 'https://foroupiicsa.net/diccionario/buscar/'
    
    self.assertTrue(self.teacher_profile_link.startswith(expected_prefix))
    
  def test_should_return_a_link_to_the_given_teachers_profile(self):
    tests: List[Tuple[str, str]] = [
      ('Susana Cuevas Escobar', 'https://foroupiicsa.net/diccionario/buscar/SUSANA+CUEVAS+ESCOBAR'),
      ('diana PéreZ Ledezma', 'https://foroupiicsa.net/diccionario/buscar/DIANA+PEREZ+LEDEZMA'),
      ('JOSEFINA NIÑO', 'https://foroupiicsa.net/diccionario/buscar/JOSEFINA+NINO')
    ]
    
    for teacher_name, expected in tests:
      teacher_profile_link: str = get_url_for_teacher(teacher_name)
      self.assertEqual(teacher_profile_link, expected)

class TestGenerateRegex(TestCase):
  def test_must_generate_a_regular_expression_from_given_sequence_parameters(self):
    sequence = Tuple[List[str], str, List[str], List[str]]
    tests: List[Tuple[sequence, str]] = [
      ((['4'], 'C', ['M'], ['4']), '^[4][C][M][4][0-9]+$'),
      ((['1'], 'A', ['V'], ['1']), '^[1][A][V][1][0-9]+$'),
      ((['2', '3'], 'N', ['M','V'], ['5']), '^[2|3][N][M|V][5][0-9]+$'),
      ((['3'], 'C', ['M','V'], ['6', '3']), '^[3][C][M|V][6|3][0-9]+$'),
      ((['3'], 'C', ['V'], ['2','3']), '^[3][C][V][2|3][0-9]+$'),
    ]
    
    for params, expected in tests:
      reg = generate_regex(params[0], params[1], params[2], params[3])
      self.assertEqual(reg, expected)    
  