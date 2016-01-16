import os, unittest
import mock
from pyfakefs import fake_filesystem_unittest
from qtcwatchdog import QtcWatchdog
from watcher import ProjectWatcher


class TestUpdateFilesFeature(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        self.fs_observer = MockObserver(self.fs)
        self.project_settings = {}

        self.running_patcher = mock.patch('watcher.running')
        self.addCleanup(self.running_patcher.stop)
        self.mock_running = self.running_patcher.start()
        self.mock_running.return_value = False

        self.observer_patcher = mock.patch('watcher.Observer')
        self.addCleanup(self.observer_patcher.stop)
        self.mock_observer = self.observer_patcher.start()
        self.mock_observer.return_value = self.fs_observer

        self.watcher_patcher = mock.patch('qtcwatchdog.ProjectWatcher')
        self.addCleanup(self.watcher_patcher.stop)
        self.mock_watcher = self.watcher_patcher.start()
        self.mock_watcher.side_effect = self.save_updater

    def tearDown(self):
        pass

    def test_willAddFilePathToFilesFile(self):
        self.setup_project_directory()

        watchdog = QtcWatchdog(self.project_settings)
        watchdog.start()

        added_files = self.create_some_files()

        (files_contains, msg) = self.files_contains_paths(added_files)
        self.assertTrue(files_contains, msg)
        (files_contains, msg) = self.files_contains_paths(self.initial_files)
        self.assertTrue(files_contains, msg)

    def test_WillRemoveFilePathFromFilesFile(self):
        self.setup_project_directory()

        watchdog = QtcWatchdog(self.project_settings)
        watchdog.start()

        added_files = self.create_some_files()

        removed_added_file = added_files.pop(0)
        removed_initial_file = self.initial_files.pop(2)

        self.remove_some_files([removed_added_file, removed_initial_file])

        (files_contains, msg) = self.files_contains_paths([removed_added_file])
        self.assertFalse(files_contains, msg)
        (files_contains, msg) = self.files_contains_paths([removed_initial_file])
        self.assertFalse(files_contains, msg)
        (files_contains, msg) = self.files_contains_paths([added_files[0], self.initial_files[0]])
        self.assertTrue(files_contains, msg)

    def setup_project_directory(self):
        self.project_settings = {
            'project_name': 'watchdog',
            'project_path': os.path.relpath('/project/watchdog'),
        }

        os.makedirs(self.project_settings['project_path'])
        self.fs.CreateFile(os.path.relpath('/project/watchdog/watchdog.files'))
        self.fs.CreateFile(os.path.relpath('/project/watchdog/watchdog.includes'))

        self.initial_files = [
            os.path.relpath('/project/watchdog/initial_file1.txt'),
            os.path.relpath('/project/watchdog/initial_file2.txt'),
            os.path.relpath('/project/watchdog/initial_file3.txt'),
        ]
        self.create_files(self.initial_files)

    def save_updater(self, project_path_arg, updater_arg):
        self.file_updater = updater_arg
        return ProjectWatcher(project_path_arg, updater_arg)

    @staticmethod
    def files_contains_paths(paths):
        with open(os.path.relpath('/project/watchdog/watchdog.files')) as f:
            lines = [f.strip('\n') for f in f.readlines()]
            for path in paths:
                if path not in lines:
                    return False, path
        return True, ''

    def create_some_files(self):
        files = [
            os.path.relpath('/project/watchdog/new_file1.txt'),
            os.path.relpath('/project/watchdog/new_file2.txt'),
            os.path.relpath('/project/watchdog/new_file3.txt'),
        ]
        for f in files:
            self.fs_observer.create_file(f)
        self.file_updater.update_files()
        return files

    def remove_some_files(self, files):
        for f in files:
            self.fs_observer.remove_file(f)
        self.file_updater.update_files()

    def create_files(self, files):
        for f in files:
            self.fs.CreateFile(f)


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
        self.event_handler.on_created(self.create_event(src_path=path))

    def remove_file(self, path):
        self.fs.RemoveObject(path)
        self.event_handler.on_deleted(self.create_event(src_path=path))

    @staticmethod
    def create_event(src_path='', dest_path='', is_directory=False):
        event = mock.MagicMock()
        event.src_path = src_path
        event.dest_path = dest_path
        event.is_directory = is_directory
        return event
