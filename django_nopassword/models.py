# -*- coding: utf-8 -*-
import string
from random import choice
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.db import models

from django_nopassword.utils import User, get_username


class LoginCode(models.Model):
    user = models.ForeignKey(User, related_name='login_codes', editable=False, verbose_name=_('user'))
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
        self.send_login_email()

    def login_url(self):
        username = get_username(self.user)
        if getattr(settings, 'NOPASSWORD_HIDE_USERNAME', False):
            view = reverse('django_nopassword.views.login_with_code', args=[self.code]),
        else:
            view = reverse('django_nopassword.views.login_with_code_and_username', args=[username, self.code]),

        return 'http://%s%s?next=%s' % (
            getattr(settings, 'SERVER_URL', 'example.com'),
            view[0],
            self.next
        )

    def send_login_email(self):
        subject = 'Login code'
        to_email = [self.user.email]
        from_email = getattr(settings, 'SERVER_EMAIL', 'root@example.com'),

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
        if not next is None:
            login_code.next = next
        login_code.save()
        return login_code

    @classmethod
    def generate_code(cls, length=20):
        chars = string.letters + string.digits
        return ''.join([choice(chars) for i in xrange(length)])
