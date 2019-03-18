"""Helpers to perform various operations on text."""
import datetime
import re

# Regular expression for parsing an HTTP log line.
# TODO Make some of these matches more specific - date format, request method,
# etc, or handle that in the HTTPLogEntry constructor
# TODO Use named groups.
# TODO Don't use regexp; parse in 1 pass.
HTTP_LOG_LINE_REGEXP = (r'^(.+) - (.+) \[(.+)\] \"([A-Z]+) (\/.*) .+\" '
                        r'([0-9]{3}) ([0-9]+)$')

# TODO The locale's abbreviated month (Jan, Feb, ..., May, ...) is used
# for the month format. This can be configured by the web server. This
# won't work if the system locale is misconfigured or if the full month
# is used. However, this should work with default Apache settings if
# the system locale matches the locale used by the web server.
HTTP_LOG_TIME_FORMAT = '%d/%b/%Y:%H:%M:%S %z'


# TODO This can be a dataclass in Python 3.7 if you move datetime conversion
# out.
class HTTPLogEntry:

    def __init__(self, host, user, timestamp, method, path, status, n_bytes):
        """Construct a log entry from an HTTP access log.

           :param str host: DNS or IP of the remote host makin an HTTP request.
           :param str user: Username.
           :param str timestamp: Timestamp of the request.
           :param str method: Request method.
           :param str path: Request path.
           :param int status: Response code.
           :param int n_bytes: Number of bytes transferred in the response.

           :raises HTTPLogParseError if the timestamp cannot be converted to a
               datetime object correctly
        """
        self.host = host
        self.user = user

        time_format = '%d/%b/%Y:%H:%M:%S %z'
        try:
            dt = datetime.datetime.strptime(timestamp, time_format)
            self.timestamp = dt
        except ValueError:
            raise HTTPLogParseError('HTTP log entry timestamp format error: '
                                    f'{timestamp}')
        self.method = method

        # TODO In addition to "path", track "section" as defined in the problem
        # TODO Convert status, n_bytes to ints
        self.path = path
        split_path = path.split('/')
        if len(split_path) >= 2:
            self.section = '/' + split_path[1]
        else:
            self.section = '/'

        try:
            self.status = int(status)
        except ValueError:
            raise HTTPLogParseError(f'HTTP status code format error: {status}')
        try:
            self.n_bytes = int(n_bytes)
        except ValueError:
            raise HTTPLogParseError(f'HTTP resp size format error: {n_bytes}')

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class HTTPLogParseError(Exception):
    """Raised when an HTTP log entry cannot be parsed correctly."""
    pass


def parse_http_log_line(line):
    """Parse an HTTP access log line and return useful data.

       :param str line: An HTTP access log line.
       :returns HTTPLogEntry

       :raises HTTPLogParseError
    """
    match = re.fullmatch(HTTP_LOG_LINE_REGEXP, line)
    if match is None:
        raise HTTPLogParseError(f'HTTP log entry is malformatted: {line}')

    # TODO is partial match possible with fullmatch? catch exception if so
    host = match.group(1)
    user = match.group(2)
    timestamp_str = match.group(3)
    method = match.group(4)
    path = match.group(5)
    status = match.group(6)
    n_bytes = match.group(7)

    return HTTPLogEntry(
        host,
        user,
        timestamp_str,
        method,
        path,
        status,
        n_bytes)
