import os, mock
from pyfakefs import fake_filesystem_unittest
from observer import FakeObserver

from qtcwatchdog import QtcWatchdog
from watcher import ProjectWatcher


class WatchdogAcceptanceTest(fake_filesystem_unittest.TestCase):
    def setUp(self):
        print 'SETTING UP'
        self.setUpPyfakefs()

        self.fs_observer = FakeObserver(self.fs)
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

    def create_and_start_watchdog(self):
        self.watchdog = QtcWatchdog(self.project_settings)
        self.watchdog.start()

    def save_updater(self, project_path_arg, updater_arg):
        self.file_updater = updater_arg
        return ProjectWatcher(project_path_arg, updater_arg)