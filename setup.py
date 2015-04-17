import os
from setuptools import setup, find_packages

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'


def _read_long_description():
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except ImportError:
        return None


setup(
    name="django-nopassword",
    version='1.3.1',
    url='http://github.com/relekang/django-nopassword',
    author='Rolf Erik Lekang',
    author_email='me@rolflekang.com',
    description='Authentication backend for django that uses a one time code instead of passwords',
    long_description=_read_long_description(),
    packages=find_packages(exclude='tests'),
    install_require=[
        'django>=1.4',
    ],
    tests_require=[
        'django>=1.4',
        'twilio==4.0.0',
        'mock>=1.0'
    ],
    license='MIT',
    test_suite='runtests.runtests',
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ]
)
