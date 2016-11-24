# coding=utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Person(models.Model):
    """
    User类扩展:用于存储用户其他信息
    """
    user = models.OneToOneField(User,)
    head_img = models.ImageField("user head image path",upload_to = 'storage/img/', default = 'storage/img/default_headimg.png',)
    sex = models.CharField("sex",max_length=1, null=True, blank= True)
    birthday = models.DateField("birthday",null= True)
    hometown_province = models.CharField("province",max_length=10, null=True,)
    hometown_city = models.CharField("city",max_length=10, null=True,)
    hometown_area = models.CharField("area",max_length=10, null=True,)
    profile = models.TextField("profile",max_length=500, null=True,)

    class Meta:
        db_table = 'users_person'
