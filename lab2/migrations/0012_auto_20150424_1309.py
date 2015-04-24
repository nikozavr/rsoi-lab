# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0011_auto_20150424_1232'),
    ]

    operations = [
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('device_type', models.CharField(max_length=50)),
                ('dig_disp', models.IntegerField()),
                ('color', models.CharField(max_length=25)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Manufacturer',
            new_name='Manufacturers',
        ),
        migrations.RemoveField(
            model_name='device',
            name='manufature',
        ),
        migrations.DeleteModel(
            name='Device',
        ),
        migrations.AddField(
            model_name='devices',
            name='manufature',
            field=models.ForeignKey(to='lab2.Manufacturers'),
            preserve_default=True,
        ),
    ]
