#!/usr/bin/env python
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'

from django.test.utils import get_runner
from django.conf import settings

TestRunner = get_runner(settings)


def runtests():
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['tests'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()
