# -*- coding: utf8 -*-

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_nopassword',
    }
}

AUTH_USER_MODEL = 'tests.CustomUser'

LOGIN_CODE_TIMEOUT = 900

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'django_nopassword',
    'tests',
]
AUTHENTICATION_BACKENDS = (
    'django_nopassword.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend'
)

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = 'supersecret'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'tests.urls'

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'