import json_field

from distutils.core import setup

description = 'Generic JSON model and form fields.'

try:
    with open('README.rst') as f:
        long_description = f.read()
except IOError:
    long_description = description

setup(
    name = 'django-json-field',
    version = json_field.__version__,
    description = description,
    author = 'Derek Schaefer',
    author_email = 'derek.schaefer@gmail.com',
    url = 'https://github.com/derek-schaefer/django-json-field',
    long_description = long_description,
    packages = ['json_field'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
