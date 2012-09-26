from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

#Todo: move to settings
TIMEOUT = timedelta(minutes=15)

class LoginCode (models.Model):
    user = models.ForeignKey(User, related_name='login_codes', editable=False, verbose_name=_('user'))
    code = models.CharField(max_length=2, editable=False, verbose_name=_('code'))
    timestamp = models.DateTimeField(editable=False)

    def __unicode__ (self):
        return "%s - %s" % (self.user, self.timestamp)

    @classmethod
    def check (cls, user, code):
        try:
            timestamp = datetime.now() + TIMEOUT
            login_code = cls.objects.get(user=user, code=code, timestamp__gt=timestamp)
            return user
        except (TypeError, cls.DoesNotExist):
            return None

