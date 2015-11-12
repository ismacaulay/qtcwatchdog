
import os, sys

def check_path_exists(path):
   if not os.path.exists(path):
      print('Error: {0} does not exist'.format(str(path)))
      sys.exit(1)

def all_files_and_dirs(path):
   files = set()
   dirs = set()
   for root, dirnames, filenames in os.walk(path):
      dirs.add(root)
      for fname in filenames:
         files.add(os.path.join(root, fname))
   return (files, dirs)

def split_semicolon(s):
   if len(s) == 0:
      return []
   return s.strip().split(';')
