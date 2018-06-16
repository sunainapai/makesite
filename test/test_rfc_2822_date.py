import unittest
import makesite


class RFC822DateTest(unittest.TestCase):

    def test_epoch(self):
        self.assertEqual(makesite.rfc_2822_format('1970-01-01'),
                         'Thu, 01 Jan 1970 00:00:00 +0000')

    def test_2018_06_16(self):
        self.assertEqual(makesite.rfc_2822_format('2018-06-16'),
                         'Sat, 16 Jun 2018 00:00:00 +0000')
