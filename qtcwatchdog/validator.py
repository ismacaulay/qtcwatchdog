
import re


class RegexValidator(object):
    def __init__(self, pattern, excludes):
        if not pattern or pattern == '':
            pattern = '.*'  # match anything
        if not excludes or excludes == '':
            excludes = 'a^'  # match nothing

        self._pattern = re.compile(pattern)
        self._excludes = re.compile(excludes)

    def is_valid(self, string):
        return self._pattern.match(string) and not self._excludes.match(string)


class FilesPathValidator(RegexValidator):
    def __init__(self, excluded_paths, pattern_regex, excludes_regex):
        self._excluded_paths = excluded_paths

        super(FilesPathValidator, self).__init__(pattern_regex, excludes_regex)

    def is_valid(self, string):
        if string not in self._excluded_paths:
            return super(FilesPathValidator, self).is_valid(string)
        return False

