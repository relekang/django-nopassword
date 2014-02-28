.. django_nopassword documentation master file, created by
   sphinx-quickstart on Thu Feb 27 20:16:47 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django_nopassword's documentation!
=============================================

Release v\ |version|. (:ref:`Installation <install>`)

Installation
------------
Run this command to install django-nopassword::

    pip install django-nopassword

Requirements:
Django >= 1.4 (1.5 custom user is supported)

Usage
-----
Add the app to installed apps::

    INSTALLED_APPS = (
        'django_nopassword',
    )

Set the authentication backend to *EmailBackend*::

    AUTHENTICATION_BACKENDS = ( 'django_nopassword.backends.EmailBackend', )

Add urls to your *urls.py*::

    urlpatterns = patterns('',
        url(r'^accounts/', include('django_nopassword.urls')),
    )