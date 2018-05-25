makesite.py
===========

[![Build Status](https://travis-ci.org/gabfl/makesite.svg?branch=master)](https://travis-ci.org/gabfl/makesite)
[![codecov](https://codecov.io/gh/gabfl/makesite/branch/master/graph/badge.svg)](https://codecov.io/gh/gabfl/makesite)

Take full control of your static website/blog generation by writing your
own simple, lightweight, and magic-free static site generator in
Python. That's right! Reinvent the wheel, fellas!

## Fork

This project is a fork from https://github.com/sunainapai/makesite, please visit the original project for the original Readme.

## Usage

### Requirements

```bash
pip3 install -r requirements.txt
```

### Compile the website

```bash
python3 makesite.py --env dev
cd _site
python3 -m http.server 8000
```

## Features from gabfl/makesite

This fork implements the following features that do not exist in the original version:
 - Uses [Jinja2](http://jinja.pocoo.org/) to render templates
 - Easy customization with variables stored in [vars.py](vars.py)
 - Multiple environments (`dev`, `prod`...) defined in [vars.py](vars.py). A build for a specific environment can be done with `python makesite.py --env prod`
 - Ability to add additional parsing with a file `add_parser.py` (see [add_parser.py.sample](add_parser.py.sample))
 - Date format customization from [vars.py](vars.py)
 - Template variables (`{{ blog_recent }}`, `{{ news_recent }}`...) to show a list of the 5 most recent items in a section

## Credits

[sunainapai](https://github.com/sunainapai) for the original project and [Susam](https://github.com/susam) for the original documentation and the unit tests.

## License

This is free and open source software. You can use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of it,
under the terms of the [MIT License](LICENSE.md).

This software is provided "AS IS", WITHOUT WARRANTY OF ANY KIND,
express or implied. See the [MIT License](LICENSE.md) for details.


## Support

To report bugs, suggest improvements, or ask questions, please visit:
 - <https://github.com/gabfl/makesite/issues> for this fork
 - <https://github.com/sunainapai/makesite/issues> for the original project
