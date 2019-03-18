import collections
import datetime

from httplogmon.storage.stats import LogStats


class SimpleLogStorage:
    """A simple in-memory storage implementation for log entries.

       This class does not cache any statistics about the log data.
    """

    # TODO You don't want to actually store all the log entries in mem, just
    # update stats
    # Required:
    # - Sections with most hits
    # - 2 minute window of counts cached
    # - Average requests per second
    # Interesting statistics:
    # - Requests per second, % of responses by code, median response size,
    # total kB transferred
    def __init__(self):
        # Deques have append and pop O(1) from either direction, use this
        # instead of a list
        self.last_two_minutes = collections.deque()
        self.last_ten_seconds = collections.deque()
        self.active_alert = None
        self.old_alerts = []

    def __str__(self):
        return self.__dict__

    @staticmethod
    def _purge_stale_entries(entries, limit):
        """Remove any entries prior to the time limit from the deque."""
        while True:
            if len(entries) == 0:
                return
            if entries[0].timestamp > limit:
                return
            entries.popleft()

    def stats_and_purge(self):
        stats = {}
        now = datetime.datetime.utcnow(datetime.timezone.utc)

        # purge any stale log data. deque stays sorted assuming logs are in
        # order by timestamp
        self._purge_stale_entries(self.last_two_minutes,
                                  now - datetime.timedelta(minutes=2))
        self._purge_stale_entries(self.last_ten_seconds,
                                  now - datetime.timedelta(seconds=10))

        stats["rps_two_minutes"] = len(self.last_two_minutes) / 120
        stats["rps_ten_seconds"] = len(self.last_ten_seconds) / 10

        counts_by_section = collections.defaultdict(int)
        counts_by_response_code = collections.defaultdict(int)
        bytes_sent = 0

        for entry in self.last_ten_seconds:
            counts_by_section[entry.section] += 1
            counts_by_response_code[entry.status] += 1
            bytes_sent += entry.n_bytes

        stats['counts_by_section'] = counts_by_section
        stats['counts_by_response_code'] = counts_by_response_code
        stats['bytes_sent'] = bytes_sent

        # TODO Add the alert?

        return LogStats(**stats)

    def add_log_entry(self, entry):
        now = datetime.datetime.utcnow(datetime.timezone.utc)
        tdelta = now - entry.timestamp

        two_minute_delta = datetime.timedelta(minutes=2)
        ten_second_delta = datetime.timedelta(seconds=10)

        if tdelta <= two_minute_delta:
            self.last_two_minutes.append(entry)
            # skip 10 second check if the outer condition does not pass
            if tdelta <= ten_second_delta:
                self.last_ten_seconds.append(entry)
