import datetime
from httplogmon.text import HTTP_LOG_TIME_FORMAT


class RequestCountAlert:
    """Alert for request count exceeding a threshold."""

    def __init__(self, rps):
        """Create the alert.

           :param float rps: Average requests per second.
        """
        self.start = datetime.datetime.now(datetime.timezone.utc)
        self.end = None
        self.current_rps = rps
        self.peak_rps = rps

    def update(self, rps):
        """Update the alert with a new average.

           :param float rps: Average requests per second.
        """
        if rps > self.peak_rps:
            self.peak_rps = rps
        self.current_rps = rps

    def close(self):
        """Close the alert."""
        self.end = datetime.datetime.now(datetime.timezone.utc)

    def __str__(self):
        rep = 'ALERT START: ' + self.start.strftime(HTTP_LOG_TIME_FORMAT)
        rep += ', Current average requests/second: ' + str(self.current_rps)
        rep += ', peak average requests/second: ' + str(self.peak_rps)
        return rep
