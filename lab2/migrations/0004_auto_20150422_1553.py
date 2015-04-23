# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0003_apps_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apps',
            old_name='secret_id',
            new_name='client_secret',
        ),
    ]
