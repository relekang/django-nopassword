Usage
-----
Add the app to installed apps::

    INSTALLED_APPS = (
        'nopassword',
    )

Add the authentication backend *EmailBackend*::

    AUTHENTICATION_BACKENDS = (
        # Needed to login by username in Django admin, regardless of `nopassword`
        'django.contrib.auth.backends.ModelBackend',

        # Send login codes via email
        'nopassword.backends.email.EmailBackend',
    )

Add urls to your *urls.py*::

    urlpatterns = patterns('',
        url(r'^accounts/', include('nopassword.urls')),
    )

Backends
++++++++
There are several predefined backends. Usage of those backends are listed below.

.. currentmodule:: nopassword.backends.email

.. class:: EmailBackend
Delivers the code by email. It uses the django send email functionality to send
the emails.

Override the following templates to customize emails:

- ``registration/login_email.txt`` - Plain text message
- ``registration/login_email.html`` - HTML message (note that no default html message is attached)
- ``registration/login_subject.txt`` - Subject

.. currentmodule:: nopassword.backends.sms

.. class:: TwilioBackend
Delivers the code by sms sent through the twilio service.

Override the following template to customize messages:

- ``registration/login_sms.txt`` - SMS message


Custom backends
~~~~~~~~~~~~~~~
In backends.py there is a *NoPasswordBackend*, from which it is possible
to build custom backends. The *EmailBackend* described above inherits from
this backend. Creating your own backend can be done by creating a subclass
of *NoPasswordBackend* and implementing *send_login_code*.::

    class CustomBackend(NoPasswordBackend):
    
        def send_login_code(self, code, context, **kwargs):
            """
            Use code.user to get contact information
            Use context to render a custom template
            Use kwargs in case you have a custom view that provides additional configuration
            """
