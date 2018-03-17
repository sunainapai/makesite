import unittest
import shutil
import os
import makesite
from test import path

class PagesTest(unittest.TestCase):
    def setUp(self):
        self.site_path = path.temppath('site')

    def tearDown(self):
        shutil.rmtree(self.site_path)

    def test_list(self):
        posts = [{'content': 'Foo'}, {'content': 'Bar'}]
        dst = os.path.join(self.site_path, 'list.txt')
        list_layout = '<div>{{ content }}</div>'
        item_layout = '<p>{{ content }}</p>'
        makesite.make_list(posts, dst, list_layout, item_layout)
        with open(os.path.join(self.site_path, 'list.txt')) as f:
            self.assertEqual(f.read(), '<div><p>Foo</p><p>Bar</p></div>')

    def test_list_params(self):
        posts = [{'content': 'Foo', 'title': 'foo'},
                 {'content': 'Bar', 'title': 'bar'}]
        dst = os.path.join(self.site_path, 'list.txt')
        list_layout = '<div>{{ key }}:{{ title }}:{{ content }}</div>'
        item_layout = '<p>{{ key }}:{{ title }}:{{ content }}</p>'
        makesite.make_list(posts, dst, list_layout, item_layout,
                           key='val', title='lorem')
        with open(os.path.join(self.site_path, 'list.txt')) as f:
            text = f.read()
        self.assertEqual(text,
            '<div>val:lorem:<p>val:foo:Foo</p><p>val:bar:Bar</p></div>')

    def test_dst_params(self):
        posts = [{'content': 'Foo'}, {'content': 'Bar'}]
        dst = os.path.join(self.site_path, '{{ key }}.txt')
        list_layout = '<div>{{ content }}</div>'
        item_layout = '<p>{{ content }}</p>'
        makesite.make_list(posts, dst, list_layout, item_layout, key='val')

        expected_path = os.path.join(self.site_path, 'val.txt')
        self.assertTrue(os.path.isfile(expected_path))
        with open(expected_path) as f:
            self.assertEqual(f.read(), '<div><p>Foo</p><p>Bar</p></div>')
