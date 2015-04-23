# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0005_auto_20150423_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='access_token',
            field=models.CharField(null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='token',
            name='redirect_uri',
            field=models.CharField(null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='token',
            name='refresh_token',
            field=models.CharField(null=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='token',
            name='token_expires',
            field=models.DateField(null=True),
        ),
    ]
