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