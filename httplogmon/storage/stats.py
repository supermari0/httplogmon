# TODO This should be a dataclass in Python 3.7
class LogStats:
    """Statistics about logs."""

    def __init__(self, rps_two_minutes, rps_ten_seconds, counts_by_section,
                 counts_by_response_code, bytes_sent):
        """Construct log statistics.

           :param float rps_two_minutes: Average requests per second for the
                                         last two minutes.
           :param float rps_ten_seconds: Average requests per second for the
                                         last 10 seconds.
           :param dict counts_by_section: Request counts per section for the
                                          last 10 seconds.
           :param dict counts_by_response_code: Response count by response code
                                                for the last 10 seconds.
           :param int bytes_sent: Total bytes sent for the last 10 seconds.
        """
        self.rps_two_minutes = rps_two_minutes
        self.rps_ten_seconds = rps_ten_seconds
        self.counts_by_section = counts_by_section
        self.counts_by_response_code = counts_by_response_code
        self.bytes_sent = bytes_sent

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
