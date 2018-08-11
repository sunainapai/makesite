import unittest
import shutil
import os

import makesite
from test import path


class ContentTest(unittest.TestCase):
    def setUp(self):
        self.blog_path = path.temppath('blog')
        self.undated_path = os.path.join(self.blog_path, 'foo.txt')
        self.dated_path = os.path.join(self.blog_path, '2018-01-01-foo.txt')
        self.normal_post_path = os.path.join(self.blog_path, 'baz.txt')
        self.md_post_path = os.path.join(self.blog_path, 'qux.md')
        self.no_md_post_path = os.path.join(self.blog_path, 'qux.txt')

        os.makedirs(self.blog_path)

        with open(self.undated_path, 'w') as f:
            f.write('hello world')

        with open(self.dated_path, 'w') as f:
            f.write('hello world')

        with open(self.normal_post_path, 'w') as f:
            f.write('<!-- a: 1 -->\n<!-- b: 2 -->\nFoo')

        with open(self.md_post_path, 'w') as f:
            f.write('*Foo*')

        with open(self.no_md_post_path, 'w') as f:
            f.write('*Foo*')

    def tearDown(self):
        shutil.rmtree(self.blog_path)

    # Rudimentary mock because unittest.mock is unavailable in Python 2.7.
    def mock(self, *args):
        self.mock_args = args

    def test_content_content(self):
        content = makesite.read_content(self.undated_path)
        self.assertEqual(content['content'], 'hello world')

    def test_content_date(self):
        content = makesite.read_content(self.dated_path)
        self.assertEqual(content['date'], '2018-01-01')

    def test_content_date_missing(self):
        content = makesite.read_content(self.undated_path)
        self.assertEqual(content['date'], '1970-01-01')

    def test_content_slug_dated(self):
        content = makesite.read_content(self.dated_path)
        self.assertEqual(content['slug'], 'foo')

    def test_content_slug_undated(self):
        content = makesite.read_content(self.undated_path)
        self.assertEqual(content['slug'], 'foo')

    def test_content_headers(self):
        content = makesite.read_content(self.normal_post_path)
        self.assertEqual(content['a'], '1')
        self.assertEqual(content['b'], '2')
        self.assertEqual(content['content'], 'Foo')

    def test_markdown_rendering(self):
        content = makesite.read_content(self.md_post_path)
        self.assertEqual(content['content'], '<p><em>Foo</em></p>\n')

    def test_markdown_import_error(self):
        makesite._test = 'ImportError'
        original_log = makesite.log

        makesite.log = self.mock
        self.mock_args = None
        content = makesite.read_content(self.md_post_path)

        makesite._test = None
        makesite.log = original_log

        self.assertEqual(content['content'], '*Foo*')
        self.assertEqual(self.mock_args,
                         ('WARNING: Cannot render Markdown in {}: {}',
                          self.md_post_path, 'Error forced by test'))

    def test_no_markdown_rendering(self):
        content = makesite.read_content(self.no_md_post_path)
        self.assertEqual(content['content'], '*Foo*')

    def test_no_markdown_import_error(self):
        makesite._test = 'ImportError'
        original_log = makesite.log

        makesite.log = self.mock
        self.mock_args = None
        content = makesite.read_content(self.no_md_post_path)

        makesite._test = None
        makesite.log = original_log

        self.assertEqual(content['content'], '*Foo*')
        self.assertIsNone(self.mock_args)
