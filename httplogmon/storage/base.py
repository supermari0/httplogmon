"""Base class for storage of log data."""
import abc

from httplogmon.storage.simple import SimpleLogStorage


class LogStorage(abc.ABC):

    @abc.abstractmethod
    def add_log_entry(self, entry):
        """Add a log entry to storage and update metrics.

           :param httplogmon.text.HTTPLogEntry entry
        """

    @abc.abstractmethod
    def stats_and_purge(self):
        """Retrieve interesting statistics about log entries.

           Also remove stale entries from the cache and alert if request count
           exceeds a certain threshold.
        """


LogStorage.register(SimpleLogStorage)
