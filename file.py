
import logging

class QtcFile():
   def __init__(self, path, validator, writer, initial_data):
      self._path = path
      self._validator = validator
      self._writer = writer
      self._data = self._validator.validate_list(initial_data)
      self._writer.write(self._data)

   def write(self, path):
      path = self._validator.validate_path(path)
      if path and not path in self._data:
         self._data.append(path)
         self._writer.append(path)

   def remove(self, path):
      path = self._validator.validate_path(path)
      if path and path in self._data:
         self._data.remove(path)
         self._writer.remove(path)

   def move(self, src, dest):
      src = self._validator.validate_path(src)
      dest = self._validator.validate_path(dest)
      if src and src in self._data:
         self._data.remove(src)
         if dest and not dest in self._data:
            self._data.append(dest)
            self._writer.remove_and_append(src, dest)
         else:
            self._writer.remove(src)
      elif dest and not dest in self._data:
         self._data.append(dest)
         self._writer.append(dest)
