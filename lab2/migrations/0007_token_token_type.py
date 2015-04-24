# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0006_auto_20150423_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='token_type',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
