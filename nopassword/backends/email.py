# -*- coding: utf-8 -*-
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from nopassword.backends.base import NoPasswordBackend


class EmailBackend(NoPasswordBackend):
    template_name = 'registration/login_code_request_email.txt'
    html_template_name = None
    subject_template_name = 'registration/login_code_request_subject.txt'
    from_email = None

    def send_login_code(self, code, context, **kwargs):
        to_email = code.user.email
        subject = render_to_string(self.subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = render_to_string(self.template_name, context)

        email_message = EmailMultiAlternatives(subject, body, self.from_email, [to_email])

        if self.html_template_name is not None:
            html_email = render_to_string(self.html_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()
