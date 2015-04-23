# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0004_auto_20150422_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='client_id',
        ),
        migrations.AddField(
            model_name='token',
            name='app_id',
            field=models.OneToOneField(to='lab2.Apps'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='token',
            name='id',
            field=models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True),
            preserve_default=False,
        ),
    ]
