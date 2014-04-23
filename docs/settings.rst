Settings
--------

django-nopassword settings
++++++++++++++++++++++++++

.. currentmodule:: django.conf.settings

.. attribute:: NOPASSWORD_LOGIN_CODE_TIMEOUT

    Defines how long a login code is valid in seconds.

.. attribute:: NOPASSWORD_AUTOCOMPLETE

    Activates autocomplete in login form. Be aware of the potensial security risk and privacy risk by publicly viewing all usernames and full names. Only do this if you are certain your users would not mind.

.. attribute:: NOPASSWORD_HIDE_USERNAME

    If set to True, the login url will not contain

.. attribute:: NOPASSWORD_LOGIN_EMAIL_SUBJECT

    Sets Email Subject for Login Emails.

.. attribute:: NOPASSWORD_HASH_ALGORITHM

    Set the algorithm for used in logincode generation. Possible values are those who are supported in hashlib. The value should be set as the name of the attribute in hashlib. Example `hashlib.sha256()` would be `NOPASSWORD_HASH_ALGORITHM = 'sha256'.

Django settings used in django-nopassword
+++++++++++++++++++++++++++++++++++++++++

.. attribute:: SERVER_URL

Default: `example.com`

.. attribute:: DEFAULT_FROM_EMAIL

Default: `root@example.com`

