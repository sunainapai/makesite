import unittest
import os
import shutil
import makesite
from test import path

class PagesTest(unittest.TestCase):
    def setUp(self):
        self.blog_path = path.temppath('blog')
        self.site_path = path.temppath('site')
        os.makedirs(self.blog_path)

        with open(os.path.join(self.blog_path, 'foo.txt'), 'w') as f:
            f.write('Foo')
        with open(os.path.join(self.blog_path, 'bar.txt'), 'w') as f:
            f.write('Bar')
        with open(os.path.join(self.blog_path, '2018-01-01-foo.txt'), 'w') as f:
            f.write('Foo')
        with open(os.path.join(self.blog_path, '2018-01-02-bar.txt'), 'w') as f:
            f.write('Bar')

    def tearDown(self):
        shutil.rmtree(self.blog_path)
        shutil.rmtree(self.site_path)

    def test_pages_undated(self):
        src = os.path.join(self.blog_path, '[fb]*.txt')
        dst = os.path.join(self.site_path, '{{ slug }}.txt')
        tpl = '<div>{{ content }}</div>'
        makesite.make_pages(src, dst, tpl)
        with open(os.path.join(self.site_path, 'foo.txt')) as f:
            self.assertEqual(f.read(), '<div>Foo</div>')
        with open(os.path.join(self.site_path, 'bar.txt')) as f:
            self.assertEqual(f.read(), '<div>Bar</div>')

    def test_pages_dated(self):
        src = os.path.join(self.blog_path, '2*.txt')
        dst = os.path.join(self.site_path, '{{ slug }}.txt')
        tpl = '<div>{{ content }}</div>'
        makesite.make_pages(src, dst, tpl)
        with open(os.path.join(self.site_path, 'foo.txt')) as f:
            self.assertEqual(f.read(), '<div>Foo</div>')
        with open(os.path.join(self.site_path, 'bar.txt')) as f:
            self.assertEqual(f.read(), '<div>Bar</div>')

    def test_pages_layout_params(self):
        src = os.path.join(self.blog_path, '2*.txt')
        dst = os.path.join(self.site_path, '{{ slug }}.txt')
        tpl = '<div>{{ slug }}:{{ title }}:{{ date }}:{{ content }}</div>'
        makesite.make_pages(src, dst, tpl, title='Lorem')
        with open(os.path.join(self.site_path, 'foo.txt')) as f:
            self.assertEqual(f.read(), '<div>foo:Lorem:2018-01-01:Foo</div>')
        with open(os.path.join(self.site_path, 'bar.txt')) as f:
            self.assertEqual(f.read(), '<div>bar:Lorem:2018-01-02:Bar</div>')

    def test_pages_return_value(self):
        src = os.path.join(self.blog_path, '2*.txt')
        dst = os.path.join(self.site_path, '{{ slug }}.txt')
        tpl = '<div>{{ content }}</div>'
        posts = makesite.make_pages(src, dst, tpl)
        self.assertEqual(len(posts), 2)
        self.assertEqual(posts[0]['date'], '2018-01-02')
        self.assertEqual(posts[1]['date'], '2018-01-01')
