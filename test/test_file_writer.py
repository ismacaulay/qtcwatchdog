import os
import unittest
from unittest.mock import patch, mock_open, call

from writer import QtcFileWriter

class TestQtcFileWriter(unittest.TestCase):
   def setUp(self):
      self.path = 'testPath'
      self.projpath = 'testProjPath'
      self.basepaths = [os.path.abspath('basepath1'), os.path.abspath('basepath/two')]

   def test_write(self):
      m = mock_open()
      with patch('writer.open', m):
         list_to_write = ['this is a line\n',
                          'basepath1/this is another line',
                          'basepath/two/this is a third line']
         patient = QtcFileWriter(self.path, self.projpath, self.basepaths)
         patient.write(list_to_write)

      expected = [call(os.path.abspath('this is a line') + '\n'),
                  call(os.path.join(self.basepaths[0], 'this is another line') + '\n'),
                  call(os.path.join(self.basepaths[1], 'this is a third line') + '\n')]
      m.assert_called_once_with(self.path, 'w')
      m().write.assert_has_calls(expected)

   def test_append(self):
      m = mock_open()
      with patch('writer.open', m):
         line = 'this is a line'
         patient = QtcFileWriter(self.path, self.projpath, self.basepaths)
         patient.append(line)

      m.assert_called_once_with(self.path, 'a')
      m().write.assert_called_once_with(line + '\n')

   def test_remove_first(self):
      m = mock_open()
      with patch('writer.open', m):
         m.return_value.readlines.return_value = [
            os.path.abspath('this line'),
            os.path.abspath('the first line'),
            os.path.abspath('the second line'),
            os.path.abspath('the third line'),
            os.path.abspath('the fourth line'),
         ]
         line = os.path.abspath('this line')
         patient = QtcFileWriter(self.path, self.projpath, self.basepaths)
         patient.remove(line)

      m.assert_called_once_with(self.path, 'r+')
      m().seek.assert_called_once_with(0)
      m().write.assert_has_calls([
         call(os.path.abspath('the first line') + '\n'),
         call(os.path.abspath('the second line') + '\n'),
         call(os.path.abspath('the third line') + '\n'),
         call(os.path.abspath('the fourth line') + '\n')])
      m().truncate.assert_called_once_with()

   def test_remove_mid(self):
      m = mock_open()
      with patch('writer.open', m):
         m.return_value.readlines.return_value = [
            os.path.abspath('the first line'),
            os.path.abspath('the second line'),
            os.path.abspath('this line'),
            os.path.abspath('the third line'),
            os.path.abspath('the fourth line'),
         ]
         line = os.path.abspath('this line')
         patient = QtcFileWriter(self.path, self.projpath, self.basepaths)
         patient.remove(line)

      m.assert_called_once_with(self.path, 'r+')
      m().seek.assert_called_once_with(2)
      m().write.assert_has_calls([
         call(os.path.abspath('the third line') + '\n'),
         call(os.path.abspath('the fourth line') + '\n')])
      m().truncate.assert_called_once_with()

   def test_remove_end(self):
      m = mock_open()
      with patch('writer.open', m):
         m.return_value.readlines.return_value = [
            os.path.abspath('the first line'),
            os.path.abspath('the second line'),
            os.path.abspath('the third line'),
            os.path.abspath('the fourth line'),
            os.path.abspath('this line'),
         ]
         line = os.path.abspath('this line')
         patient = QtcFileWriter(self.path, self.projpath, self.basepaths)
         patient.remove(line)

      m.assert_called_once_with(self.path, 'r+')
      m().seek.assert_called_once_with(4)
      m().write.assert_not_called()
      m().truncate.assert_called_once_with()

   def test_remove_not_found(self):
      m = mock_open()
      with patch('writer.open', m):
         m.return_value.readlines.return_value = [
            os.path.abspath('the first line'),
            os.path.abspath('the second line'),
            os.path.abspath('the third line'),
            os.path.abspath('the fourth line'),
         ]
         line = os.path.abspath('this line')
         patient = QtcFileWriter(self.path, self.projpath, self.basepaths)
         patient.remove(line)

      m.assert_called_once_with(self.path, 'r+')
      m().seek.assert_not_called()
      m().write.assert_not_called()
      m().truncate.assert_not_called()

   def test_remove_and_append_first(self):
      m = mock_open()
      with patch('writer.open', m):
         m.return_value.readlines.return_value = [
            os.path.abspath('this line'),
            os.path.abspath('the first line'),
            os.path.abspath('the second line'),
            os.path.abspath('the third line'),
            os.path.abspath('the fourth line'),
         ]
         line_to_remove = os.path.abspath('this line')
         line_to_append = os.path.abspath('append me')
         patient = QtcFileWriter(self.path, self.projpath, self.basepaths)
         patient.remove_and_append(line_to_remove, line_to_append)

      m.assert_called_once_with(self.path, 'r+')
      m().seek.assert_called_once_with(0)
      m().write.assert_has_calls([
         call(os.path.abspath('the first line') + '\n'),
         call(os.path.abspath('the second line') + '\n'),
         call(os.path.abspath('the third line') + '\n'),
         call(os.path.abspath('the fourth line') + '\n'),
         call(os.path.abspath('append me') + '\n'),
         ])
      m().truncate.assert_called_once_with()

   def test_remove_and_append_mid(self):
      m = mock_open()
      with patch('writer.open', m):
         m.return_value.readlines.return_value = [
            os.path.abspath('the first line'),
            os.path.abspath('the second line'),
            os.path.abspath('this line'),
            os.path.abspath('the third line'),
            os.path.abspath('the fourth line'),
         ]
         line_to_remove = os.path.abspath('this line')
         line_to_append = os.path.abspath('append me')
         patient = QtcFileWriter(self.path, self.projpath, self.basepaths)
         patient.remove_and_append(line_to_remove, line_to_append)

      m.assert_called_once_with(self.path, 'r+')
      m().seek.assert_called_once_with(2)
      m().write.assert_has_calls([
         call(os.path.abspath('the third line') + '\n'),
         call(os.path.abspath('the fourth line') + '\n'),
         call(os.path.abspath('append me') + '\n'),
         ])
      m().truncate.assert_called_once_with()

   def test_remove_and_append_end(self):
      m = mock_open()
      with patch('writer.open', m):
         m.return_value.readlines.return_value = [
            os.path.abspath('the first line'),
            os.path.abspath('the second line'),
            os.path.abspath('the third line'),
            os.path.abspath('the fourth line'),
            os.path.abspath('this line'),
         ]
         line_to_remove = os.path.abspath('this line')
         line_to_append = os.path.abspath('append me')
         patient = QtcFileWriter(self.path, self.projpath, self.basepaths)
         patient.remove_and_append(line_to_remove, line_to_append)

      m.assert_called_once_with(self.path, 'r+')
      m().seek.assert_called_once_with(4)
      m().write.assert_called_once_with(os.path.abspath('append me') + '\n')
      m().truncate.assert_called_once_with()

   def test_remove_and_append_not_found(self):
      m = mock_open()
      with patch('writer.open', m):
         m.return_value.readlines.return_value = [
            os.path.abspath('the first line'),
            os.path.abspath('the second line'),
            os.path.abspath('the third line'),
            os.path.abspath('the fourth line'),
         ]
         line_to_remove = os.path.abspath('this line')
         line_to_append = os.path.abspath('append me')
         patient = QtcFileWriter(self.path, self.projpath, self.basepaths)
         patient.remove_and_append(line_to_remove, line_to_append)

      m.assert_called_once_with(self.path, 'r+')
      m().seek.assert_not_called()
      m().write.assert_called_once_with(os.path.abspath('append me') + '\n')
      m().truncate.assert_not_called()
