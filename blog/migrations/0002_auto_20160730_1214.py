# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-07-30 12:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Replay',
            new_name='Reply',
        ),
        migrations.RenameField(
            model_name='reply',
            old_name='replay_mun',
            new_name='reply_mun',
        ),
        migrations.RenameField(
            model_name='reply',
            old_name='replay_text',
            new_name='reply_text',
        ),
    ]
