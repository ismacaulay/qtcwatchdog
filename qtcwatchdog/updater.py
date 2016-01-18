
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



