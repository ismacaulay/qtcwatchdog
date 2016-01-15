
import unittest, mock
from initializer import QtcFilesInitializer


class TestQtcFilesInitializer(unittest.TestCase):

    def setUp(self):
        pass

    @mock.patch('updater.QtcUpdater', autospec=True)
    @mock.patch('os.walk')
    def test_willAddAllFilePathsToTheUpdater(self, mock_walk, mock_updater):
        mock_walk.return_value = project_directory_structure('project/path')

        patient = QtcFilesInitializer(mock_updater)
        patient.initialize_files('project/path')

        self.assertEqual(mock_updater.add.call_count, 4)
        mock_updater.add.assert_has_calls([
            mock.call('project/path/file1.txt'),
            mock.call('project/path/file2.txt'),
            mock.call('project/path/dir1/subfile1.txt'),
            mock.call('project/path/dir1/subfile2.txt'),
        ], any_order=True)

    @mock.patch('updater.QtcUpdater', autospec=True)
    @mock.patch('os.walk')
    def test_willAddAllIncludesPathsToTheUpdater(self, mock_walk, mock_updater):
        def walk_side_effect(path):
            if path == 'project/path':
                return project_directory_structure('project/path')
            elif path == 'external/includes' or 'external2/includes':
                return external_includes_structure(path)
            else:
                return []
        mock_walk.side_effect = walk_side_effect

        patient = QtcFilesInitializer(mock_updater)
        includes = ['external/includes', 'external2/includes']
        patient.initialize_includes('project/path', includes)

        self.assertEqual(mock_updater.add.call_count, 15)
        mock_updater.add.assert_has_calls([
            mock.call('project/path', is_dir=True),
            mock.call('project/path/dir1', is_dir=True),
            mock.call('project/path/dir2', is_dir=True),
            mock.call('project/path/dir1/subdir1', is_dir=True),
            mock.call('project/path/dir1/subdir2', is_dir=True),
            mock.call('external/includes', is_dir=True),
            mock.call('external/includes/external_dir1', is_dir=True),
            mock.call('external/includes/external_dir2', is_dir=True),
            mock.call('external/includes/external_dir1/external_subdir1', is_dir=True),
            mock.call('external/includes/external_dir1/external_subdir2', is_dir=True),
            mock.call('external2/includes', is_dir=True),
            mock.call('external2/includes/external_dir1', is_dir=True),
            mock.call('external2/includes/external_dir2', is_dir=True),
            mock.call('external2/includes/external_dir1/external_subdir1', is_dir=True),
            mock.call('external2/includes/external_dir1/external_subdir2', is_dir=True),
        ], any_order=True)


def project_directory_structure(project_path):
    structure = []
    root = project_path
    dirnames = ['dir1', 'dir2']
    filenames = ['file1.txt', 'file2.txt']
    structure.append((root, dirnames, filenames))
    structure.append((root + '/dir2', [], []))

    root = project_path + '/dir1'
    dirnames = ['subdir1', 'subdir2']
    filenames = ['subfile1.txt', 'subfile2.txt']
    structure.append((root, dirnames, filenames))
    structure.append((root + '/subdir1', [], []))
    structure.append((root + '/subdir2', [], []))

    return structure


def external_includes_structure(include_root):
    structure = []
    root = include_root
    dirnames = ['external_dir1', 'external_dir2']
    filenames = ['file1.txt', 'file2.txt']
    structure.append((root, dirnames, filenames))
    structure.append((root + '/external_dir2', [], []))

    root = include_root + '/external_dir1'
    dirnames = ['external_subdir1', 'external_subdir2']
    filenames = ['subfile1.txt', 'subfile2.txt']
    structure.append((root, dirnames, filenames))
    structure.append((root + '/external_subdir1', [], []))
    structure.append((root + '/external_subdir2', [], []))

    return structure

