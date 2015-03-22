# -*- coding: utf-8 -*-
import django
if django.VERSION < (1, 6):
    from .test_backends import *  # noqa
    from .test_models import *  # noqa
    from .test_views import *  # noqa
