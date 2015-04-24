# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0008_auto_20150424_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='code_expires',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='token_expires',
            field=models.DateTimeField(null=True),
        ),
    ]
