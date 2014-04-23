# django-nopassword
[![Build Status](https://travis-ci.org/relekang/django-nopassword.svg?branch=master)](https://travis-ci.org/relekang/django-nopassword)
[![PyPi version](https://pypip.in/v/django-nopassword/badge.png)](https://crate.io/packages/django-nopassword/)

**Disclaimer:** I am writing this to learn more about custom authentication in django. Inspired by [Is it time for password-less login?](http://notes.xoxco.com/post/27999787765/is-it-time-for-password-less-login) by [Ben Brown](http://twitter.com/benbrown)

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

## Settings

##### NOPASSWORD_LOGIN_CODE_TIMEOUT
default: `900` (15 minutes)
Defines how long a login code is valid in seconds.

##### NOPASSWORD_AUTOCOMPLETE
default: `False`
Activates autocomplete in login form. Be aware of the potensial security risk and privacy risk by publicly viewing all usernames and full names. Only do this if you are certain your users would not mind.

##### NOPASSWORD_HIDE_USERNAME
default: `False`
If set to True, the login url will not contain

##### NOPASSWORD_LOGIN_EMAIL_SUBJECT
default: `Login code`

Sets Email Subject for Login Emails

### Django settings used by django-nopassword
##### SERVER_URL
default: `example.com`

##### DEFAULT_FROM_EMAIL
default: `root@example.com`
