import os.path


class Settings(object):
    def __init__(self, settings_dict):
        self._settings = settings_dict
        if 'project_path' not in self._settings:
            raise InvalidSettingsError('Project path missing')

        if not os.path.exists(self._settings['project_path']):
            raise InvalidSettingsError('Project path invalid')

    @property
    def project_name(self):
        # TODO: rename to just project
        return self._settings.get('project_name', os.path.basename(self.project_path))

    @property
    def project_path(self):
        return self._settings.get('project_path')

    @property
    def files_regex(self):
        return self._settings.get('files', {}).get('regex', '')

    @property
    def files_excludes(self):
        return self._settings.get('files', {}).get('excludes', '')

    @property
    def includes_paths(self):
        return self._settings.get('includes', {}).get('paths', [])

    @property
    def includes_regex(self):
        return self._settings.get('includes', {}).get('regex', '')

    @property
    def includes_excludes(self):
        return self._settings.get('includes', {}).get('excludes', '')


class InvalidSettingsError(Exception):
    def __init__(self, msg):
        print msg
        self.msg = msg

