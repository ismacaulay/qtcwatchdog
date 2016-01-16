
import unittest
import mock

from updater import QtcUpdater


class TestQtcUpdater(unittest.TestCase):

    @mock.patch('file.QtcFile')
    @mock.patch('file.QtcFile')
    def test_addFileAddsTheFileToTheFilesFile(self, mock_files, mock_includes):
        patient = QtcUpdater(mock_files, mock_includes)
        patient.add('hello/World', is_dir=False)

        mock_files.write.assert_called_with('hello/World')

    @mock.patch('file.QtcFile')
    @mock.patch('file.QtcFile')
    def test_addDirAddsTheDirToTheIncludesFile(self, mock_files, mock_includes):
        patient = QtcUpdater(mock_files, mock_includes)
        patient.add('hello/World', is_dir=True)

        mock_includes.write.assert_called_with('hello/World')

    @mock.patch('file.QtcFile')
    @mock.patch('file.QtcFile')
    def test_removeFileRemovesTheFileFromTheFilesFile(self, mock_files, mock_includes):
        patient = QtcUpdater(mock_files, mock_includes)
        patient.remove('hello/World', is_dir=False)

        mock_files.remove.assert_called_with('hello/World')

    @mock.patch('file.QtcFile')
    @mock.patch('file.QtcFile')
    def test_removeDirRemovesTheFileFromTheIncludesFile(self, mock_files, mock_includes):
        patient = QtcUpdater(mock_files, mock_includes)
        patient.remove('hello/World', is_dir=True)

        mock_includes.remove.assert_called_with('hello/World')

    @mock.patch('file.QtcFile')
    @mock.patch('file.QtcFile')
    def test_moveWillRemoveSrcAndAddDestToFilesFile(self, mock_files, mock_includes):
        patient = QtcUpdater(mock_files, mock_includes)
        patient.move('hello/World', 'world/Hello', is_dir=False)

        mock_files.remove.assert_called_with('hello/World')
        mock_files.write.assert_called_with('world/Hello')

    @mock.patch('file.QtcFile')
    @mock.patch('file.QtcFile')
    def test_moveWillRemoveSrcAndAddDestToIncludesFile(self, mock_files, mock_includes):
        patient = QtcUpdater(mock_files, mock_includes)
        patient.move('hello/World', 'world/Hello', is_dir=True)

        mock_includes.remove.assert_called_with('hello/World')
        mock_includes.write.assert_called_with('world/Hello')

    @mock.patch('file.QtcFile')
    @mock.patch('file.QtcFile')
    def test_willUpdateBothFilesAndIncludes(self, mock_files, mock_includes):
        patient = QtcUpdater(mock_files, mock_includes)
        patient.update_files()

        mock_files.update.assert_called_once_with()
        mock_includes.update.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()

