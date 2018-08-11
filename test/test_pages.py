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
        with open(os.path.join(self.blog_path, 'header-foo.txt'), 'w') as f:
            f.write('<!-- tag: foo -->Foo')
        with open(os.path.join(self.blog_path, 'header-bar.txt'), 'w') as f:
            f.write('<!-- title: bar -->Bar')
        with open(os.path.join(self.blog_path, 'placeholder-foo.txt'), 'w') as f:
            f.write('<!-- title: foo -->{{ title }}:{{ author }}:Foo')
        with open(os.path.join(self.blog_path, 'placeholder-bar.txt'), 'w') as f:
            f.write('<!-- title: bar --><!-- render: yes -->{{ title }}:{{ author }}:Bar')

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

    def test_content_header_params(self):
        # Test that header params from one post is not used in another
        # post.
        src = os.path.join(self.blog_path, 'header*.txt')
        dst = os.path.join(self.site_path, '{{ slug }}.txt')
        tpl = '{{ title }}:{{ tag }}:{{ content }}'
        makesite.make_pages(src, dst, tpl)
        with open(os.path.join(self.site_path, 'header-foo.txt')) as f:
            self.assertEqual(f.read(), '{{ title }}:foo:Foo')
        with open(os.path.join(self.site_path, 'header-bar.txt')) as f:
            self.assertEqual(f.read(), 'bar:{{ tag }}:Bar')

    def test_content_no_rendering(self):
        # Test that placeholders are not populated in content rendering
        # by default.
        src = os.path.join(self.blog_path, 'placeholder-foo.txt')
        dst = os.path.join(self.site_path, '{{ slug }}.txt')
        tpl = '<div>{{ content }}</div>'
        makesite.make_pages(src, dst, tpl, author='Admin')
        with open(os.path.join(self.site_path, 'placeholder-foo.txt')) as f:
            self.assertEqual(f.read(), '<div>{{ title }}:{{ author }}:Foo</div>')

    def test_content_rendering_via_kwargs(self):
        # Test that placeholders are populated in content rendering when
        # requested in make_pages.
        src = os.path.join(self.blog_path, 'placeholder-foo.txt')
        dst = os.path.join(self.site_path, '{{ slug }}.txt')
        tpl = '<div>{{ content }}</div>'
        makesite.make_pages(src, dst, tpl, author='Admin', render='yes')
        with open(os.path.join(self.site_path, 'placeholder-foo.txt')) as f:
            self.assertEqual(f.read(), '<div>foo:Admin:Foo</div>')

    def test_content_rendering_via_header(self):
        # Test that placeholders are populated in content rendering when
        # requested in content header.
        src = os.path.join(self.blog_path, 'placeholder-bar.txt')
        dst = os.path.join(self.site_path, '{{ slug }}.txt')
        tpl = '<div>{{ content }}</div>'
        makesite.make_pages(src, dst, tpl, author='Admin')
        with open(os.path.join(self.site_path, 'placeholder-bar.txt')) as f:
            self.assertEqual(f.read(), '<div>bar:Admin:Bar</div>')

    def test_rendered_content_in_summary(self):
        # Test that placeholders are populated in summary if and only if
        # content rendering is enabled.
        src = os.path.join(self.blog_path, 'placeholder*.txt')
        post_dst = os.path.join(self.site_path, '{{ slug }}.txt')
        list_dst = os.path.join(self.site_path, 'list.txt')
        post_layout = ''
        list_layout = '<div>{{ content }}</div>'
        item_layout = '<p>{{ summary }}</p>'
        posts = makesite.make_pages(src, post_dst, post_layout, author='Admin')
        makesite.make_list(posts, list_dst, list_layout, item_layout)
        with open(os.path.join(self.site_path, 'list.txt')) as f:
            self.assertEqual(f.read(), '<div><p>{{ title }}:{{ author }}:Foo</p><p>bar:Admin:Bar</p></div>')
