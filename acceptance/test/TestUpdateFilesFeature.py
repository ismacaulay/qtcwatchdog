import os
import unittest
from ddt import ddt, file_data

from acceptance.harness.acceptance_test import WatchdogAcceptanceTest


@ddt
class TestUpdateFilesFeature(WatchdogAcceptanceTest):
    def test_willAddInitialFilesToFilesFile(self):
        self.create_and_start_watchdog()

        self.verify_files_contains_paths(self.initial_files)

    def test_willNotAddQtcFilesToFilesFile(self):
        self.create_and_start_watchdog()

        self.verify_files_does_not_contain_path(self.files_file)
        self.verify_files_does_not_contain_path (self.includes_file)

    def test_willAddFilePathToFilesFile(self):
        self.create_and_start_watchdog()

        added_files = self.create_some_files()

        self.verify_files_contains_paths(added_files)

    def test_willRemoveFilePathFromFilesFile(self):
        self.create_and_start_watchdog()

        added_files = self.create_some_files()
        removed_files = [added_files.pop(0), self.initial_files.pop(2)]

        self.remove_some_files(removed_files)

        self.verify_files_does_not_contain_paths(removed_files)
        self.verify_files_contains_paths([added_files[0], self.initial_files[0]])

    @file_data('test_data/files_regex_td.json')
    def test_willOnlyIncludeFilesThatMatchTheRegex(self, regex, files_to_add, expected, expected_missing):
        self.setup_project_files_regex(regex)
        self.create_and_start_watchdog()

        files_to_add = [os.path.join(self.project_settings['project_path'], f) for f in files_to_add]
        expected = [os.path.join(self.project_settings['project_path'], f) for f in expected]
        expected_missing = [os.path.join(self.project_settings['project_path'], f) for f in expected_missing]

        self.create_files(files_to_add)

        self.verify_files_contains_paths(expected)
        self.verify_files_does_not_contain_paths(expected_missing)

    @file_data('test_data/files_excludes_td.json')
    def test_willOnlyIncludeFilesThatMatchTheRegex(self, excludes, files_to_add, expected, expected_missing):
        self.setup_project_files_excludes(excludes)
        self.create_and_start_watchdog()

        files_to_add = [os.path.join(self.project_settings['project_path'], f) for f in files_to_add]
        expected = [os.path.join(self.project_settings['project_path'], f) for f in expected]
        expected_missing = [os.path.join(self.project_settings['project_path'], f) for f in expected_missing]

        self.create_files(files_to_add)

        self.verify_files_contains_paths(expected)
        self.verify_files_does_not_contain_paths(expected_missing)

    @file_data('test_data/files_moved_td.json')
    def test_willRemoveMovedFilesAndReAddThemIfSettingsAllow(self, regex, excludes, src, dest, expected, expected_missing):
        self.setup_project_files_regex(regex)
        self.setup_project_files_excludes(excludes)
        self.create_and_start_watchdog()

        src = os.path.join(self.project_settings['project_path'], src)
        dest = os.path.join(self.project_settings['project_path'], dest)
        expected = [os.path.join(self.project_settings['project_path'], f) for f in expected]
        expected_missing = [os.path.join(self.project_settings['project_path'], f) for f in expected_missing]
        self.create_files([src])

        self.move_file(src, dest)

        self.verify_files_contains_paths(expected)
        self.verify_files_does_not_contain_paths(expected_missing)

    def test_willTruncateExistingFilesFileOnInitialization(self):
        initial_paths_in_file = self.create_initial_files_file()
        self.create_and_start_watchdog()

        self.verify_files_does_not_contain_paths(initial_paths_in_file)

    def verify_files_contains_paths(self, paths):
        (files_contains, msg) = self.file_contains_paths(self.files_file, paths)
        self.assertTrue(files_contains, msg)

    def verify_files_does_not_contain_paths(self, paths):
        for f in paths:
            self.verify_files_does_not_contain_path(f)

    def verify_files_does_not_contain_path(self, path):
        (files_contains, msg) = self.file_contains_paths(self.files_file, [path])
        self.assertFalse(files_contains, msg)

    def setup_project_files_regex(self, regex):
        self.project_settings['files']['regex'] = regex

    def setup_project_files_excludes(self, regex):
        self.project_settings['files']['excludes'] = regex

    def create_initial_files_file(self):
        initial_paths = [
            'this/is/a/path',
            'this/is/another/path'
        ]
        self.create_file_with_contents(self.files_file, contents='\n'.join(initial_paths))
        return initial_paths

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

    def move_file(self, src, dest):
        self.fs_observer.move_file(src, dest)
        self.file_updater.update_files()

if __name__ == '__main__':
    unittest.main()
