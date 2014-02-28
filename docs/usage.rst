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