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
        # self._paths_to_write = set()
        # self._paths_to_remove = set()
        self._lock = threading.Lock()
        self._process_timer = threading.Timer(interval=1.0, function=self._process_paths)

    # def _timer_reset(self):
    #     self._process_timer.cancel()
    #     self._process_timer = threading.Timer(1.0, self._process_paths)
    #
    # def _reset_and_lock(self):
    #     self._timer_reset()
    #     self._lock.acquire()
    #
    # def _unlock_and_start(self):
    #     self._lock.release()
    #     self._process_timer.start()
    #
    def write(self, path):
        self._lock.acquire()

        self._lock.release()
    #
    # def remove(self, path):
    #     self._reset_and_lock()
    #     if path in self._paths_to_write:
    #         self._paths_to_write.remove(path)
    #     self._paths_to_remove.add(path)
    #     self._unlock_and_start()
    #
    def _process_paths(self):
        # grab the lock, copy/clear the sets, remove the lock
        self._lock.acquire()
    #     write_paths = set(self._paths_to_write)
    #     self._paths_to_write = set()
    #     remove_paths = set(self._paths_to_remove)
    #     self._paths_to_remove = set()
        self._lock.release()
    #
    #     with open(self._file_path, 'r+') as f:
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
    #         for path in write_paths:
    #             f.write(path + '\n')


class InvalidPathError(Exception):
    def __init__(self, msg):
        self.msg = msg

