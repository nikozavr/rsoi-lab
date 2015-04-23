# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0002_auto_20150422_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='apps',
            name='user',
            field=models.ForeignKey(to='lab2.Users')
        ),
    ]
