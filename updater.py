
import os
import threading

class QtcUpdater(object):
   def __init__(self, proj, projpath, files_validator, includes_validator):
      self._qtc_files = QtcFile(os.path.join(projpath, '{}.files'.format(str(proj))), files_validator)
      self._qtc_includes = QtcFile(os.path.join(projpath, '{}.includes'.format(str(proj))), includes_validator)
      self._projpath = projpath

   def add(self, path, is_dir, relpath=True):
      path = self._convert_to_path(path, relpath)
      if is_dir:
         print '[add include] ' + path
         self._qtc_includes.write(path)
      else:
         print '[add file] ' + path
         self._qtc_files.write(path)

   def remove(self, path, is_dir):
      path = self._convert_to_path(path)
      if is_dir:
         print '[remove include] ' + path
         self._qtc_includes.remove(path)
      else:
         print '[remove file] ' + path
         self._qtc_files.remove(path)

   def move(self, src, dest, is_dir):
      src = self._convert_to_path(src)
      dest = self._convert_to_path(dest)
      if is_dir:
         print '[move include]\n   src: ' + src + '\n   dest:' + dest
         self._qtc_includes.move(src, dest)
      else:
         print '[move file]\n   src: ' + src + '\n   dest:' + dest
         self._qtc_files.move(src, dest)

   def _convert_to_path(self, path, relpath=True):
      if relpath:
         return os.path.relpath(path, self._projpath)
      else:
         return os.path.abspath(path)

class QtcFile(object):
   def __init__(self, path, validator):
      if not os.path.isfile(path):
         raise Exception('{} does not exists'.format(str(path)))

      self._writer = FileWriter(path)
      self._validator = validator

   def write(self, path):
      if self._validator.is_valid(path):
         self._writer.write(path)

   def remove(self, path):
      if self._validator.is_valid(path):
         self._writer.remove(path)

   def move(self, src, dest):
      self.remove(src)
      self.write(dest)


class FileWriter(object):
   def __init__(self, path):
      self._file_path = path
      self._paths_to_write = set()
      self._paths_to_remove = set()
      self._process_timer = threading.Timer(1.0, self._process_paths)
      self._lock = threading.Lock()
      with open(self._file_path, 'r+') as f:
         f.truncate()

   def _timer_reset(self):
      self._process_timer.cancel()
      self._process_timer = threading.Timer(1.0, self._process_paths)

   def _reset_and_lock(self):
      self._timer_reset()
      self._lock.acquire()

   def _unlock_and_start(self):
      self._lock.release()
      self._process_timer.start()

   def write(self, path):
      self._reset_and_lock()
      if path in self._paths_to_remove:
         self._paths_to_remove.remove(path)
      self._paths_to_write.add(path)
      self._unlock_and_start()

   def remove(self, path):
      self._reset_and_lock()
      if path in self._paths_to_write:
         self._paths_to_write.remove(path)
      self._paths_to_remove.add(path)
      self._unlock_and_start()

   def _process_paths(self):
      # grab the lock, copy/clear the sets, remove the lock
      self._lock.acquire()
      write_paths = set(self._paths_to_write)
      self._paths_to_write = set()
      remove_paths = set(self._paths_to_remove)
      self._paths_to_remove = set()
      self._lock.release()

      with open(self._file_path, 'r+') as f:
         found_first = False
         data = f.readlines()
         offset = 0

         if len(remove_paths) > 0:
            for line in data:
               stripped_line = line.strip('\n') # strip the newline character off the end
               
               # if we should remove the line:
               #     if we have not removed any line yet, seek to the position in the file
               #     if we have removed a line, just remove the line from the paths to remove
               # else if we have seeked to the first line to remove:
               #     write the line to the file
               if stripped_line in remove_paths:
                  if not found_first:
                     found_first = True
                     f.seek(offset)
                  remove_paths.remove(stripped_line)
               elif found_first:
                  f.write(line)
                  offset += len(line)
               else:
                  offset += len(line)

            f.seek(offset)
            f.truncate()

         # if there are any paths that need writing, write them
         for path in write_paths:
            f.write(path + '\n')
