# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 10:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_person_hometown_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='sex',
            field=models.CharField(choices=[('m', '\u7537'), ('f', '\u5973')], max_length=1, null=True),
        ),
    ]