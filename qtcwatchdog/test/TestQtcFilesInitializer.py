import os
import unittest, mock
from qtcwatchdog.initializer import QtcFilesInitializer


class TestQtcFilesInitializer(unittest.TestCase):
    def setUp(self):
        pass

    @mock.patch('qtcwatchdog.updater.QtcUpdater', autospec=True)
    @mock.patch('os.walk')
    def test_willAddAllFilePathsToTheUpdater(self, mock_walk, mock_updater):
        mock_walk.return_value = project_directory_structure(os.path.normpath('project/path'))

        patient = QtcFilesInitializer(mock_updater)
        patient.initialize_files(os.path.normpath('project/path'))

        self.assertEqual(mock_updater.add.call_count, 4)
        mock_updater.add.assert_has_calls([
            mock.call(os.path.normpath('project/path/file1.txt')),
            mock.call(os.path.normpath('project/path/file2.txt')),
            mock.call(os.path.normpath('project/path/dir1/subfile1.txt')),
            mock.call(os.path.normpath('project/path/dir1/subfile2.txt')),
        ], any_order=True)

    @mock.patch('qtcwatchdog.updater.QtcUpdater', autospec=True)
    @mock.patch('os.walk')
    def test_willAddAllIncludesPathsToTheUpdater(self, mock_walk, mock_updater):
        mock_walk.side_effect = [
            project_directory_structure(os.path.normpath('project/path')),
            external_includes_structure(os.path.normpath('external/includes')),
            external_includes_structure(os.path.normpath('external2/includes')),
            [],
        ]

        patient = QtcFilesInitializer(mock_updater)
        includes = [os.path.normpath('external/includes'), os.path.normpath('external2/includes')]
        patient.initialize_includes(os.path.normpath('project/path'), includes)

        self.assertEqual(mock_updater.add.call_count, 15)
        mock_updater.add.assert_has_calls([
            mock.call(os.path.normpath('project/path'), is_dir=True),
            mock.call(os.path.normpath('project/path/dir1'), is_dir=True),
            mock.call(os.path.normpath('project/path/dir2'), is_dir=True),
            mock.call(os.path.normpath('project/path/dir1/subdir1'), is_dir=True),
            mock.call(os.path.normpath('project/path/dir1/subdir2'), is_dir=True),
            mock.call(os.path.normpath('external/includes'), is_dir=True),
            mock.call(os.path.normpath('external/includes/external_dir1'), is_dir=True),
            mock.call(os.path.normpath('external/includes/external_dir2'), is_dir=True),
            mock.call(os.path.normpath('external/includes/external_dir1/external_subdir1'), is_dir=True),
            mock.call(os.path.normpath('external/includes/external_dir1/external_subdir2'), is_dir=True),
            mock.call(os.path.normpath('external2/includes'), is_dir=True),
            mock.call(os.path.normpath('external2/includes/external_dir1'), is_dir=True),
            mock.call(os.path.normpath('external2/includes/external_dir2'), is_dir=True),
            mock.call(os.path.normpath('external2/includes/external_dir1/external_subdir1'), is_dir=True),
            mock.call(os.path.normpath('external2/includes/external_dir1/external_subdir2'), is_dir=True),
        ], any_order=True)


def project_directory_structure(project_path):
    structure = []
    root = project_path
    dirnames = ['dir1', 'dir2']
    filenames = ['file1.txt', 'file2.txt']
    structure.append((root, dirnames, filenames))
    structure.append((os.path.join(root, 'dir2'), [], []))

    root = os.path.join(project_path, 'dir1')
    dirnames = ['subdir1', 'subdir2']
    filenames = ['subfile1.txt', 'subfile2.txt']
    structure.append((root, dirnames, filenames))
    structure.append((os.path.join(root, 'subdir1'), [], []))
    structure.append((os.path.join(root, 'subdir2'), [], []))

    return structure


def external_includes_structure(include_root):
    structure = []
    root = include_root
    dirnames = ['external_dir1', 'external_dir2']
    filenames = ['file1.txt', 'file2.txt']
    structure.append((root, dirnames, filenames))
    structure.append((os.path.join(root, 'external_dir2'), [], []))

    root = os.path.join(include_root, 'external_dir1')
    dirnames = ['external_subdir1', 'external_subdir2']
    filenames = ['subfile1.txt', 'subfile2.txt']
    structure.append((root, dirnames, filenames))
    structure.append((os.path.join(root, 'external_subdir1'), [], []))
    structure.append((os.path.join(root, 'external_subdir2'), [], []))

    return structure

if __name__ == '__main__':
    unittest.main()
