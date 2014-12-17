Usage
-----
Add the app to installed apps::

    INSTALLED_APPS = (
        'nopassword',
    )

Set the authentication backend to *EmailBackend*::

    AUTHENTICATION_BACKENDS = ( 'nopassword.backends.email.EmailBackend', )

Add urls to your *urls.py*::

    urlpatterns = patterns('',
        url(r'^accounts/', include('nopassword.urls')),
    )

Verify users
~~~~~~~~~~~~
If it is necessary to verify that users still are active in another system. Override
*verify_user(user)* to implement your check. In *NoPasswordBackend* that method checks
whether the user is active in the django app.

Backends
++++++++
There are several predefined backends. Usage of those backends are listed below.

.. currentmodule:: nopassword.backends.email

.. class:: EmailBackend
Delivers the code by email. It uses the django send email functionality to send
the emails. It will attach both HTML and plain-text versions of the email.

.. currentmodule:: nopassword.backends.sms

.. class:: TwilioBackend
Delivers the code by sms sent through the twilio service.


Custom backends
~~~~~~~~~~~~~~~
In backends.py there is a *NoPasswordBackend*, from which it is possible
to build custom backends. The *EmailBackend* described above inherits from
this backend. Creating your own backend is can be done by creating a subclass
of *NoPasswordBackend* and implementing *send_login_code*. A good example is
the *EmailBackend*::

    class EmailBackend(NoPasswordBackend):

        def send_login_code(self, code):
            subject = getattr(settings, 'NOPASSWORD_LOGIN_EMAIL_SUBJECT', _('Login code'))
            to_email = [code.user.email]
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'root@example.com')

            context = {'url': code.login_url(), 'code': code}
            text_content = render_to_string('registration/login_email.txt', context)
            html_content = render_to_string('registration/login_email.html', context)

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
