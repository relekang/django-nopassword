# django-nopassword
[![Build Status](https://travis-ci.org/relekang/django-nopassword.svg?branch=master)](https://travis-ci.org/relekang/django-nopassword)
[![PyPi version](https://pypip.in/v/django-nopassword/badge.png)](https://crate.io/packages/django-nopassword/)

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
    'django_nopassword',
    ...
)
```

Set the authentication backend to *EmailBackend*

    AUTHENTICATION_BACKENDS = ( 'django_nopassword.backends.EmailBackend', )

Add urls to your *urls.py*

```python
urlpatterns = patterns('',
    ...
    url(r'^accounts/', include('django_nopassword.urls')),
    ...
)
```

## Tests
Run with `python setup.py test`.
To run with sqlite add `USE_SQLITE = True` in tests/local.py
