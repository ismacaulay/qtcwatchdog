from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import time


class ProjectWatcher(object):
    def __init__(self, project_path, updater):
        self._updater = updater
        self._event_handler = ProjectWatcher.EventHandler(updater)
        self._observer = Observer()
        self._observer.schedule(self._event_handler, project_path, recursive=True)

    def start(self):
        try:
            self._observer.start()
        except OSError as e:
            if 'inotify watch limit reached' in e:
                raise InotifyError()
            else:
                print e.filename
                raise e

        while running():
            try:
                self._updater.update_files()
                time.sleep(1)
            except KeyboardInterrupt:
                break

    def stop(self):
        self._observer.stop()
        self._observer.join()

    class EventHandler(FileSystemEventHandler):
        def __init__(self, updater):
            self._updater = updater

        def on_created(self, event):
            self._updater.add(event.src_path, event.is_directory)

        def on_deleted(self, event):
            self._updater.remove(event.src_path, event.is_directory)

        def on_moved(self, event):
            self._updater.move(event.src_path, event.dest_path, event.is_directory)


def running():
    return True


class InotifyError(Exception):
    def __init__(self):
        pass