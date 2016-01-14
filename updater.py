import os
import threading


class QtcUpdater(object):
    def __init__(self, files, includes):
        self._files = files
        self._includes = includes

    def add(self, path, is_dir):
        self._perform_operation(path, is_dir, self._files.write, self._includes.write)

    def remove(self, path, is_dir):
        self._perform_operation(path, is_dir, self._files.remove, self._includes.remove)

    def move(self, src, dest, is_dir):
        self._perform_operation(src, is_dir, self._files.remove, self._includes.remove)
        self._perform_operation(dest, is_dir, self._files.write, self._includes.write)

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


class FileWriter(object):
    def __init__(self, path):
        if not os.path.isfile(path):
            raise InvalidPathError('The file {} does not exist.'.format(str(path)))

        self._path = path
        with open(self._path, 'r+') as f:
            f.truncate()

        self._write_cache = set()
        self._remove_cache = set()

        self._lock = threading.Lock()
        self._process_timer = threading.Timer(interval=1.0, function=self._process_paths)
        self._process_timer.start()

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

    def _process_paths(self):
        self._lock.acquire()
        write_paths = set(self._write_cache)
        self._write_cache = set()
        remove_paths = set(self._remove_cache)
        self._paths_to_remove = set()
        self._lock.release()

        # todo: dont open if caches are empty
        with open(self._path, 'r+') as f:
            data = f.readlines()
            for path in data:
                stripped_path = path.strip('\n')
                if stripped_path not in remove_paths:
                    f.write(path)

            for path in write_paths:
                f.write(path + '\n')

            f.truncate()

        self._process_timer.start()

    #         found_first = False
    #         data = f.readlines()
    #         offset = 0
    #
    #         if len(remove_paths) > 0:
    #             for line in data:
    #                 stripped_line = line.strip('\n')  # strip the newline character off the end
    #
    #                 # if we should remove the line:
    #                 #     if we have not removed any line yet, seek to the position in the file
    #                 #     if we have removed a line, just remove the line from the paths to remove
    #                 # else if we have seeked to the first line to remove:
    #                 #     write the line to the file
    #                 if stripped_line in remove_paths:
    #                     if not found_first:
    #                         found_first = True
    #                         f.seek(offset)
    #                     remove_paths.remove(stripped_line)
    #                 elif found_first:
    #                     f.write(line)
    #                     offset += len(line)
    #                 else:
    #                     offset += len(line)
    #
    #             f.seek(offset)
    #             f.truncate()
    #
    #         # if there are any paths that need writing, write them


class InvalidPathError(Exception):
    def __init__(self, msg):
        self.msg = msg

