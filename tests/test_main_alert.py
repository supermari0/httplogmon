from httplogmon import conf, main
from httplogmon.storage.simple import SimpleLogStorage
from httplogmon.storage.stats import LogStats

import unittest


class TestAlertLogic(unittest.TestCase):
    """Test alert logic."""

    def _get_mock_storage(self, rps_two_minutes):
        """Return a SimpleLogStorage and a stats object.

           :param int rps_two_minutes: The requests over the last 2 minutes
                                       that the stats object will indicate.
        """
        storage = SimpleLogStorage()
        # alert logic doesn't care about anything other than requests per
        # second for 2 minutes, so we just set those value randomly here
        stats = {
            "rps_two_minutes": rps_two_minutes,
            "rps_ten_seconds": 5.5,
            "counts_by_section": {"/api": 50},
            "counts_by_response_code": {"200": 50},
            "bytes_sent": 5000
        }
        return storage, LogStats(**stats)

    def _override_conf(self):
        """Enforce that config defaults are used during this test case."""
        conf.RPS_ALERT_THRESOLD = conf.DEFAULT_RPS_ALERT_THRESHOLD
        conf.LOG_LOCATION = conf.DEFAULT_LOG_LOCATION

    def test_no_alert(self):
        self._override_conf()
        storage, stats = self._get_mock_storage(5)
        main.update_and_print_alerts(stats, storage)
        self.assertIsNone(storage.active_alert)

    def test_new_alert_no_previous_alert(self):
        self._override_conf()
        storage, stats = self._get_mock_storage(300)
        main.update_and_print_alerts(stats, storage)
        self.assertIsNotNone(storage.active_alert)

    def test_stop_alert(self):
        self._override_conf()

        storage, stats = self._get_mock_storage(300)
        main.update_and_print_alerts(stats, storage)
        self.assertIsNotNone(storage.active_alert)

        _, stats = self._get_mock_storage(5)
        main.update_and_print_alerts(stats, storage)
        self.assertIsNone(storage.active_alert)

    def test_update_alert(self):
        self._override_conf()

        storage, stats = self._get_mock_storage(300)
        main.update_and_print_alerts(stats, storage)
        self.assertIsNotNone(storage.active_alert)

        _, stats = self._get_mock_storage(250)
        main.update_and_print_alerts(stats, storage)
        self.assertIsNotNone(storage.active_alert)
