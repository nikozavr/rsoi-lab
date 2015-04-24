# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0013_auto_20150424_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='dig_disp',
            field=models.FloatField(),
        ),
    ]
