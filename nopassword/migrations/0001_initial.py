# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginCode',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID',
                 auto_created=True)),
                ('code', models.CharField(editable=False, verbose_name='code', max_length=20)),
                ('timestamp', models.DateTimeField(editable=False)),
                ('next', models.TextField(blank=True, editable=False)),
                ('user', models.ForeignKey(related_name='login_codes', verbose_name='user',
                 to=settings.AUTH_USER_MODEL, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
