import os, mock
from pyfakefs import fake_filesystem_unittest
from observer import FakeObserver

from qtcwatchdog.qtcwatchdog import QtcWatchdog
from qtcwatchdog.watcher import ProjectWatcher


class WatchdogAcceptanceTest(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        self.fs_observer = FakeObserver(self.fs)
        self.project_settings = {}

        self.sleep_patcher = mock.patch('time.sleep')
        self.addCleanup(self.sleep_patcher.stop)
        self.mock_sleep = self.sleep_patcher.start()

        self.running_patcher = mock.patch('qtcwatchdog.watcher.running')
        self.addCleanup(self.running_patcher.stop)
        self.mock_running = self.running_patcher.start()
        self.mock_running.side_effect = [True, False]

        self.observer_patcher = mock.patch('qtcwatchdog.watcher.Observer')
        self.addCleanup(self.observer_patcher.stop)
        self.mock_observer = self.observer_patcher.start()
        self.mock_observer.return_value = self.fs_observer

        self.watcher_patcher = mock.patch('qtcwatchdog.qtcwatchdog.ProjectWatcher')
        self.addCleanup(self.watcher_patcher.stop)
        self.mock_watcher = self.watcher_patcher.start()
        self.mock_watcher.side_effect = self.save_updater

        self.setup_project_directory()

    def tearDown(self):
        pass

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

        self.initial_directories = [
            os.path.join(self.project_settings['project_path'], 'directory1'),
            os.path.join(self.project_settings['project_path'], 'directory2'),
            os.path.join(self.project_settings['project_path'], 'directory3'),
        ]
        for d in self.initial_directories:
            self.fs.CreateDirectory(d)

    def create_and_start_watchdog(self):
        self.watchdog = QtcWatchdog(self.project_settings)
        self.watchdog.start()

    def save_updater(self, project_path_arg, updater_arg):
        self.file_updater = updater_arg
        return ProjectWatcher(project_path_arg, updater_arg)

    def file_contains_paths(self, file_path, paths=[]):
        with open(file_path) as f:
            lines = [f.strip('\n') for f in f.readlines()]
            for path in paths:
                if path not in lines:
                    return False, '{} does not contain path {}'.format(file_path, path)
        return True, 'All paths in {}. paths: {}'.format(file_path, str(paths))

