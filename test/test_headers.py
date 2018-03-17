import unittest
import makesite


class HeaderTest(unittest.TestCase):
    """Tests for read_headers() function."""

    def test_single_header(self):
        text = '<!-- key1: val1 -->'
        headers = list(makesite.read_headers(text))
        self.assertEqual(headers, [('key1', 'val1', 19)])

    def test_multiple_headers(self):
        text = '<!-- key1: val1 -->\n<!-- key2: val2-->'
        headers = list(makesite.read_headers(text))
        self.assertEqual(headers, [('key1', 'val1', 20), ('key2', 'val2', 38)])

    def test_headers_and_text(self):
        text = '<!-- a: 1 -->\n<!-- b: 2 -->\nFoo\n<!-- c: 3 -->'
        headers = list(makesite.read_headers(text))
        self.assertEqual(headers, [('a', '1', 14), ('b', '2', 28)])

    def test_headers_and_blank_line(self):
        text = '<!-- a: 1 -->\n<!-- b: 2 -->\n\n<!-- c: 3 -->\n'
        headers = list(makesite.read_headers(text))
        self.assertEqual(headers, [('a', '1', 14),
                                   ('b', '2', 29),
                                   ('c', '3', 43)])

    def test_multiline_header(self):
        text = '<!--\na: 1 --><!-- b:\n2 -->\n<!-- c: 3\n-->'
        headers = list(makesite.read_headers(text))
        self.assertEqual(headers, [('a', '1', 13),
                                   ('b', '2', 27),
                                   ('c', '3', 40)])

    def test_no_header(self):
        headers = list(makesite.read_headers('Foo'))
        self.assertEqual(headers, [])

    def test_empty_string(self):
        headers = list(makesite.read_headers(''))
        self.assertEqual(headers, [])
