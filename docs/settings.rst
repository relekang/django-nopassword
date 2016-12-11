Settings
--------

django-nopassword settings
++++++++++++++++++++++++++

.. currentmodule:: django.conf.settings

.. attribute:: NOPASSWORD_LOGIN_CODE_TIMEOUT

    Defines how long a login code is valid in seconds.

.. attribute:: NOPASSWORD_NAMESPACE

    Defines the namespace for the urls, this must match the namespace of the include of
    nopassword.urls. Default is 'nopassword'.

.. attribute:: NOPASSWORD_HIDE_USERNAME

    If set to True, the login url will not contain the username.

.. attribute:: NOPASSWORD_LOGIN_EMAIL_SUBJECT

    Sets Email Subject for Login Emails.

.. attribute:: NOPASSWORD_HASH_ALGORITHM

    Set the algorithm for used in logincode generation. Possible values are those who are supported in hashlib. The value should be set as the name of the attribute in hashlib. Example `hashlib.sha256()` would be `NOPASSWORD_HASH_ALGORITHM = 'sha256'.

.. attribute:: NOPASSWORD_POST_REDIRECT

    By default, the login code url requires a POST request to authenticate the user. A GET request renders ``registration/login_submit.html``, which contains some Javascript that automatically performs the POST on page load. To authenticate directly inside the initial GET request instead, set this to ``False``.

.. attribute:: NOPASSWORD_CODE_LENGTH

    The length of the code used to log people in. Default is 20.

.. attribute:: NOPASSWORD_TWILIO_SID

    Account ID for Twilio.

.. attribute:: NOPASSWORD_TWILIO_AUTH_TOKEN

    Account secret for Twilio

.. attribute:: NOPASSWORD_NUMERIC_CODES

    A boolean flag if set to True, codes will contain numeric characters only (0-9). Default: False

Django settings used in django-nopassword
+++++++++++++++++++++++++++++++++++++++++

.. attribute:: SERVER_URL

    Default: `example.com`

    By default, ``nopassword.views.login`` passes the result of ``result.get_host()`` to
    ``LoginCode.send_login_code`` to build the login URL. If you write your own view
    and/or want to avoid this behavior by not passing a value for host, the
    ``SERVER_URL`` setting will be used instead.

.. attribute:: DEFAULT_FROM_EMAIL

    Default: `root@example.com`
