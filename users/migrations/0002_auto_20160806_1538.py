# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-08-06 07:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='relationship',
            unique_together=set([('current_user', 'follower')]),
        ),
    ]