
import re

class RegexValidator(object):
   def __init__(self, pattern, excludes):
      self._pattern = re.compile(pattern)
      self._excludes = re.compile(excludes)

   def is_valid(self, string):
      return self._pattern.match(string) and not self._excludes.match(string):
