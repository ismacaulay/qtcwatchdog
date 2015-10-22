
import logging

class QtcUpdater():
   def __init__(self, qtc_files, qtc_includes):
      self._qtc_files = qtc_files
      self._qtc_includes = qtc_includes

   def add(self, path, is_dir):
      if is_dir:
         logging.debug('QtcUpdater::add include=' + str(path))
         self._qtc_includes.write(path)
      else:
         logging.debug('QtcUpdater::add file=' + str(path))
         self._qtc_files.write(path)

   def remove(self, path, is_dir):
      if is_dir:
         logging.debug('QtcUpdater::remove include=' + str(path))
         self._qtc_includes.remove(path)
      else:
         logging.debug('QtcUpdater::remove file=' + str(path))
         self._qtc_files.remove(path)

   def move(self, src, dest, is_dir):
      if is_dir:
         logging.debug('QtcUpdater::move include src=' + str(src) + ' dest=' + str(dest))
         self._qtc_includes.move(src, dest)
      else:
         logging.debug('QtcUpdater::move file src=' + str(src) + ' dest=' + str(dest))
         self._qtc_files.move(src, dest)
