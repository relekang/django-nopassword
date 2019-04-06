Changelog
=========

5.0.0
-----

Breaking changes:

- Removed custom length of login codes
- Do not store the code in the database. Hash and compare on login instead. This might have an performance impact.
- Add user id to the login code form and urls sent to the user.
- Changing the secret key will now invalidate all login codes.

4.0.1
-----

Set the default length of codes to 64. The setting ``NOPASSWORD_CODE_LENGTH`` is considered
deprecated.

4.0.0
-----

Added:

- Added ``LoginCodeAdmin``
- Added rest support

Breaking changes:

- Remove support for Django < 1.11
- Add support for Django 2
- ``NoPasswordBackend.authenticate`` doesn't have side effects anymore, it only checks if a login code is valid.
- ``NoPasswordBackend`` now uses the default django method ``user_can_authenticate`` instead of ``verify_user``.
- Changed signature of ``NoPasswordBackend.send_login_code`` to ``send_login_code(code, context, **kwargs)``, to support custom template context.
- ``EmailBackend`` doesn't attach a html message to the email by default. You can provide a template ``registration/login_email.html`` to do so.
- Removed setting ``NOPASSWORD_LOGIN_EMAIL_SUBJECT`` in favor of template ``registration/login_subject.txt``
- Renamed form ``AuthenticationForm`` to ``LoginForm``
- ``LoginForm`` (previously ``AuthenticationForm``) doesn't have side effects anymore while cleaning.
- ``LoginForm`` (previously ``AuthenticationForm``) doesn't check for cookie support anymore.
- Removed methods ``get_user`` and ``get_user_id`` from ``LoginForm`` (previously ``AuthenticationForm``).
- Removed method ``login_url`` and ``send_login_code`` from ``LoginCode`` (previously ``AuthenticationForm``).
- Renamed template ``registration/login.html`` to ``registration/login_form.html``.
- Changed content of default templates.
- Removed views ``login_with_code_and_username``.
- Refactored views to be class based views and to use forms instead of url parameters.
- Changed url paths
- Removed setting ``NOPASSWORD_POST_REDIRECT``, use ``NOPASSWORD_LOGIN_ON_GET`` instead.
- Removed setting ``NOPASSWORD_NAMESPACE``.
- Removed setting ``NOPASSWORD_HIDE_USERNAME``.
- Removed setting ``NOPASSWORD_LOGIN_EMAIL_SUBJECT``.
