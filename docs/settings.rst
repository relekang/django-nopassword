Settings
--------

django-nopassword settings
++++++++++++++++++++++++++

.. currentmodule:: django.conf.settings

.. attribute:: NOPASSWORD_LOGIN_CODE_TIMEOUT

    Default: ``900``

    Defines how long a login code is valid in seconds.

.. attribute:: NOPASSWORD_HASH_ALGORITHM

    Default: ``'sha256'``

    Set the algorithm for used in logincode generation. Possible values are those who are supported in hashlib. The value should be set as the name of the attribute in hashlib. Example `hashlib.sha256()` would be `NOPASSWORD_HASH_ALGORITHM = 'sha256'.

.. attribute:: NOPASSWORD_LOGIN_ON_GET

    Default: ``False``

    By default, the login code url requires a POST request to authenticate the user. A GET request renders a form that must be submitted by the user to perform authentication. To authenticate directly inside the initial GET request instead, set this to ``True``.

.. attribute:: NOPASSWORD_TWILIO_SID

    Account ID for Twilio.

.. attribute:: NOPASSWORD_TWILIO_AUTH_TOKEN

    Account secret for Twilio

.. attribute:: NOPASSWORD_NUMERIC_CODES

    Default: ``False``

    A boolean flag if set to True, codes will contain numeric characters only (0-9).

Django settings used in django-nopassword
+++++++++++++++++++++++++++++++++++++++++

.. attribute:: DEFAULT_FROM_EMAIL

    Default: ``'root@example.com'``
