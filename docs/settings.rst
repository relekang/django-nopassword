
Settings
********

NOPASSWORD_LOGIN_CODE_TIMEOUT
-----------------------------
- Default: `900` (15 minutes)

Defines how long a login code is valid in seconds.

NOPASSWORD_AUTOCOMPLETE
-----------------------
- Default: `False`

Activates autocomplete in login form. Be aware of the potensial security risk and privacy risk by publicly viewing all usernames and full names. Only do this if you are certain your users would not mind.

NOPASSWORD_HIDE_USERNAME
------------------------
- Default: `False`

If set to True, the login url will not contain

NOPASSWORD_LOGIN_EMAIL_SUBJECT
------------------------------
- Default: `Login code`

Sets Email Subject for Login Emails

Django settings
========

These are settings in the Django framework which is used in django_nopassword.

SERVER_URL
----------------
- Default: `example.com`

DEFAULT_FROM_EMAIL
------------------
- Default: `root@example.com`

