# -*- coding: utf-8 -*-
from django.core.mail import EmailMultiAlternatives
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string

from nopassword.backends.base import NoPasswordBackend


class EmailBackend(NoPasswordBackend):
    template_name = 'registration/login_code_request_email.txt'
    html_template_name = 'registration/login_code_request_email.html'
    subject_template_name = 'registration/login_code_request_subject.txt'
    from_email = None

    def send_login_code(self, code, context, **kwargs):
        to_email = code.user.email
        subject = render_to_string(self.subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = render_to_string(self.template_name, context)

        email_message = EmailMultiAlternatives(subject, body, self.from_email, [to_email])

        try:
            html_email = render_to_string(self.html_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')
        except TemplateDoesNotExist:
            pass

        email_message.send()
