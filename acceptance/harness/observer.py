import mock


class FakeObserver(object):
    def __init__(self, fs):
        self.fs = fs
        self.event_handler = None
        self.running = False
        self.joined = False

    def schedule(self, event_handler, project_path, recursive):
        self.event_handler = event_handler

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def join(self):
        self.joined = True

    def create_file(self, path):
        self.fs.CreateFile(path)
        self.event_handler.on_created(self.create_event(src_path=path))

    def create_directory(self, path):
        self.fs.CreateDirectory(path)
        self.event_handler.on_created(self.create_event(src_path=path, is_directory=True))

    def remove_file(self, path):
        self.fs.RemoveObject(path)
        self.event_handler.on_deleted(self.create_event(src_path=path))

    def remove_directory(self, path):
        self.fs.RemoveObject(path)
        self.event_handler.on_deleted(self.create_event(src_path=path, is_directory=True))

    def move_file(self, src, dest):
        self.fs.RemoveObject(src)
        self.fs.CreateFile(dest)
        self.event_handler.on_moved(self.create_event(src_path=src, dest_path=dest))

    def move_directory(self, src, dest):
        self.fs.RemoveObject(src)
        self.fs.CreateDirectory(dest)
        self.event_handler.on_moved(self.create_event(src_path=src, dest_path=dest, is_directory=True))

    @staticmethod
    def create_event(src_path='', dest_path='', is_directory=False):
        event = mock.MagicMock()
        event.src_path = src_path
        event.dest_path = dest_path
        event.is_directory = is_directory
        return event

