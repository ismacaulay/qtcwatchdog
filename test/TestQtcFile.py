
import unittest
import mock

from updater import QtcFile, FileWriter
from validator import RegexValidator


class TestQtcFile(unittest.TestCase):

    def test_writeWillWriteIfPathIsValid(self):
        writer = mock.create_autospec(FileWriter)
        validator = mock.create_autospec(RegexValidator)
        validator.is_valid.return_value = True

        patient = QtcFile(writer, validator)
        patient.write('hello/World')

        writer.write.assert_called_with('hello/World')

    def test_writeWillNotWriteIfPathIsInvalid(self):
        writer = mock.create_autospec(FileWriter)
        validator = mock.create_autospec(RegexValidator)
        validator.is_valid.return_value = False

        patient = QtcFile(writer, validator)
        patient.write('hello/World')

        writer.write.assert_not_called()

    def test_removeWillRemovePathIsPathIsValid(self):
        writer = mock.create_autospec(FileWriter)
        validator = mock.create_autospec(RegexValidator)
        validator.is_valid.return_value = True

        patient = QtcFile(writer, validator)
        patient.remove('hello/World')

        writer.remove.assert_called_with('hello/World')

    def test_removeWillNotRemovePathIfPathIsInvalid(self):
        writer = mock.create_autospec(FileWriter)
        validator = mock.create_autospec(RegexValidator)
        validator.is_valid.return_value = False

        patient = QtcFile(writer, validator)
        patient.remove('hello/World')

        writer.remove.assert_not_called()

