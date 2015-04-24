# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0009_auto_20150424_0836'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('device_type', models.CharField(max_length=50)),
                ('dig_disp', models.IntegerField()),
                ('color', models.CharField(max_length=25)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Manufature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('established', models.DateTimeField()),
                ('country', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='city',
            name='country',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.RemoveField(
            model_name='monument',
            name='city',
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Monument',
        ),
        migrations.AddField(
            model_name='device',
            name='manufature',
            field=models.ForeignKey(to='lab2.Manufature'),
            preserve_default=True,
        ),
    ]
