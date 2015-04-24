# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0012_auto_20150424_1309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devices',
            old_name='manufature',
            new_name='manufaturer',
        ),
        migrations.RemoveField(
            model_name='devices',
            name='color',
        ),
        migrations.AddField(
            model_name='devices',
            name='year',
            field=models.IntegerField(default=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='manufacturers',
            name='established',
            field=models.IntegerField(),
        ),
    ]
