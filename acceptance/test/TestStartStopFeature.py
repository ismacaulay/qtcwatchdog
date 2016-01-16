from acceptance.harness.acceptance_test import WatchdogAcceptanceTest


class TestStartStopFeature(WatchdogAcceptanceTest):

    def test_willStartObserverWhenWatchdogStarted(self):
        self.create_and_start_watchdog()

        self.assertTrue(self.fs_observer.running)

    def test_willStopObserverWhenWatchdogStopped(self):
        self.create_and_start_watchdog()

        self.watchdog.stop()

        self.assertFalse(self.fs_observer.running)

    def test_willJoinObserverThreadWhenWatchdogStopped(self):
        self.create_and_start_watchdog()

        self.watchdog.stop()

        self.assertTrue(self.fs_observer.joined)
