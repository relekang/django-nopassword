from django.contrib.auth.models import UserManager
from django.db import models

try:
    from django.contrib.auth.models import AbstractUser
except ImportError:
    from django.db.models import Model as AbstractUser


class CustomUser(AbstractUser):
    extra_field = models.CharField(max_length=2)