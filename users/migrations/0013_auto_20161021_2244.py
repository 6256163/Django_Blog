# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20161021_2233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='birthday_day',
        ),
        migrations.RemoveField(
            model_name='person',
            name='birthday_month',
        ),
        migrations.RemoveField(
            model_name='person',
            name='birthday_year',
        ),
        migrations.AddField(
            model_name='person',
            name='birthday',
            field=models.DateField(null=True),
        ),
    ]
