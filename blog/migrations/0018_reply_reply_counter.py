# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-09-27 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20160927_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='reply_counter',
            field=models.IntegerField(default=0),
        ),
    ]
