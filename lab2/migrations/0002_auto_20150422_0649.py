# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apps',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('client_id', models.CharField(max_length=100, unique=True)),
                ('secret_id', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Monument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('date', models.DateField()),
                ('city', models.ForeignKey(to='lab2.City')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('client_id', models.OneToOneField(to='lab2.Apps', primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('access_token', models.CharField(max_length=100)),
                ('refresh_token', models.CharField(max_length=100)),
                ('token_expires', models.DateField()),
                ('code_expires', models.CharField(max_length=30)),
                ('redirect_uri', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(to='lab2.Country'),
        ),
    ]
