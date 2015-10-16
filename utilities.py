
import os

def check_path_exists(path):
   if not os.path.exists(path):
      print 'Error: {0} does not exist'.format(unicode(path))
      sys.exit(1)

def all_files_and_dirs(path):
   files = []
   dirs = []
   for root, dirnames, filenames in os.walk(path):
      dirs.append(root)
      for fname in filenames:
         files.append(os.path.join(root, fname))
   return (files, dirs)

def split_semicolon(s):
   return s.strip().split(';')
