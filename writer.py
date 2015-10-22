
import os, logging

class QtcFileWriter():
   def __init__(self, filepath, projpath, basepaths=[]):
      self._projpath = projpath
      self._basepaths = basepaths
      self._filepath = filepath

   def write(self, list_to_write):
      logging.debug('QtcFileWriter::write: ' + str(list_to_write))
      with open(self._filepath, 'w') as f:
         for i in list_to_write:
            f.write(self._convert_to_path(i) + '\n')

   def append(self, line):
      logging.debug('QtcFileWriter::append: ' + str(line))
      with open(self._filepath, 'a') as f:
         f.write(line + '\n')

   def remove(self, line_to_remove):
      logging.debug('QtcFileWriter::remove: ' + str(line_to_remove))
      position = 0
      found = False
      with open(self._filepath, 'r+') as f:
         data = f.readlines()
         for line in data:
            line = self._convert_to_path(line)
            if line == line_to_remove:
               found = True
               f.seek(position)
            elif found:
               f.write(line + '\n')
            else:
               position += 1
         if found:
            f.truncate()

   def remove_and_append(self, line_to_remove, line_to_append):
      logging.debug('QtcFileWriter::remove_and_append: ' + str(line_to_remove) + ' ' + str(line_to_append))
      position = 0
      found = False
      with open(self._filepath, 'r+') as f:
         data = f.readlines()
         for line in data:
            line = self._convert_to_path(line)
            if line == line_to_remove:
               found = True
               f.seek(position)
            elif found:
               f.write(line + '\n')
            else:
               position += 1
         if found:
            f.truncate()
         f.write(line_to_append + '\n')

   def _convert_to_path(self, line):
      line = line.strip()
      line = os.path.abspath(line)
      for basepath in self._basepaths:
         if line.startswith(basepath):
            return line
      return os.path.join(self._projpath, line)
