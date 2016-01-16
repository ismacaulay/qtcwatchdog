
import unittest
import mock

from updater import QtcFile


class TestQtcFile(unittest.TestCase):

    @mock.patch('updater.FileWriter')
    @mock.patch('validator.RegexValidator')
    def test_writeWillWriteIfPathIsValid(self, mock_writer, mock_validator):
        mock_validator.is_valid.return_value = True

        patient = QtcFile(mock_writer, mock_validator)
        patient.write('hello/World')

        mock_writer.write.assert_called_with('hello/World')

    @mock.patch('updater.FileWriter')
    @mock.patch('validator.RegexValidator')
    def test_writeWillNotWriteIfPathIsInvalid(self, mock_writer, mock_validator):
        mock_validator.is_valid.return_value = False

        patient = QtcFile(mock_writer, mock_validator)
        patient.write('hello/World')

        mock_writer.write.assert_not_called()

    @mock.patch('updater.FileWriter')
    @mock.patch('validator.RegexValidator')
    def test_removeWillRemovePathIsPathIsValid(self, mock_writer, mock_validator):
        mock_validator.is_valid.return_value = True

        patient = QtcFile(mock_writer, mock_validator)
        patient.remove('hello/World')

        mock_writer.remove.assert_called_with('hello/World')

    @mock.patch('updater.FileWriter')
    @mock.patch('validator.RegexValidator')
    def test_removeWillNotRemovePathIfPathIsInvalid(self, mock_writer, mock_validator):
        mock_validator.is_valid.return_value = False

        patient = QtcFile(mock_writer, mock_validator)
        patient.remove('hello/World')

        mock_writer.remove.assert_not_called()

    @mock.patch('updater.FileWriter')
    @mock.patch('validator.RegexValidator')
    def test_updateWithProcessCaches(self, mock_writer, mock_validator):
        patient = QtcFile(mock_writer, mock_validator)
        patient.update()

        mock_writer.process_caches.assert_called_once_with()
