# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-11-30 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20161101_2135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='notice',
            name='to_user',
        ),
        migrations.AlterUniqueTogether(
            name='relationship',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='current_user',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='follower',
        ),
        migrations.AlterField(
            model_name='person',
            name='birthday',
            field=models.DateField(null=True, verbose_name='birthday'),
        ),
        migrations.AlterField(
            model_name='person',
            name='head_img',
            field=models.ImageField(default='storage/img/default_headimg.png', upload_to='storage/img/', verbose_name='user head image path'),
        ),
        migrations.AlterField(
            model_name='person',
            name='hometown_area',
            field=models.CharField(max_length=10, null=True, verbose_name='area'),
        ),
        migrations.AlterField(
            model_name='person',
            name='hometown_city',
            field=models.CharField(max_length=10, null=True, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='person',
            name='hometown_province',
            field=models.CharField(max_length=10, null=True, verbose_name='province'),
        ),
        migrations.AlterField(
            model_name='person',
            name='profile',
            field=models.TextField(max_length=500, null=True, verbose_name='profile'),
        ),
        migrations.AlterField(
            model_name='person',
            name='sex',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='sex'),
        ),
        migrations.DeleteModel(
            name='Notice',
        ),
        migrations.DeleteModel(
            name='Relationship',
        ),
    ]
