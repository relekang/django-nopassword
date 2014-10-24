# django-nopassword
[![Build Status](https://travis-ci.org/relekang/django-nopassword.svg?branch=master)](https://travis-ci.org/relekang/django-nopassword)
[![PyPi version](https://pypip.in/v/django-nopassword/badge.png)](https://crate.io/packages/django-nopassword/)
[![Wheel Status](https://pypip.in/wheel/django-nopassword/badge.svg)](https://pypi.python.org/pypi/django-nopassword/)
[![Downloads](https://pypip.in/download/django-nopassword/badge.svg)](https://pypi.python.org/pypi/django-nopassword/)
[![Requirements Status](https://requires.io/github/relekang/django-nopassword/requirements.svg?branch=master)](https://requires.io/github/relekang/django-nopassword/requirements/?branch=master)
[![License](https://pypip.in/license/django-nopassword/badge.svg)](https://pypi.python.org/pypi/django-nopassword/)

This project was originally inspired by [Is it time for password-less login?](http://notes.xoxco.com/post/27999787765/is-it-time-for-password-less-login) by [Ben Brown](http://twitter.com/benbrown)

## Installation
Run this command to install django-nopassword

    pip install django-nopassword

### Requirements
Django >= 1.4 (1.5 custom user is supported)

## Usage
Add the app to installed apps

```python
INSTALLED_APPS = (
    ...
    'nopassword',
    ...
)
```

Set the authentication backend to *EmailBackend*

    AUTHENTICATION_BACKENDS = ( 'nopassword.backends.EmailBackend', )

Add urls to your *urls.py*

```python
urlpatterns = patterns('',
    ...
    url(r'^accounts/', include('nopassword.urls')),
    ...
)
```

### Settings
Information about the available settings can be found in the [docs](http://django-nopassword.readthedocs.org/en/latest/#settings)

## Tests
Run with `python setup.py test`.
To run with sqlite add `USE_SQLITE = True` in tests/local.py

--------
MIT © Rolf Erik Lekang
