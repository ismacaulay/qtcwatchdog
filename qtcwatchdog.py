#!/usr/bin/env python
import os

from updater import QtcUpdater, QtcFile, FileWriter
from validator import RegexValidator
from settings import Settings
from initializer import QtcFilesInitializer
from watcher import ProjectWatcher


class QtcWatchdog(object):
    def __init__(self, project_settings):
        settings = Settings(project_settings)

        files_validator = RegexValidator(settings.files_regex, settings.files_excludes)
        files_writer = FileWriter(os.path.join(settings.project_path, '{}.files'.format(settings.project_name)))
        files_file = QtcFile(files_writer, files_validator)

        includes_validator = RegexValidator(settings.includes_regex, settings.includes_excludes)
        includes_writer = FileWriter(os.path.join(settings.project_path, '{}.includes'.format(settings.project_name)))
        includes_file = QtcFile(includes_writer, includes_validator)

        updater = QtcUpdater(files_file, includes_file)
        initializer = QtcFilesInitializer(updater)
        initializer.initialize_files(settings.project_path)
        initializer.initialize_includes(settings.project_path, settings.includes_paths)

        self._watcher = ProjectWatcher(settings.project_path, updater)

    def start(self):
        self._watcher.start()

    def stop(self):
        self._watcher.stop()
