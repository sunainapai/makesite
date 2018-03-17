import unittest
import os
import shutil

import makesite
from test import path


class FileIOTest(unittest.TestCase):
    """Tests for file I/O functions."""

    def test_fread(self):
        text = 'foo\nbar\n'
        filepath = path.temppath('foo.txt')
        with open(filepath, 'w') as f:
            f.write(text)
        text_read = makesite.fread(filepath)
        os.remove(filepath)
        self.assertEqual(text_read, text)

    def test_fwrite(self):
        text = 'baz\nqux\n'
        filepath = path.temppath('foo.txt')
        makesite.fwrite(filepath, text)
        with open(filepath) as f:
            text_read = f.read()
        os.remove(filepath)
        self.assertEqual(text_read, text)

    def test_fwrite_makedir(self):
        text = 'baz\nqux\n'
        dirpath = path.temppath('foo', 'bar')
        filepath = os.path.join(dirpath, 'foo.txt')
        makesite.fwrite(filepath, text)
        with open(filepath) as f:
            text_read = f.read()
        self.assertTrue(os.path.isdir(dirpath))
        shutil.rmtree(path.temppath('foo'))
        self.assertEqual(text_read, text)
