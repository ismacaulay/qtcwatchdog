import os
import mock
from ddt import ddt, file_data, unpack
from pyfakefs import fake_filesystem_unittest

from qtcwatchdog import QtcWatchdog
from watcher import ProjectWatcher


@ddt
class TestUpdateFilesFeature(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        self.fs_observer = MockObserver(self.fs)
        self.project_settings = {}

        self.sleep_patcher = mock.patch('time.sleep')
        self.addCleanup(self.sleep_patcher.stop)
        self.mock_sleep = self.sleep_patcher.start()

        self.running_patcher = mock.patch('watcher.running')
        self.addCleanup(self.running_patcher.stop)
        self.mock_running = self.running_patcher.start()
        self.mock_running.side_effect = [True, False]

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

    def test_willAddInitialFilesToFilesFile(self):
        self.setup_project_directory()
        self.create_and_start_watchdog()

        self.verify_files_contains_paths(self.initial_files)

    def test_willNotAddQtcFilesToFilesFile(self):
        self.setup_project_directory()
        self.create_and_start_watchdog()

        self.verify_files_does_not_contain_path(self.files_file)
        self.verify_files_does_not_contain_path(self.includes_file)

    def test_willAddFilePathToFilesFile(self):
        self.setup_project_directory()
        self.create_and_start_watchdog()

        added_files = self.create_some_files()

        self.verify_files_contains_paths(added_files)

    def test_willRemoveFilePathFromFilesFile(self):
        self.setup_project_directory()
        self.create_and_start_watchdog()

        added_files = self.create_some_files()
        removed_files = [added_files.pop(0), self.initial_files.pop(2)]

        self.remove_some_files(removed_files)

        self.verify_files_does_not_contain_paths(removed_files)
        self.verify_files_contains_paths([added_files[0], self.initial_files[0]])

    @file_data('regex_test_cases.json')
    def test_willOnlyIncludeFilesThatMatchTheRegex(self, regex, files_to_add, expected_paths, expected_missing_paths):
        self.setup_project_directory()
        self.setup_project_files_regex(regex)
        self.create_and_start_watchdog()

        files_to_add = [os.path.join(self.project_settings['project_path'], f) for f in files_to_add]
        expected_paths = [os.path.join(self.project_settings['project_path'], f) for f in expected_paths]
        expected_missing_paths = [os.path.join(self.project_settings['project_path'], f) for f in expected_missing_paths]

        self.create_files(files_to_add)

        self.verify_files_contains_paths(expected_paths)
        self.verify_files_does_not_contain_paths(expected_missing_paths)

    def verify_files_contains_paths(self, paths):
        (files_contains, msg) = self.files_contains_paths(paths)
        self.assertTrue(files_contains, msg)

    def verify_files_does_not_contain_paths(self, paths):
        for f in paths:
            self.verify_files_does_not_contain_path(f)

    def verify_files_does_not_contain_path(self, path):
        (files_contains, msg) = self.files_contains_paths([path])
        self.assertFalse(files_contains, msg)

    def files_contains_paths(self, paths):
        with open(self.files_file) as f:
            lines = [f.strip('\n') for f in f.readlines()]
            for path in paths:
                if path not in lines:
                    return False, 'files contains path: {}'.format(path)
        return True, 'All paths in files file. paths: {}'.format(str(paths))

    def create_and_start_watchdog(self):
        watchdog = QtcWatchdog(self.project_settings)
        watchdog.start()

    def setup_project_directory(self):
        self.project_settings = {
            'project_name': 'watchdog',
            'project_path': os.path.relpath('/project/watchdog'),
            'files': {},
            'includes': {},
        }
        self.files_file = os.path.join(self.project_settings['project_path'], 'watchdog.files')
        self.includes_file = os.path.join(self.project_settings['project_path'], 'watchdog.includes')

        os.makedirs(self.project_settings['project_path'])
        self.fs.CreateFile(self.files_file)
        self.fs.CreateFile(self.includes_file)

        self.initial_files = [
            os.path.join(self.project_settings['project_path'], 'initial_file.txt'),
            os.path.join(self.project_settings['project_path'], 'initial_file.cxx'),
            os.path.join(self.project_settings['project_path'], 'initial_file.h'),
        ]
        for f in self.initial_files:
            self.fs.CreateFile(f)

    def setup_project_files_regex(self, regex):
        self.project_settings['files']['regex'] = regex

    def save_updater(self, project_path_arg, updater_arg):
        self.file_updater = updater_arg
        return ProjectWatcher(project_path_arg, updater_arg)

    def create_files(self, files):
        for f in files:
            self.fs_observer.create_file(f)
        self.file_updater.update_files()

    def create_some_files(self):
        files = [
            os.path.join(self.project_settings['project_path'], 'new_file1.txt'),
            os.path.join(self.project_settings['project_path'], 'new_file2.txt'),
            os.path.join(self.project_settings['project_path'], 'new_file3.txt'),
        ]
        self.create_files(files)
        return files

    def remove_some_files(self, files):
        for f in files:
            self.fs_observer.remove_file(f)
        self.file_updater.update_files()


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
