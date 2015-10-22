
import os, logging

class PathValidator():
   def __init__(self, file_patterns, exclude_dirs, includes):
      self._extensions = self._extensions_from_pattterns(file_patterns)
      self._filenames = self._filenames_from_patterns(file_patterns)
      self._exclude_dirs = exclude_dirs
      self._includes = includes

   def validate_list(self, data):
      ret = []
      for path in data:
         path = self.validate_path(path)
         if path:
            ret.append(path)
      return ret

   def validate_path(self, path):
      if os.path.isdir(path):
         return self._validate_include(path)
      else:
         return self._validate_file(path)

   def _validate_include(self, path):
      if self._is_include(path):
         return self._check_excludes(path)
      return None

   def _validate_file(self, path):
      _, ext = os.path.splitext(path)
      if self._all_included():
         return self._check_excludes(path)
      if ext in self._extensions:
         return self._check_excludes(path)
      if os.path.basename(path) in self._filenames:
         return self._check_excludes(path)
      return None

   def _check_excludes(self, path):
      if len(self._exclude_dirs) == 0:
         return path

      remaining = path
      while True:
         (remaining, x) = os.path.split(remaining)
         if not x or x == '':
            return path
         if x in self._exclude_dirs:
            return None

   def _all_included(self):
      return len(self._extensions) == 0 and len(self._filenames) == 0
   
   def _is_include(self, path):
      p = os.path.abspath(path)
      for inc in self._includes:
         if p.startswith(os.path.abspath(inc)):
            return True
      return False

   def _extensions_from_pattterns(self, patterns):
      exts = []
      for p in patterns:
         if p.startswith('*.'):
            _, ext = os.path.splitext(p)
            exts.append(ext)
      return exts

   def _filenames_from_patterns(self, patterns):
      fnames = []
      for p in patterns:
         if not p.startswith('*.'):
            fnames.append(p)
      return fnames
