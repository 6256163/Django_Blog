from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Relationship(models.Model):
    current_user = models.ForeignKey(User)
    follower = models.ForeignKey(User, related_name= 'Follower')
    date = models.DateTimeField('date of making friend', auto_now_add=True)

    class Meta:
        unique_together = ("current_user", "follower")
