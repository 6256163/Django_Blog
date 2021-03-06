# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-11-22 08:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0020_auto_20161115_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='latest_reply_user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='latest_reply_user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blog',
            name='latest_reply',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'date latest_reply'),
        ),
    ]
