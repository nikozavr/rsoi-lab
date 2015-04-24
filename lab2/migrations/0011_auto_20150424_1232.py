# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0010_auto_20150424_1213'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Manufature',
            new_name='Manufacturer',
        ),
    ]
