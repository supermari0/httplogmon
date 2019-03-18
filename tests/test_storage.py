import collections
import datetime
from httplogmon import text
from httplogmon.storage import simple
from httplogmon.storage.stats import LogStats

from unittest import mock, TestCase


class TestSimpleStorage(TestCase):

    @mock.patch.object(simple, 'datetime', mock.Mock(wraps=datetime))
    def test_log_stats(self):
        simple.datetime.datetime.now.return_value = datetime.datetime(
                2018, 5, 9, 16, 0, 42, tzinfo=datetime.timezone.utc)
        entry1 = text.HTTPLogEntry(
            '127.0.0.1',
            'james',
            '09/May/2018:16:00:39 +0000',
            'GET',
            '/report',
            '200',
            '123')
        entry2 = text.HTTPLogEntry(
            '127.0.0.1',
            'jill',
            '09/May/2018:16:00:41 +0000',
            'GET',
            '/api/user',
            '200',
            '234')
        entry3 = text.HTTPLogEntry(
            '127.0.0.1',
            'jill',
            '09/May/2018:16:00:41 +0000',
            'GET',
            '/api/stats',
            '404',
            '234')
        entries = [entry1, entry2, entry3]

        storage = simple.SimpleLogStorage()
        for e in entries:
            storage.add_log_entry(e)

        expected = LogStats(
            3/120,
            3/10,
            collections.defaultdict(int, {'/report': 1,
                                          '/api': 2}),
            collections.defaultdict(int, {200: 2,
                                          404: 1}),
            123 + 234 + 234)
        self.assertEqual(
            expected,
            storage.stats_and_purge())
