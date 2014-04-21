# -*- coding: utf-8 -*-
import os
import hashlib
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse_lazy
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.db import models

from .utils import get_username, AUTH_USER_MODEL


class LoginCode(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='login_codes',
                             editable=False, verbose_name=_('user'))
    code = models.CharField(max_length=20, editable=False, verbose_name=_('code'))
    timestamp = models.DateTimeField(editable=False)
    next = models.TextField(editable=False, blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.timestamp)

    def save(self, *args, **kwargs):
        self.timestamp = datetime.now()
        if not self.next:
            self.next = '/'
        super(LoginCode, self).save(*args, **kwargs)

    def login_url(self):
        username = get_username(self.user)
        if getattr(settings, 'NOPASSWORD_HIDE_USERNAME', False):
            view = reverse_lazy('django_nopassword.views.login_with_code', args=[self.code]),
        else:
            view = reverse_lazy('django_nopassword.views.login_with_code_and_username',
                                args=[username, self.code]),

        return 'http://%s%s?next=%s' % (
            getattr(settings, 'SERVER_URL', 'example.com'),
            view[0],
            self.next
        )

    def send_login_email(self):
        subject = getattr(settings, 'NOPASSWORD_LOGIN_EMAIL_SUBJECT', _('Login code'))
        to_email = [self.user.email]
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'root@example.com')

        context = {'url': self.login_url(), 'code': self}
        text_content = render_to_string('registration/login_email.txt', context)
        html_content = render_to_string('registration/login_email.html', context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @classmethod
    def create_code_for_user(cls, user, next=None):
        if not user.is_active:
            return None

        code = cls.generate_code()
        login_code = LoginCode(user=user, code=code)
        if next is not None:
            login_code.next = next
        login_code.save()
        return login_code

    @classmethod
    def generate_code(cls, length=40):
        hash_algorithm = getattr(settings, 'NOPASSWORD_HASH_ALGORITHM', 'sha256')
        m = getattr(hashlib, hash_algorithm)()
        m.update(getattr(settings, 'SECRET_KEY', None))
        m.update(os.urandom(16).encode('hex'))
        return m.hexdigest()[:length]
