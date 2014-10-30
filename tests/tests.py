# -*- coding: utf-8 -*-
import django

if django.VERSION < (1, 6):
    from .test_backends import *
    from .test_models import *
    from .test_views import *
