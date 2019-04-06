# -*- coding: utf-8 -*-
import hashlib
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class LoginCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='login_codes',
                             editable=False, verbose_name=_('user'), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(editable=False)
    next = models.TextField(editable=False, blank=True)

    def __str__(self):
        return "%s - %s" % (self.user, self.timestamp)

    @property
    def code(self):
        hash_algorithm = getattr(settings, 'NOPASSWORD_HASH_ALGORITHM', 'sha256')
        m = getattr(hashlib, hash_algorithm)()
        m.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
        m.update(str(self.id).encode())
        if getattr(settings, 'NOPASSWORD_NUMERIC_CODES', False):
            hashed = str(int(m.hexdigest(), 16))
        else:
            hashed = m.hexdigest()
        return hashed

    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()

        if not self.next:
            self.next = '/'

        super(LoginCode, self).save(*args, **kwargs)

    @classmethod
    def create_code_for_user(cls, user, next=None):
        if not user.is_active:
            return None

        login_code = LoginCode(user=user)
        if next is not None:
            login_code.next = next
        login_code.save()
        return login_code
