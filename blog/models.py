# coding=utf-8
from __future__ import unicode_literals
import datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.


class Blog(models.Model):
    user = models.ForeignKey(User)
    blog_title = models.CharField("blog title",max_length=40, null=False)
    blog_text = models.TextField("blog content", null=False)
    pub_date = models.DateTimeField("publish date", auto_now_add=True)
    reply_counter = models.IntegerField("the count of reply",default=0)
    latest_reply = models.DateTimeField("latest reply date", auto_now_add=True)
    latest_reply_user = models.ForeignKey(User, related_name='latest_reply_user')

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.blog_title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Reply(models.Model):
    blog = models.ForeignKey(Blog)
    user = models.ForeignKey(User)
    reply_text = models.CharField("reply content",max_length=200, null=False)
    floor = models.IntegerField("floor number",default=0)
    reply_counter = models.IntegerField("the lzl count of reply",default=0)
    pub_date = models.DateTimeField("publish date", auto_now_add=True)

    def __str__(self):
        return self.reply_text


@receiver(post_save, sender=Reply)
def update_floor(sender, created, instance, **kwargs):
    if created:
        instance.floor = Blog.objects.get(pk=instance.blog.id).reply_counter + 1
        instance.save()
        instance.blog.reply_counter += 1
        instance.blog.latest_reply = instance.pub_date
        instance.blog.latest_reply_user = instance.user
        instance.blog.save()


class ReplyInReply(models.Model):
    reply = models.ForeignKey(Reply)
    user = models.ForeignKey(User)
    reply_text = models.CharField("lzl content",max_length=200, null=False)
    pub_date = models.DateTimeField("publish date", auto_now_add=True)

    def __str__(self):
        return self.reply_text


@receiver(post_save, sender=ReplyInReply)
def update_reply_counter(sender, created, instance, **kwargs):
    if created:
        instance.reply.reply_counter += 1
        instance.reply.save()
