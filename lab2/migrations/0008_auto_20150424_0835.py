# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0007_token_token_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='code_expires',
            field=models.DateField(null=True),
        ),
    ]
