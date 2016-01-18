import unittest
from qtcwatchdog.validator import FilesPathValidator


class TestFilesPathValidator(unittest.TestCase):
    def test_excludedPathsAreInvalid(self):
        excluded_paths = ['hello', 'world']

        patient = FilesPathValidator(excluded_paths, '', '')

        self.assertFalse(patient.is_valid('hello'))
        self.assertFalse(patient.is_valid('world'))

    def test_excludedPathsAreInvalidEvenIfTheyMatchTheRegex(self):
        excluded_paths = ['hello', 'world']

        patient = FilesPathValidator(excluded_paths, 'hello*', '')

        self.assertFalse(patient.is_valid('hello'))
        self.assertTrue(patient.is_valid('helloWorld'))

if __name__ == '__main__':
    unittest.main()
