# coding=utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Relationship(models.Model):
    current_user = models.ForeignKey(User)
    follower = models.ForeignKey(User, related_name='Follower')
    date = models.DateTimeField('date of making friend', auto_now_add=True)

    class Meta:
        unique_together = ("current_user", "follower")


class Notice(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user')
    to_user = models.ForeignKey(User, related_name='to_user')
    message = models.CharField(max_length=200)
    pub_date = models.DateField(auto_now_add=True)
    flag = models.IntegerField(default=1)


class Person(models.Model):
    user = models.OneToOneField(User,)
    head_img = models.ImageField(upload_to = 'storage/img/', default = 'storage/img/default_headimg.png',)
    sex = models.CharField(max_length=1, null=True, blank= True)
    birthday = models.DateField(null= True)
    hometown_province = models.CharField(max_length=10, null=True,)
    hometown_city = models.CharField(max_length=10, null=True,)
    hometown_area = models.CharField(max_length=10, null=True,)
    profile = models.TextField(max_length=500, null=True,)

    class Meta:
        db_table = 'users_person'
