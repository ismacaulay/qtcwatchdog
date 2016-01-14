
import unittest, mock
from copy import deepcopy

from updater import FileWriter, InvalidPathError


class TestFileWriter(unittest.TestCase):

    def test_willRaiseExceptionIfPathIsInvalid(self):
        def create_patient(path):
            with mock.patch('updater.open', mock.mock_open(), create=True):
                return FileWriter(path)

        with mock.patch('os.path.isfile', return_value=False) as mock_isfile:
            self.assertRaises(InvalidPathError, create_patient, 'this/is/a/path')
            mock_isfile.assert_called_with('this/is/a/path')

    def test_willNotRaiseExceptionIfPathIsValid(self):
        try:
            create_patient('helloWorld')
        except InvalidPathError:
            self.fail('InvalidPathError raised when it should not be.')

    def test_willTruncateFileOnCreation(self):
        mock_open = mock.mock_open()

        with mock.patch('os.path.isfile', return_value=True):
            with mock.patch('updater.open', mock_open, create=True):
                FileWriter('hello/World')

        mock_open.assert_called_with('hello/World', 'r+')
        handle = mock_open()
        handle.truncate.assert_called_with()

    @mock.patch('threading.Timer')
    def test_willCreateTimerWithCorrectIntervalOnCreation(self, mock_timer_object):
        create_patient('helloWorld')
        mock_timer_object.assert_called_with(interval=1.0, function=mock.ANY)

    @mock.patch('threading.Lock')
    def test_willLockAndUnlockMutexOnWrite(self, mock_lock_object):
        mock_lock = mock_lock_object.return_value
        patient = create_patient('helloWorld')

        patient.write('hello')
        mock_lock.acquire.assert_called_once_with()
        mock_lock.release.assert_called_once_with()

    @mock.patch('threading.Timer')
    @mock.patch('threading.Lock')
    def test_willLockAndUnlockMutexWhenProcessingPaths(self, mock_lock_obj, mock_timer_obj):
        def save_function_arg(*args, **kwargs):
            global timer_function
            timer_function = kwargs['function']

        mock_lock = mock_lock_obj.return_value
        mock_timer_obj.side_effect = save_function_arg

        create_patient('helloWorld')
        timer_function()

        mock_lock.acquire.assert_called_once_with()
        mock_lock.release.assert_called_once_with()


def create_patient(path):
    with mock.patch('os.path.isfile', return_value=True):
        with mock.patch('updater.open', mock.mock_open(), create=True):
            return FileWriter(path)
