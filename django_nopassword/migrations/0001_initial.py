# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True,
                 primary_key=True)),
                ('code', models.CharField(verbose_name='code', max_length=20, editable=False)),
                ('timestamp', models.DateTimeField(editable=False)),
                ('next', models.TextField(editable=False, blank=True)),
                ('user', models.ForeignKey(related_name=b'login_codes', editable=False,
                 to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
