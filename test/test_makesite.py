
import unittest
import tempfile
import os

import makesite


class Test(unittest.TestCase):

    md_file = 'content/blog/2018-01-01-proin-quam.md'
    html_file = 'content/news/2018-01-02-vivamus-purus.html'

    def test_get_environment_name(self):
        self.assertEqual(makesite.get_environment_name(), 'default')

    def test_import_additional_parser(self):
        self.assertIsNone(makesite.import_additional_parser())

    def test_fread(self):
        self.assertIsInstance(makesite.fread('content/about.html'), str)

    def test_fwrite(self):
        file_ = tempfile.NamedTemporaryFile()
        self.assertIsNone(makesite.fwrite(file_.name, 'some content'))

    def test_log(self):
        self.assertIsNone(makesite.log('some log'))

    def test_truncate(self):
        self.assertEqual(makesite.truncate(
            '    some string   '), 'some string')

    def test_read_content(self):
        makesite.date_format = '%b. %e, %Y'
        content = makesite.read_content(self.md_file)

        self.assertIsInstance(content, dict)
        self.assertEqual(content['date'], 'Jan.  1, 2018')
        self.assertEqual(content['date_ymd'], '2018-01-01')
        self.assertEqual(content['date_ymd'], '2018-01-01')
        self.assertEqual(content['slug'], 'proin-quam')

    def test_separate_content_and_variables(self):
        a, b = makesite.separate_content_and_variables(
            'a{# /variables #}b')
        self.assertEqual(a, 'a')
        self.assertEqual(b, 'b')

    def test_separate_content_and_variables_2(self):
        a, b = makesite.separate_content_and_variables(
            'b')
        self.assertEqual(a, '')
        self.assertEqual(b, 'b')

    def test_format_date(self):
        makesite.date_format = '%b. %e, %Y'
        self.assertEqual(makesite.format_date('2018-01-01'), 'Jan.  1, 2018')

    def test_render(self):
        makesite.date_format = '%b. %e, %Y'
        content = makesite.read_content(self.md_file)
        self.assertIsInstance(makesite.render(content['content']), str)

    def test_make_list(self):
        section_pages = makesite.make_pages(
            'content/blog/*.md', '_site/blog/{{ slug }}/index.html', None, blog='blog')

        a = makesite.make_list(section_pages, '_site/blog/index.html',
                               makesite.fread('layout/list.html'), makesite.fread('layout/item.html'), None, blog='blog', title='blog')

        self.assertIsNone(a)

    def test_get_title_and_summary(self):
        title, extract = makesite.get_title_and_summary(self.html_file)
        self.assertEqual(title, '{{ title }}')
        self.assertEqual(
            extract, 'Vivamus purus tellus, facilisis in sapien quis, ullamcorper lacinia neque. Morbi tincidunt ac leo sit amet auctor. Donec dolor mauris, lobortis eget faucibus sit amet,')

    def test_get_content_path(self):
        self.assertEqual(makesite.get_content_path(
            'blog', 'blog/'), 'content/blog')
        self.assertEqual(makesite.get_content_path(
            'blog'), 'content/blog')
        self.assertEqual(makesite.get_content_path(
            'news'), 'content/news')
        self.assertEqual(makesite.get_content_path(
            'name', 'some/other/path'), 'content/some/other/path')
