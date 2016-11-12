from __future__ import unicode_literals
from blog.models import Blog, Reply
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Image(models.Model):
    user= models.ForeignKey(User)
    path = models.ImageField(upload_to = 'storage/blog_img/',)
