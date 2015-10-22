
import logging

class QtcUpdater():
   def __init__(self, qtc_files, qtc_includes):
      self._qtc_files = qtc_files
      self._qtc_includes = qtc_includes

   def add(self, path, is_dir):
      if is_dir:
         self._qtc_includes.write(path)
      else:
         self._qtc_files.write(path)

   def remove(self, path, is_dir):
      if is_dir:
         self._qtc_includes.remove(path)
      else:
         self._qtc_files.remove(path)

   def move(self, src, dest, is_dir):
      if is_dir:
         self._qtc_includes.move(src, dest)
      else:
         self._qtc_files.move(src, dest)
