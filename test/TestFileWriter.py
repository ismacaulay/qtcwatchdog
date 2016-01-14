import threading
import unittest, mock

from updater import FileWriter, InvalidPathError


class TestFileWriter(unittest.TestCase):

    def setUp(self):
        self.is_file_patcher = mock.patch('os.path.isfile')
        self.addCleanup(self.is_file_patcher.stop)
        self.open_patcher = mock.patch('updater.open', mock.mock_open())
        self.addCleanup(self.open_patcher.stop)
        self.lock_patcher = mock.patch('threading.Lock')
        self.addCleanup(self.lock_patcher.stop)
        self.timer_patcher = mock.patch('threading.Timer')
        self.addCleanup(self.timer_patcher.stop)

        self.mock_isfile = self.is_file_patcher.start()
        self.mock_open = self.open_patcher.start()
        self.mock_lock_obj = self.lock_patcher.start()
        self.mock_timer_obj = self.timer_patcher.start()
        self.mock_timer_obj.side_effect = self.save_timer_callback

    def create_patient(self, path='', clear=True):
        patient = FileWriter(path)
        if clear:
            self.clear_mocks()
        return patient

    def clear_mocks(self):
        self.mock_isfile.reset_mock()
        self.mock_open.reset_mock()
        self.mock_timer_obj.reset_mock()
        self.mock_timer_obj.reset_mock()

    def save_timer_callback(self, *args, **kwargs):
        self.process_paths_func = kwargs['function']
        return mock.DEFAULT

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

    def test_willTruncateFileOnCreation(self):
        self.create_patient('hello/World', clear=False)

        self.mock_open.assert_called_with('hello/World', 'r+')
        handle = self.mock_open()
        handle.truncate.assert_called_with()

    def test_willCreateTimerWithCorrectIntervalOnCreation(self):
        self.create_patient(clear=False)
        self.mock_timer_obj.assert_called_with(interval=1.0, function=mock.ANY)

    def test_willStartTimerOnCreation(self):
        mock_timer = self.mock_timer_obj.return_value

        self.create_patient(clear=False)

        mock_timer.start.assert_called_once_with()

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

        self.create_patient()
        self.process_paths_func()

        mock_lock.acquire.assert_called_once_with()
        mock_lock.release.assert_called_once_with()

    def test_willOpenCorrectFileWhenProcessingPaths(self):
        expected_file_path = 'hello/world.txt'
        self.create_patient(expected_file_path)

        self.process_paths_func()

        self.mock_open.assert_called_once_with(expected_file_path, 'r+')

    def test_willStartTimerAfterProcessingPaths(self):
        mock_timer = self.mock_timer_obj.return_value

        self.create_patient()
        self.process_paths_func()

        mock_timer.start.assert_called_once_with()

    def test_willWriteAllPathsToFileWhenProcessingPaths(self):
        patient = self.create_patient()

        patient.write('helloWorld.txt')
        patient.write('path/to/helloWorld.txt')
        patient.write('this/is/helloWorld')

        self.process_paths_func()

        mock_file = self.mock_open()
        mock_file.write.assert_has_calls([
            mock.call('helloWorld.txt\n'),
            mock.call('path/to/helloWorld.txt\n'),
            mock.call('this/is/helloWorld\n')
        ], any_order=True)

    def test_willClearWritePathCacheWhenProcessingPaths(self):
        patient = self.create_patient()

        patient.write('helloWorld.txt')
        self.process_paths_func()

        self.clear_mocks()
        self.process_paths_func()
        mock_file = self.mock_open()
        mock_file.write.assert_not_called()

    def test_willRemovePathFromCacheBeforeProcessingPaths(self):
        patient = self.create_patient()

        patient.write('helloWorld')
        patient.remove('helloWorld')

        self.process_paths_func()

        mock_file = self.mock_open()
        mock_file.write.assert_not_called()

    def test_willRemovePathFromFile(self):
        patient = self.create_patient()
        mock_file = self.mock_open()
        data = self.file_data()
        mock_file.readlines.return_value = data

        patient.remove('remove/this/path')
        self.process_paths_func()

        data.remove('remove/this/path\n')
        mock_file.write.assert_has_calls(self.covert_to_call_list(data), any_order=True)

    def test_willClearRemoveCacheWhenProcessingPaths(self):
        patient = self.create_patient()
        mock_file = self.mock_open()
        data = self.file_data()
        mock_file.readlines.return_value = data

        patient.remove('remove/this/path')
        self.process_paths_func()

        self.clear_mocks()
        mock_file.reset_mock()
        mock_file.readlines.return_value = data
        self.process_paths_func()
        mock_file.write.assert_has_calls(self.covert_to_call_list(data), any_order=True)

    def test_willTruncateFileAfterWritingFile(self):
        patient = self.create_patient()
        mock_file = self.mock_open()
        data = self.file_data()
        mock_file.readlines.return_value = data

        patient.remove('remove/this/path')
        self.process_paths_func()

        mock_file.truncate.assert_called_once_with()

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

