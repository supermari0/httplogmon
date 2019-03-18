from httplogmon import text

import unittest


class TestHTTPLogParsing(unittest.TestCase):

    def test_parse_success(self):
        example1 = ('127.0.0.1 - james [09/May/2018:16:00:39 +0000] '
                    '"GET /report HTTP/1.0" 200 123')
        example2 = ('127.0.0.1 - jill [09/May/2018:16:00:41 +0000] '
                    '"GET /api/user HTTP/1.0" 200 234')
        example3 = ('127.0.0.1 - jill [09/May/2018:16:00:41 +0000] '
                    '"GET / HTTP/1.0" 200 234')

        result1 = text.HTTPLogEntry(
            '127.0.0.1',
            'james',
            '09/May/2018:16:00:39 +0000',
            'GET',
            '/report',
            '200',
            '123')
        result2 = text.HTTPLogEntry(
            '127.0.0.1',
            'jill',
            '09/May/2018:16:00:41 +0000',
            'GET',
            '/api/user',
            '200',
            '234')
        result3 = text.HTTPLogEntry(
            '127.0.0.1',
            'jill',
            '09/May/2018:16:00:41 +0000',
            'GET',
            '/',
            '200',
            '234')

        self.assertEqual(result1, text.parse_http_log_line(example1))
        self.assertEqual(result2, text.parse_http_log_line(example2))
        self.assertEqual(result3, text.parse_http_log_line(example3))
        self.assertEqual('/report', result1.section)
        self.assertEqual('/api', result2.section)
        self.assertEqual('/', result3.section)
