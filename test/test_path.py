import unittest
import os
import shutil

from test import path

class PathTest(unittest.TestCase):
    def test_temppath(self):
        self.assertTrue(path.temppath())

    def test_move_existing_file(self):
        src = os.path.join(path.temppath(), 'foo.txt')
        dst = os.path.join(path.temppath(), 'bar.txt')
        with open(src, 'w') as f:
            f.write('foo')

        path.move(src, dst)
        self.assertFalse(os.path.isfile(src))
        self.assertTrue(os.path.isfile(dst))

        with open(dst) as f:
            text = f.read()

        os.remove(dst)

        self.assertEqual(text, 'foo')

    def test_move_missing_file(self):
        src = os.path.join(path.temppath(), 'foo.txt')
        dst = os.path.join(path.temppath(), 'bar.txt')
        path.move(src, dst)
        self.assertFalse(os.path.isfile(src))
        self.assertFalse(os.path.isfile(dst))

    def test_move_file_cleanup(self):
        src = os.path.join(path.temppath(), 'foo.txt')
        dst = os.path.join(path.temppath(), 'bar.txt')
        with open(dst, 'w') as f:
            f.write('foo')
        path.move(src, dst)
        self.assertFalse(os.path.isfile(src))
        self.assertFalse(os.path.isfile(dst))

    def test_move_existing_dir(self):
        src = os.path.join(path.temppath(), 'foo')
        srcf = os.path.join(src, 'foo.txt')
        dst = os.path.join(path.temppath(), 'bar')
        dstf = os.path.join(dst, 'foo.txt')

        os.makedirs(src)
        with open(srcf, 'w') as f:
            f.write('foo')

        path.move(src, dst)
        self.assertFalse(os.path.isdir(src))
        self.assertTrue(os.path.isdir(dst))

        with open(dstf) as f:
            text = f.read()

        shutil.rmtree(dst)

        self.assertEqual(text, 'foo')

    def test_move_missing_dir(self):
        src = os.path.join(path.temppath(), 'foo')
        dst = os.path.join(path.temppath(), 'bar')
        path.move(src, dst)
        self.assertFalse(os.path.isdir(src))
        self.assertFalse(os.path.isdir(dst))

    def test_move_dir_cleanup(self):
        src = os.path.join(path.temppath(), 'foo')
        dst = os.path.join(path.temppath(), 'bar')
        os.makedirs(dst)
        path.move(src, dst)
        self.assertFalse(os.path.isdir(src))
        self.assertFalse(os.path.isdir(dst))
