# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-17 23:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20161216_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='stateflag',
            name='name',
            field=models.CharField(default='alertState', max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='stateflag',
            name='state',
            field=models.BooleanField(default=True),
        ),
    ]