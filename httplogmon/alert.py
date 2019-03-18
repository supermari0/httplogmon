import datetime


class RequestCountAlert:
    """Alert for request count exceeding a threshold."""

    def __init__(self, rps):
        """Create the alert.

           :param float rps: Average requests per second.
        """
        self.start = datetime.datetime.utcnow(tzinfo=datetime.timezone.utc)
        self.active = True
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
        self.active = False
        self.end = datetime.datetime.utcnow(tzinfo=datetime.timezone.utc)
