import os
from setuptools import setup, find_packages
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'

setup(
    name = "django-nopassword",
    version = '0.1.2',
    url='http://github.com/relekang/django-nopassword',
    author = 'Rolf Erik Lekang',
    author_email = 'me@rolflekang.com',
    description = 'Authentication backend for django that uses email verification instead of passwords',
    packages = find_packages(exclude='tests'),
    tests_require=[
        'django>=1.3',
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
)