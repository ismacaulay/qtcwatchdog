#!/usr/bin/env python
import os, sys, time, logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, RegexMatchingEventHandler

from updater import QtcUpdater, QtcFile, FileWriter
from validator import RegexValidator
from settings import Settings
from initializer import QtcFilesInitializer
from watcher import ProjectWatcher

class QtcWatchdog(object):
    def __init__(self, **kwargs):
        settings = Settings(kwargs)

        files_validator = RegexValidator(settings.files_regex, settings.files_excludes)
        files_writer = FileWriter(os.path.join(settings.project_path, '{}.files'.format(settings.project_name)))
        files_file = QtcFile(files_writer, files_validator)

        includes_validator = RegexValidator(settings.includes_regex, settings.includes_excludes)
        includes_writer = FileWriter(os.path.join(settings.project_path, '{}.includes'.format(settings.project_name)))
        includes_file = QtcFile(includes_writer, includes_validator)

        updater = QtcUpdater(files_file, includes_file)
        initializer = QtcFilesInitializer()
        initializer.initialize_files(settings.project_path, updater)
        initializer.initialize_includes(settings.includes_paths, updater)

        self._watcher = ProjectWatcher(updater)

        # print_message('Initializing event handler...', False)
        # self._event_handler = QtcWatchdog.EventHandler(updater, files_regex, files_excludes)
        # self._observer = Observer()
        # self._observer.schedule(self._event_handler, self._project_path, recursive=True)
        # print_message('done')

    def start(self):
        self._watcher.start()

    def stop(self):
        self._watcher.stop()

    # def start(self):
    #     try:
    #         print_message('Starting watchdog...', False)
    #         self._observer.start()
    #         print_message('running')
    #     except OSError as e:
    #         if 'inotify watch limit reached' in e:
    #             msg =  'inotify watch limit reached.\n\n'
    #             msg += 'To fix add the \'fs.inotify.max_user_watches = 524288\' to /etc/sysctl.conf\n'
    #             msg += 'Then run \'sudo sysctl -p\'\n'
    #             raise Exception(msg)
    #         else:
    #             raise e
    #
    #     try:
    #         while True:
    #             if self._observer.isAlive():
    #                 time.sleep(1)
    #             else:
    #                 self._restart()
    #     except KeyboardInterrupt as e:
    #         raise e
    #     except:
    #         print 'Exception thrown. Restarting watchdog'
    #         self._restart()

    # def stop(self):
    #     print_message('Stopping watchdog...', False)
    #     self._observer.stop()
    #     self._observer.join()
    #     print_message('done')
    #
    # def _restart(self):
    #     self._observer.stop()
    #     self._observer = Observer()
    #     self._observer.schedule(self._event_handler, self._project_path, recursive=True)
    #     self._observer.start()
    #
    # class EventHandler(RegexMatchingEventHandler):
    #     def __init__(self, updater, regex, ignores):
    #         self._updater = updater
    #         super(QtcWatchdog.EventHandler, self).__init__(regexes=[regex], ignore_regexes=[ignores])
    #
    #     def on_created(self, event):
    #         self._updater.add(event.src_path, event.is_directory)
    #
    #     def on_deleted(self, event):
    #         self._updater.remove(event.src_path, event.is_directory)
    #
    #     def on_moved(self, event):
    #         self._updater.move(event.src_path, event.dest_path, event.is_directory)


def print_message(message, newline=True):
    if newline:
        print message
    else:
        print message,
    sys.stdout.flush()
