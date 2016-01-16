import unittest, mock
from watcher import ProjectWatcher, InotifyError


class TestProjectWatcher(unittest.TestCase):

    def setUp(self):
        self.running_patcher = mock.patch('watcher.running')
        self.addCleanup(self.running_patcher.stop)
        self.mock_running = self.running_patcher.start()
        self.mock_running.side_effect = [True, False]

    @mock.patch('watcher.Observer')
    @mock.patch('updater.QtcUpdater')
    def test_willScheduleObserverWithProjectPathOnCreation(self, mock_updater, mock_observer_obj):
        mock_observer = mock_observer_obj.return_value

        ProjectWatcher('project/path', mock_updater)

        mock_observer.schedule.assert_called_once_with(mock.ANY, 'project/path', recursive=True)

    @mock.patch('time.sleep')
    @mock.patch('watcher.Observer')
    @mock.patch('updater.QtcUpdater')
    def test_willStartObserverOnStart(self, mock_updater, mock_observer_obj, mock_sleep):
        mock_observer = mock_observer_obj.return_value

        patient = ProjectWatcher('project_path', mock_updater)
        patient.start()

        mock_observer.start.assert_called_once_with()

    @mock.patch('watcher.Observer')
    @mock.patch('updater.QtcUpdater')
    def test_willRaiseExceptionWithInoitfyErrorOnStart(self, mock_updater, mock_observer_obj):
        def raise_os_error():
            raise OSError('inotify watch limit reached')
        mock_observer = mock_observer_obj.return_value
        mock_observer.start.side_effect = raise_os_error

        patient = ProjectWatcher('project_path', mock_updater)

        self.assertRaises(InotifyError, patient.start)

    @mock.patch('watcher.Observer')
    @mock.patch('updater.QtcUpdater')
    def test_willRaiseOsErrorWhenNotInotifyError(self, mock_updater, mock_observer_obj):
        def raise_os_error():
            raise OSError('other os error')
        mock_observer = mock_observer_obj.return_value
        mock_observer.start.side_effect = raise_os_error

        patient = ProjectWatcher('project_path', mock_updater)

        self.assertRaises(OSError, patient.start)

    @mock.patch('time.sleep')
    @mock.patch('watcher.Observer')
    @mock.patch('updater.QtcUpdater')
    def test_willSleepForOneSecondOnStart(self, mock_updater, mock_observer_obj, mock_sleep):
        patient = ProjectWatcher('project_path', mock_updater)
        patient.start()

        mock_sleep.assert_called_once_with(1)


    @mock.patch('time.sleep')
    @mock.patch('watcher.Observer')
    @mock.patch('updater.QtcUpdater')
    def test_willUpdateFilesEveryLoopIteration(self, mock_updater, mock_observer_obj, mock_sleep):
        self.mock_running.side_effect = [True, True, True, False]

        patient = ProjectWatcher('project_path', mock_updater)
        patient.start()

        self.assertEqual(mock_updater.update_files.call_count, 3)

    @mock.patch('time.sleep')
    @mock.patch('watcher.Observer')
    @mock.patch('updater.QtcUpdater')
    def test_willQuitLoopOnKeyboardInterrupt(self, mock_updater, mock_observer_obj,  mock_sleep):
        def raise_keyboard_interrupt(*args, **kwargs):
            raise KeyboardInterrupt()

        self.mock_running.side_effect = None
        mock_sleep.side_effect = raise_keyboard_interrupt

        patient = ProjectWatcher('project_path', mock_updater)
        patient.start()

        mock_sleep.assert_called_once_with(1)

    @mock.patch('watcher.Observer')
    @mock.patch('updater.QtcUpdater')
    def test_willStopAndJoinObserverOnStop(self, mock_updater, mock_observer_obj):
        mock_observer = mock_observer_obj.return_value

        patient = ProjectWatcher('project_path', mock_updater)
        patient.stop()

        mock_observer.stop.assert_called_once_with()
        mock_observer.join.assert_called_once_with()

    @mock.patch('updater.QtcUpdater')
    def test_eventHandlerWillAddPathOnCreatedEvent(self, mock_updater):
        patient = ProjectWatcher.EventHandler(mock_updater)

        mock_event = mock.MagicMock()
        mock_event.src_path = 'helloWorld'
        mock_event.is_directory = False

        patient.on_created(mock_event)

        mock_updater.add.assert_called_once_with('helloWorld', False)

    @mock.patch('updater.QtcUpdater')
    def test_eventHandlerWillRemovePathOnDeletedEvent(self, mock_updater):
        patient = ProjectWatcher.EventHandler(mock_updater)

        mock_event = mock.MagicMock()
        mock_event.src_path = 'helloWorld'
        mock_event.is_directory = False

        patient.on_deleted(mock_event)

        mock_updater.remove.assert_called_once_with('helloWorld', False)

    @mock.patch('updater.QtcUpdater')
    def test_eventHandlerWillMovePathOnMovedEvent(self, mock_updater):
        patient = ProjectWatcher.EventHandler(mock_updater)

        mock_event = mock.MagicMock()
        mock_event.src_path = 'helloWorld'
        mock_event.dest_path = 'destination'
        mock_event.is_directory = True

        patient.on_moved(mock_event)

        mock_updater.move.assert_called_once_with('helloWorld', 'destination', True)


if __name__ == '__main__':
    unittest.main()


