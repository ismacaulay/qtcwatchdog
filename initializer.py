import os.path


class QtcFilesInitializer(object):
    def __init__(self, updater):
        self._updater = updater

    def initialize_files(self, project_path):
        for root, _, files in os.walk(project_path):
            for fname in files:
                self._updater.add(os.path.join(root, fname))

    def initialize_includes(self, project_path, includes_paths):
        for root, _, _ in os.walk(project_path):
            self._updater.add(root, is_dir=True)
        for include_path in includes_paths:
            for root, _, _ in os.walk(include_path):
                self._updater.add(root, is_dir=True)
