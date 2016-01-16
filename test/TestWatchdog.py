
import os
import mock
from pyfakefs import fake_filesystem_unittest
from qtcwatchdog import QtcWatchdog
from watcher import ProjectWatcher


class TestWatchdog(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def tearDown(self):
        pass

    @mock.patch('qtcwatchdog.ProjectWatcher')
    @mock.patch('watcher.Observer')
    @mock.patch('watcher.running')
    def test_willAddFilePathToFilesFile(self, mock_running, mock_observer_obj, project_watcher_obj):
        fs_observer = MockObserver(self.fs)
        mock_observer_obj.return_value = fs_observer
        mock_running.return_value = False

        project_watcher_obj.side_effect = save_updater
        settings = {
            'project_name': 'watchdog',
            'project_path': os.path.relpath('/project/watchdog'),

            'files': {
                'regex': '',
                'excludes': '',
            },

            'includes': {
                'regex': '',
                'excludes': '',
            },
        }

        os.makedirs(settings['project_path'])
        self.fs.CreateFile(os.path.relpath('/project/watchdog/watchdog.files'))
        self.fs.CreateFile(os.path.relpath('/project/watchdog/watchdog.includes'))

        watchdog = QtcWatchdog(settings)
        watchdog.start()

        fs_observer.create_file(os.path.relpath('/project/watchdog/test.txt'))
        fs_observer.create_file(os.path.relpath('/project/watchdog/test1.txt'))
        fs_observer.create_file(os.path.relpath('/project/watchdog/test2.txt'))
        fs_observer.create_file(os.path.relpath('/project/watchdog/test3.txt'))

        updater.update_files()

        self.assertTrue(self.files_contains_path(os.path.relpath('/project/watchdog/test.txt')))
        self.assertTrue(self.files_contains_path(os.path.relpath('/project/watchdog/test1.txt')))
        self.assertTrue(self.files_contains_path(os.path.relpath('/project/watchdog/test2.txt')))
        self.assertTrue(self.files_contains_path(os.path.relpath('/project/watchdog/test3.txt')))

    @staticmethod
    def files_contains_path(path):
        with open(os.path.relpath('/project/watchdog/watchdog.files')) as f:
            lines = f.readlines()
            for line in lines:
                if path in line:
                    return True
        return False


def save_updater(proj_path_arg, updater_arg):
    global updater
    updater = updater_arg
    return ProjectWatcher(proj_path_arg, updater_arg)


class MockObserver(object):
    def __init__(self, fs):
        self.fs = fs
        self.event_handler = None

    def schedule(self, event_handler, project_path, recursive):
        self.event_handler = event_handler

    def start(self):
        pass

    def stop(self):
        pass

    def join(self):
        pass

    def create_file(self, path):
        self.fs.CreateFile(path)
        event = mock.MagicMock()
        event.src_path = path
        event.is_directory = False
        self.event_handler.on_created(event)


