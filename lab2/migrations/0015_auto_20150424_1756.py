# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0014_auto_20150424_1716'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devices',
            old_name='manufaturer',
            new_name='manufacturer',
        ),
    ]
