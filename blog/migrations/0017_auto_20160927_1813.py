# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-09-27 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20160927_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='floor',
            field=models.IntegerField(default=0),
        ),
    ]