
import unittest
import os
import mock

from qtcwatchdog.settings import Settings, InvalidSettingsError


class TestSettings(unittest.TestCase):
    def test_willRaiseExceptionIfProjectPathIsMissing(self):
        def create_patient():
            Settings({})

        self.assertRaises(InvalidSettingsError, create_patient)

    @mock.patch('os.path.exists')
    def test_willRaiseExceptionIfProjectPathIsInvalid(self, mock_os_path_exists):
        def create_patient(path):
            Settings({'project_path': path})

        mock_os_path_exists.return_value = False

        self.assertRaises(InvalidSettingsError, create_patient, 'hello/World')
        mock_os_path_exists.assert_called_with('hello/World')

        mock_os_path_exists.return_value = True
        try:
            create_patient('helloWorld')
        except InvalidSettingsError:
            self.fail("InvalidSettingsError thrown when it shouldn't.")

    def test_willReturnProjectName(self):
        project = 'helloworld'
        settings = anonymous_settings_dict()
        settings['project'] = project

        patient = Settings(settings)

        self.assertEqual(patient.project, project)

    def test_willDefaultProjectNameToProjectPathBasename(self):
        settings = anonymous_settings_dict()
        project_name = os.path.basename(settings['project_path'])

        patient = Settings(settings)

        self.assertEqual(patient.project, project_name)

    def test_willReturnFilesRegex(self):
        settings = anonymous_settings_dict()
        settings['files'] = {'regex': 'helloworld'}

        patient = Settings(settings)

        self.assertEqual(patient.files_regex, 'helloworld')

    def test_willReturnDefaultFilesRegex(self):
        settings = anonymous_settings_dict()
        settings['files'] = {}

        patient = Settings(settings)
        self.assertEqual(patient.files_regex, '')

        patient = Settings(anonymous_settings_dict())
        self.assertEqual(patient.files_regex, '')

    def test_willReturnFilesExcludes(self):
        settings = anonymous_settings_dict()
        settings['files'] = {'excludes': 'helloworld'}

        patient = Settings(settings)

        self.assertEqual(patient.files_excludes, 'helloworld')

    def test_willReturnDefaultFilesExcludes(self):
        settings = anonymous_settings_dict()
        settings['files'] = {}

        patient = Settings(settings)
        self.assertEqual(patient.files_excludes, '')

        patient = Settings(anonymous_settings_dict())
        self.assertEqual(patient.files_excludes, '')

    def test_willReturnIncludesPaths(self):
        settings = anonymous_settings_dict()

        patient = Settings(settings)
        self.assertListEqual(patient.includes_paths, [])

        settings['includes'] = {'paths': ['hello', 'world']}
        patient = Settings(settings)
        self.assertListEqual(patient.includes_paths, ['hello', 'world'])

    def test_willReturnIncludesRegex(self):
        settings = anonymous_settings_dict()

        patient = Settings(settings)
        self.assertEqual(patient.includes_regex, '')

        settings['includes'] = {'regex': 'helloWorld'}
        patient = Settings(settings)
        self.assertEqual(patient.includes_regex, 'helloWorld')

    def test_willReturnIncludesExcludes(self):
        settings = anonymous_settings_dict()

        patient = Settings(settings)
        self.assertEqual(patient.includes_excludes, '')

        settings['includes'] = {'excludes': 'helloWorld'}
        patient = Settings(settings)
        self.assertEqual(patient.includes_excludes, 'helloWorld')


def anonymous_settings_dict():
    return {'project_path': os.getcwd()}

if __name__ == '__main__':
    unittest.main()

