# django-nopassword
[![CircleCI](https://circleci.com/gh/relekang/django-nopassword.svg?style=svg)](https://circleci.com/gh/relekang/django-nopassword)

_Authentication backend for django that uses a one time code instead of passwords._

This project was originally inspired by [Is it time for password-less login?](http://notes.xoxco.com/post/27999787765/is-it-time-for-password-less-login) by [Ben Brown](http://twitter.com/benbrown)

## Installation
Run this command to install django-nopassword

    pip install django-nopassword

### Requirements
Django >= 1.11 (custom user is supported)

## Usage
Add the app to installed apps

```python
INSTALLED_APPS = (
    ...
    'nopassword',
    ...
)
```

Add the authentication backend *EmailBackend*

```python
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `nopassword`
    'django.contrib.auth.backends.ModelBackend',

    # Send login codes via email
    'nopassword.backends.email.EmailBackend',
)
```

Add urls to your *urls.py*

```python
urlpatterns = patterns('',
    ...
    url(r'^accounts/', include('nopassword.urls')),
    ...
)
```

### REST API

To use the REST API, *djangorestframework* must be installed

    pip install djangorestframework

Add rest framework to installed apps

```python
INSTALLED_APPS = (
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'nopassword',
    ...
)
```

Add *TokenAuthentication* to default authentication classes

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}
```

Add urls to your *urls.py*

```python
urlpatterns = patterns('',
    ...
    url(r'^api/accounts/', include('nopassword.rest.urls')),
    ...
)
```

You will have the following endpoints available:

- `/api/accounts/login/` (POST)
  - username
  - next (optional, will be returned in `/api/accounts/login/code/` to be handled by the frontend)
  - Sends a login code to the user
- `/api/accounts/login/code/` (POST)
  - code
  - Returns `key` (authentication token) and `next` (provided by `/api/accounts/login/`)
- `/api/accounts/logout/` (POST)
  - Performs logout

### Settings
Information about the available settings can be found in the [docs](http://django-nopassword.readthedocs.org/en/latest/#settings)

## Tests
Run with `python setup.py test`.

--------
MIT © Rolf Erik Lekang
