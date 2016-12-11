# django-nopassword
[![CircleCI](https://circleci.com/gh/relekang/django-nopassword.svg?style=svg)](https://circleci.com/gh/relekang/django-nopassword)

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

    AUTHENTICATION_BACKENDS = ( 'nopassword.backends.email.EmailBackend', )

Add urls to your *urls.py*

```python
urlpatterns = patterns('',
    ...
    url(r'^accounts/', include('nopassword.urls'), namespace='nopassword'),
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
