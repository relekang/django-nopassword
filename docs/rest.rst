REST API
--------
To use the REST API, *djangorestframework* must be installed::

    pip install djangorestframework

Add rest framework to installed apps::

    INSTALLED_APPS = (
        ...
        'rest_framework',
        'rest_framework.authtoken',
        'nopassword',
        ...
    )

Add *TokenAuthentication* to default authentication classes::

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
        )
    }

Add urls to your *urls.py*::

    urlpatterns = patterns('',
        ...
        url(r'^api/accounts/', include('nopassword.rest.urls')),
        ...
    )

You will have the following endpoints available:

- `/api/accounts/login/` (POST)
   - username
   - next (optional, will be returned in ``/api/accounts/login/code/`` to be handled by the frontend)
   - Sends a login code to the user
- `/api/accounts/login/code/` (POST)
   - code
   - Returns ``key`` (authentication token) and ``next`` (provided by ``/api/accounts/login/``)
- `/api/accounts/logout/` (POST)
   - Performs logout
