# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-09-27 06:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20160927_1417'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='reply_num',
            new_name='reply_counter',
        ),
    ]