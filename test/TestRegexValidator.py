
import unittest

from validator import RegexValidator


class TestRegexValidator(unittest.TestCase):

    def test_isValidWhenMatchingAndExcluding(self):
        patient = RegexValidator(pattern='.*world', excludes='hello.*')

        self.assertTrue(patient.is_valid('world'))
        self.assertTrue(patient.is_valid('goodbye world'))
        self.assertFalse(patient.is_valid('hello world'))

    def test_isValidWhenMatchingRegex(self):
        patient = RegexValidator(pattern='(.*world|hello.*)', excludes='')

        self.assertTrue(patient.is_valid('helloWorld'))
        self.assertTrue(patient.is_valid('goodbye world'))
        self.assertFalse(patient.is_valid('this wont match'))

    def test_isValidOnlyWhenPatternMatches(self):
        patient = RegexValidator(pattern='helloWorld', excludes='')

        self.assertTrue(patient.is_valid('helloWorld'))
        self.assertFalse(patient.is_valid('goodbyeWorld'))

    def test_emptyPatternAndExcludesIsAlwaysValid(self):
        patient = RegexValidator(pattern='', excludes='')

        self.assertTrue(patient.is_valid('hello world this is a string'))

if __name__ == '__main__':
    unittest.main()

