import os
import unittest
from ddt import ddt, file_data

from acceptance.harness.acceptance_test import WatchdogAcceptanceTest


@ddt
class TestUpdateIncludesFeature(WatchdogAcceptanceTest):
    def test_willAddProjectDirectoriesToIncludesFile(self):
        self.create_and_start_watchdog()

        self.verify_includes_contains_paths(self.initial_directories)

    def test_willAddProjectDirectoryToIncludesFile(self):
        self.create_and_start_watchdog()

        self.verify_includes_contains_paths([self.project_settings['project_path']])

    def test_willAddCreatedDirectoryToIncludesFile(self):
        self.create_and_start_watchdog()

        added_directories = self.create_some_directories()

        self.verify_includes_contains_paths(added_directories)

    def test_willRemoveDirectoryFromIncludesFile(self):
        self.create_and_start_watchdog()

        added_directories = self.create_some_directories()
        removed_directories = [added_directories.pop(1), self.initial_directories.pop(0)]

        self.remove_some_directories(removed_directories)

        self.verify_includes_does_not_contain_paths(removed_directories)
        self.verify_includes_contains_paths([added_directories[0], self.initial_directories[0]])

    # todo: moved tests

    @file_data('test_data/includes_regex_td.json')
    def test_willOnlyIncludeDirectoriesThatMatchTheRegex(self, regex, dirs_to_add, expected_paths, expected_missing_paths):
        self.setup_project_includes_regex(regex)
        self.create_and_start_watchdog()

        dirs_to_add = [os.path.join(self.project_settings['project_path'], *d.split('/')) for d in dirs_to_add]
        expected_paths = [os.path.join(self.project_settings['project_path'], *d.split('/')) for d in expected_paths]
        expected_missing_paths = [os.path.join(self.project_settings['project_path'], *d.split('/')) for d in expected_missing_paths]

        self.create_directories(dirs_to_add)

        self.verify_includes_contains_paths(expected_paths)
        self.verify_includes_does_not_contain_paths(expected_missing_paths)

    # todo: excludes tests

    def verify_includes_contains_paths(self, paths):
        (contains, msg) = self.file_contains_paths(self.includes_file, paths)
        self.assertTrue(contains, msg)

    def verify_includes_does_not_contain_paths(self, paths):
        for d in paths:
            self.verify_includes_does_not_contain_path(d)

    def verify_includes_does_not_contain_path(self, path):
        (contains, msg) = self.file_contains_paths(self.includes_file, [path])
        self.assertFalse(contains, msg)

    def setup_project_includes_regex(self, regex):
        self.project_settings['includes']['regex'] = regex

    def create_some_directories(self):
        directories = [
            os.path.join(self.project_settings['project_path'], 'new_directory1'),
            os.path.join(self.project_settings['project_path'], 'new_directory1', 'new_subdirectory'),
            os.path.join(self.project_settings['project_path'], 'new_directory2'),
            os.path.join(self.project_settings['project_path'], 'new_directory2', 'new_subdirectory2'),
        ]
        self.create_directories(directories)
        return directories

    def remove_some_directories(self, directories):
        for d in directories:
            self.fs_observer.remove_directory(d)
        self.file_updater.update_files()

    def create_directories(self, dirs):
        for d in dirs:
            self.fs_observer.create_directory(d)
        self.file_updater.update_files()

if __name__ == '__main__':
    unittest.main()
