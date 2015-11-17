# qtcwatchdog

qtcwatchdog is a python module that watches a given directory and updates the qt creator files and includes files for
imported projects.

### Dependencies
#### Python 2.7
- watchdog 0.8.3

### Example
```
#!/usr/bin/env python

import sys, os
print os.path.dirname(__file__)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qtcwatchdog import QtcWatchdog

def main():
   args = {
      'project': 'sample',          # default = basename of project_path
      'project_path': 'project',    # required

      'files': {
         'regex': '.*\.(txt|py)',      # defualt = .*
         'excludes': '(.*\.tmp)',      # defualt = no excludes
      },

      'includes': {
         'regex': '',                  # default = .*
         'excludes': '(excluded_*)',   # default = no excludes
      'paths': [                       # default = []
            'project_includes'
         ]
      }
   }
   watchdog = QtcWatchdog(**args)

if __name__ == '__main__':
   main()
```

