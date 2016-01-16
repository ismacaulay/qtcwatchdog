
import unittest
import mock

from file import QtcFile


class TestQtcFile(unittest.TestCase):

    @mock.patch('validator.RegexValidator')
    @mock.patch('file.FileWriter')
    def test_willCreateFileWriterWithPathOnCreation(self,  mock_writer_obj, mock_validator):
        mock_validator.is_valid.return_value = True

        QtcFile('path/to/file', mock_validator)

        mock_writer_obj.assert_called_with('path/to/file')

    @mock.patch('validator.RegexValidator')
    @mock.patch('file.FileWriter')
    def test_writeWillWriteIfPathIsValid(self, mock_writer_obj, mock_validator):
        mock_writer = mock_writer_obj.return_value
        mock_validator.is_valid.return_value = True

        patient = QtcFile('path/to/file', mock_validator)
        patient.write('hello/World')

        mock_writer.write.assert_called_with('hello/World')

    @mock.patch('validator.RegexValidator')
    @mock.patch('file.FileWriter')
    def test_writeWillNotWriteIfPathIsInvalid(self, mock_writer_obj, mock_validator):
        mock_writer = mock_writer_obj.return_value
        mock_validator.is_valid.return_value = False

        patient = QtcFile('path/to/file', mock_validator)
        patient.write('hello/World')

        mock_writer.write.assert_not_called()

    @mock.patch('validator.RegexValidator')
    @mock.patch('file.FileWriter')
    def test_removeWillRemovePathIsPathIsValid(self, mock_writer_obj, mock_validator):
        mock_writer = mock_writer_obj.return_value
        mock_validator.is_valid.return_value = True

        patient = QtcFile('path/to/file', mock_validator)
        patient.remove('hello/World')

        mock_writer.remove.assert_called_with('hello/World')

    @mock.patch('validator.RegexValidator')
    @mock.patch('file.FileWriter')
    def test_removeWillNotRemovePathIfPathIsInvalid(self, mock_writer_obj, mock_validator):
        mock_writer = mock_writer_obj.return_value
        mock_validator.is_valid.return_value = False

        patient = QtcFile('path/to/file', mock_validator)
        patient.remove('hello/World')

        mock_writer.remove.assert_not_called()

    @mock.patch('validator.RegexValidator')
    @mock.patch('file.FileWriter')
    def test_updateWithProcessCaches(self, mock_writer_obj, mock_validator):
        mock_writer = mock_writer_obj.return_value

        patient = QtcFile('path/to/file', mock_validator)
        patient.update()

        mock_writer.process_caches.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()

