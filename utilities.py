
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

def write_list(path, list_to_write):
   with open(path, 'w') as f:
      for i in list_to_write:
         f.write(i + '\n')

def append_line(path, line):
   with open(path, 'a') as f:
      f.write(line + '\n')

def remove_line(path, line):
   with open(path, 'r+') as f:
      data = f.readlines()
      f.seek(0)
      for line in data:
         if line.strip() != remove:
            f.write(line)
      f.truncate()

def remove_and_append(path, remove, append):
   print 'utilities::remove_and_append: r:' + remove + ' a: ' + append
   with open(path, 'r+') as f:
      data = f.readlines()
      f.seek(0)
      for line in data:
         if line.strip() != remove:
            f.write(line)
      f.write(append + '\n')
      f.truncate()
