import unittest, mock

from file import FileWriter, InvalidPathError


class TestFileWriter(unittest.TestCase):

    def setUp(self):
        self.isfile_patcher = mock.patch('os.path.isfile')
        self.addCleanup(self.isfile_patcher.stop)
        self.open_patcher = mock.patch('__builtin__.open', mock.mock_open())
        self.addCleanup(self.open_patcher.stop)
        self.lock_patcher = mock.patch('threading.Lock')
        self.addCleanup(self.lock_patcher.stop)

        self.mock_isfile = self.isfile_patcher.start()
        self.mock_open = self.open_patcher.start()
        self.mock_lock_obj = self.lock_patcher.start()

    def create_patient(self, path='', clear=True):
        patient = FileWriter(path)
        if clear:
            self.clear_mocks()
        return patient

    def clear_mocks(self):
        self.mock_isfile.reset_mock()
        self.mock_open.reset_mock()
        self.mock_lock_obj.reset_mock()

    def test_willRaiseExceptionIfPathIsInvalid(self):
        self.mock_isfile.return_value = False

        self.assertRaises(InvalidPathError, self.create_patient, 'this/is/a/path', False)

        self.mock_isfile.assert_called_with('this/is/a/path')

    def test_willNotRaiseExceptionIfPathIsValid(self):
        try:
            self.mock_isfile.return_value = True
            self.create_patient('helloWorld', clear=False)
        except InvalidPathError:
            self.fail('InvalidPathError raised when it should not be.')

    def test_willLockAndUnlockMutexOnWrite(self):
        mock_lock = self.mock_lock_obj.return_value

        patient = self.create_patient()
        patient.write('hello')

        mock_lock.acquire.assert_called_once_with()
        mock_lock.release.assert_called_once_with()

    def test_willLockAndUnlockMutexOnRemove(self):
        mock_lock = self.mock_lock_obj.return_value

        patient = self.create_patient()
        patient.remove('hello')

        mock_lock.acquire.assert_called_once_with()
        mock_lock.release.assert_called_once_with()

    def test_willLockAndUnlockMutexWhenProcessingPaths(self):
        mock_lock = self.mock_lock_obj.return_value

        patient = self.create_patient()
        patient.process_caches()

        mock_lock.acquire.assert_called_once_with()
        mock_lock.release.assert_called_once_with()

    def test_willOpenCorrectFileWhenProcessingPaths(self):
        expected_file_path = 'hello/world.txt'
        patient = self.create_patient(expected_file_path)
        patient.write('helloWorld')

        patient.process_caches()

        self.mock_open.assert_called_once_with(expected_file_path, 'r+')

    def test_willWriteAllPathsToFileWhenProcessingPaths(self):
        patient = self.create_patient()

        patient.write('helloWorld.txt')
        patient.write('path/to/helloWorld.txt')
        patient.write('this/is/helloWorld')

        patient.process_caches()

        mock_file = self.mock_open()
        self.assertEqual(mock_file.write.call_count, 3)
        mock_file.write.assert_has_calls([
            mock.call('helloWorld.txt\n'),
            mock.call('path/to/helloWorld.txt\n'),
            mock.call('this/is/helloWorld\n')
        ], any_order=True)

    def test_willClearWritePathCacheWhenProcessingPaths(self):
        patient = self.create_patient()

        patient.write('helloWorld.txt')
        patient.process_caches()
        self.clear_mocks()

        patient.process_caches()
        self.mock_open.assert_not_called()

    def test_willRemovePathFromCacheBeforeProcessingPaths(self):
        patient = self.create_patient()

        patient.write('helloWorld')
        patient.remove('helloWorld')

        patient.process_caches()

        mock_file = self.mock_open()
        mock_file.write.assert_not_called()

    def test_willRemovePathFromFile(self):
        patient = self.create_patient()
        mock_file = self.mock_open()
        data = self.file_data()
        mock_file.readlines.return_value = data

        patient.remove('remove/this/path')
        patient.process_caches()

        data.remove('remove/this/path\n')
        self.assertEqual(mock_file.write.call_count, len(data))
        mock_file.write.assert_has_calls(self.covert_to_call_list(data), any_order=True)

    def test_willClearRemoveCacheWhenProcessingPaths(self):
        patient = self.create_patient()

        patient.remove('remove/this/path')
        patient.process_caches()
        self.clear_mocks()

        patient.process_caches()
        self.mock_open.assert_not_called()

    def test_willTruncateFileAfterWritingFile(self):
        patient = self.create_patient()
        mock_file = self.mock_open()
        data = self.file_data()
        mock_file.readlines.return_value = data

        patient.remove('remove/this/path')
        patient.process_caches()

        mock_file.truncate.assert_called_once_with()

    def test_willSeekBackToStartOfFileAfterReadingLines(self):
        patient = self.create_patient()
        mock_file = self.mock_open()

        patient.remove('remove/this/path')
        patient.process_caches()

        mock_file.seek.assert_called_once_with(0)

    def test_willNotModifyFileIfCachesAreEmpty(self):
        patient = self.create_patient()
        patient.process_caches()

        self.mock_open.assert_not_called()

    def file_data(self):
        return [
            'hello/world.txt\n',
            'this/is/a/test.cxx\n',
            'remove/this/path\n',
            'path1.txt\n',
            'path2.txt\n',
            'path3.txt\n',
            'path4.txt\n',
            'path5.txt\n',
        ]

    def covert_to_call_list(self, list_to_convert):
        calls = []
        for l in list_to_convert:
            calls.append(mock.call(l))
        return calls


if __name__ == '__main__':
    unittest.main()
