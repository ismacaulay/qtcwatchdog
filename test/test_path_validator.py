
import unittest
from validator import PathValidator

class TestPathValidator(unittest.TestCase):
   def setUp(self):
      self.file_patterns = ['*.py', '*.cpp', '*.h', 'helloWorld', 'wscript']
      self.exclude_dirs = ['excluded', 'also_excluded']
      self.patient = PathValidator(self.file_patterns, self.exclude_dirs)

   def test_validate_path_extension(self):
      self.assertEqual(self.patient.validate_path('hello/world.h'), 'hello/world.h')
      self.assertEqual(self.patient.validate_path('hello/world.cpp'), 'hello/world.cpp')
      self.assertEqual(self.patient.validate_path('hello/world.py'), 'hello/world.py')
      self.assertEqual(self.patient.validate_path('hello/world.txt'), None)

   def test_validate_file_name(self):
      self.assertEqual(self.patient.validate_path('valid/helloWorld'), 'valid/helloWorld')
      self.assertEqual(self.patient.validate_path('valid/wscript'), 'valid/wscript')
      self.assertEqual(self.patient.validate_path('valid/notIncluded'), None)

   def test_remove_excluded_directories(self):
      self.assertEqual(self.patient.validate_path('hello/excluded/world.py'), None)
      self.assertEqual(self.patient.validate_path('hello/also_excluded/world.cpp'), None)

   def test_validate_list(self):
      data = ['this/is/valid.cpp', 'this/is/valid.h', 'this/is/excluded/invalid.py', 'this/is/also_excluded', 'helloWorld']
      self.assertEqual(self.patient.validate_list(data), ['this/is/valid.cpp', 'this/is/valid.h', 'helloWorld']);

   def test_validate_path_with_empty_patterns_and_excludes(self):
      patient = PathValidator([], [])
      self.assertEqual(patient.validate_path('hello.txt'), 'hello.txt')
