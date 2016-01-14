
import unittest
import mock

from updater import QtcUpdater, QtcFile


class TestQtcUpdater(unittest.TestCase):

    def test_addFileAddsTheFileToTheFilesFile(self):
        files_file = mock.create_autospec(QtcFile)
        includes_file = mock.create_autospec(QtcFile)

        patient = QtcUpdater(files=files_file, includes=includes_file)
        patient.add('hello/World', is_dir=False)

        files_file.write.assert_called_with('hello/World')

    def test_addDirAddsTheDirToTheIncludesFile(self):
        files_file = mock.create_autospec(QtcFile)
        includes_file = mock.create_autospec(QtcFile)

        patient = QtcUpdater(files=files_file, includes=includes_file)
        patient.add('hello/World', is_dir=True)

        includes_file.write.assert_called_with('hello/World')

    def test_removeFileRemovesTheFileFromTheFilesFile(self):
        files_file = mock.create_autospec(QtcFile)
        includes_file = mock.create_autospec(QtcFile)

        patient = QtcUpdater(files=files_file, includes=includes_file)
        patient.remove('hello/World', is_dir=False)

        files_file.remove.assert_called_with('hello/World')

    def test_removeDirRemovesTheFileFromTheIncludesFile(self):
        files_file = mock.create_autospec(QtcFile)
        includes_file = mock.create_autospec(QtcFile)

        patient = QtcUpdater(files=files_file, includes=includes_file)
        patient.remove('hello/World', is_dir=True)

        includes_file.remove.assert_called_with('hello/World')

    def test_moveWillRemoveSrcAndAddDestToFilesFile(self):
        files_file = mock.create_autospec(QtcFile)
        includes_file = mock.create_autospec(QtcFile)

        patient = QtcUpdater(files=files_file, includes=includes_file)
        patient.move('hello/World', 'world/Hello', is_dir=False)

        files_file.remove.assert_called_with('hello/World')
        files_file.write.assert_called_with('world/Hello')

    def test_moveWillRemoveSrcAndAddDestToIncludesFile(self):
        files_file = mock.create_autospec(QtcFile)
        includes_file = mock.create_autospec(QtcFile)

        patient = QtcUpdater(files=files_file, includes=includes_file)
        patient.move('hello/World', 'world/Hello', is_dir=True)

        includes_file.remove.assert_called_with('hello/World')
        includes_file.write.assert_called_with('world/Hello')
