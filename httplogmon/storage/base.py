"""Base class for storage of log data."""
import abc

class LogStorage(abc.ABC):

    @abc.abstractmethod
    def add_log_entry(self, entry):
        """Add a log entry to storage and update metrics.

           :param httplogmon.text.HTTPLogEntry entry
        """

class SimpleLogStorage:

    # TODO You don't want to actually store all the log entries in mem, just
    # update stats
    def __init__(self):
        self.log_entries = []

    def add_log_entry(self, entry):
        self.log_entries.append(entry)


LogStorage.register(SimpleLogStorage)
