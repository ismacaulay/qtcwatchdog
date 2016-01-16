import os
import threading


class QtcUpdater(object):
    def __init__(self, files, includes):
        self._files = files
        self._includes = includes

    def add(self, path, is_dir=False):
        self._perform_operation(path, is_dir, self._files.write, self._includes.write)

    def remove(self, path, is_dir=False):
        self._perform_operation(path, is_dir, self._files.remove, self._includes.remove)

    def move(self, src, dest, is_dir=False):
        self._perform_operation(src, is_dir, self._files.remove, self._includes.remove)
        self._perform_operation(dest, is_dir, self._files.write, self._includes.write)

    def update_files(self):
        self._files.update()
        self._includes.update()

    @staticmethod
    def _perform_operation(path, is_dir, files_operation, includes_operation):
        if is_dir:
            includes_operation(path)
        else:
            files_operation(path)


class QtcFile(object):
    def __init__(self, writer, validator):
        self._writer = writer
        self._validator = validator

    def write(self, path):
        if self._validator.is_valid(path):
            self._writer.write(path)

    def remove(self, path):
        if self._validator.is_valid(path):
            self._writer.remove(path)

    def update(self):
        self._writer.process_caches()


class FileWriter(object):
    def __init__(self, path):
        if not os.path.isfile(path):
            raise InvalidPathError('The file {} does not exist.'.format(str(path)))

        self._path = path
        self._write_cache = set()
        self._remove_cache = set()

        self._lock = threading.Lock()

    def write(self, path):
        self._lock.acquire()
        self._write_cache.add(path)
        self._lock.release()

    def remove(self, path):
        self._lock.acquire()
        if path in self._write_cache:
            self._write_cache.remove(path)
        self._remove_cache.add(path)
        self._lock.release()

    def process_caches(self):
        self._lock.acquire()
        write_cache = set(self._write_cache)
        self._write_cache = set()
        remove_cache = set(self._remove_cache)
        self._remove_cache = set()
        self._lock.release()

        if len(write_cache) > 0 or len(remove_cache) > 0:
            with open(self._path, 'r+') as f:
                data = f.readlines()
                for path in data:
                    stripped_path = path.strip('\n')
                    if stripped_path not in remove_cache:
                        f.write(path)

                for path in write_cache:
                    f.write(path + '\n')

                f.truncate()


class InvalidPathError(Exception):
    def __init__(self, msg):
        self.msg = msg

