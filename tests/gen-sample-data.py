"""Generate data for httplogmon"""
import datetime

from httplogmon import conf, main, text


if __name__ == '__main__':
    test_data = [
"""127.0.0.1 - james [{timestamp}] "GET /report HTTP/1.0" 200 123
127.0.0.1 - jill [{timestamp}] "GET /api/user HTTP/1.0" 200 234""",
"""127.0.0.1 - frank [{timestamp_later}] "POST /report/stuff HTTP/1.0" 200 34
127.0.0.1 - mary [{timestamp_later}] "POST /api/user HTTP/1.0" 503 12"""
]
    now = datetime.datetime.now(datetime.timezone.utc)
    now_str = now.strftime(text.HTTP_LOG_TIME_FORMAT)
    five_seconds_ago_str = (now - datetime.timedelta(seconds=5)).strftime(
        text.HTTP_LOG_TIME_FORMAT)
    for _ in range(500):
        print(test_data[0].format(timestamp=five_seconds_ago_str))
    for _ in range(200):
        print(test_data[1].format(timestamp_later=now_str))
