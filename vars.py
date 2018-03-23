site_vars = {
    'envs': {
        'default': {
            'base_path': '',
            'site_url': 'http://localhost:8000',
            'documentroot': '_site',
        },
        'dev': {
            'base_path': '',
            'site_url': 'http://localhost:8000',
            'documentroot': '_site',
        },
        'prod':
        {
            'base_path': '',
            'site_url': 'http://localhost:8000',
            'documentroot': '_site',
        },
    },
    'subtitle': 'Lorem Ipsum',
    'author': 'Admin',
    'html_lang': 'en',
    'date_format': '%b. %e, %Y',
    'sections': {
        'blog', 'news'
    },
    'blog': {
        'name': 'Blog',
        'path': 'blog',
        'files_extension': '.md',
        'recent_items': 5,
    },
    'news': {
        'name': 'News',
        'path': 'news',
        'files_extension': '.html',
        'recent_items': 5,
    },
    'contact': {
        'name': 'Contact',
        'path': 'contact',
    },
    'about': {
        'name': 'About',
        'path': 'about',
    }
}
