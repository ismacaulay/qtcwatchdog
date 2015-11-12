#!/usr/bin/env python
import os, sys, time, logging
from argparse import ArgumentParser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import utilities
from updater import QtcUpdater
from validator import RegexValidator

class QtcWatchdog(object):
   def __init__(self, *args, **kwargs):
      self._configured = False

      if not 'watchdir' in kwargs:
         print 'Missing watchdir'
         return

      self._watchdir = kwargs.get('watchdir')
      
      proj = kwargs.get('proj', os.path.basename(self._watchdir))

      files_regex = kwargs.get('files_regex', '')
      files_excludes_regex = kwargs.get('files_excludes_regex', '')
      files_validator = RegexValidator(files_regex, files_excludes_regex)
      
      includes_regex = kwargs.get('includes_regex', '')
      includes_excludes_regex = kwargs.get('includes_excludes_regex', '')
      includes_validator = RegexValidator(includes_regex, includes_excludes_regex)

      print 'Initializing files...',
      sys.stdout.flush()
      updater = QtcUpdater(proj, self._watchdir, files_validator, includes_validator)
      (files, dirs) = utilities.all_files_and_dirs(self._watchdir)
      for f in files:
         updater.add(f, False)
      for d in dirs:
         updater.add(d, True)
      print 'done'
      sys.stdout.flush()
      
      print 'Initializing event handler...',
      sys.stdout.flush()
      self._event_handler = QtcWatchdog.EventHandler(updater)
      self._observer = Observer()
      self._observer.schedule(self._event_handler, self._watchdir, recursive=True)
      self._configured = True
      print 'done'
      sys.stdout.flush()

   def start(self):
      if not self._configured:
         print 'Not configured.'
         return

      while True:
         if self._observer.isAlive():
            time.sleep(1)
         else:
            self._restart()

   def stop(self):
      self._observer.stop()
      self._observer.join()

   def _restart(self):
      self._observer.stop()
      self._observer = Observer()
      self._observer.schedule(self._event_handler, self._watchdir, recursive=True)
      self._observer.start()

   class EventHandler(FileSystemEventHandler):
      def __init__(self, updater):
         self._updater = updater

      def on_created(self, event):
         self._updater.add(event.src_path, event.is_directory)

      def on_deleted(self, event):
         self._updater.remove(event.src_path, event.is_directory)

      def on_moved(self, event):
         self._updater.move(event.src_path, event.dest_path, event.is_directory)

