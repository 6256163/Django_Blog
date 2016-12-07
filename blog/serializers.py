# coding=utf-8
from __future__ import unicode_literals

from blog.models import Blog, Reply, ReplyInReply
from rest_framework import serializers


class BlogSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    head_img = serializers.ReadOnlyField(source='user.person.head_img.url')
    latest_reply_user = serializers.ReadOnlyField(source='latest_reply_user.username')

    class Meta:
        model = Blog
        fields = ('url', 'id', 'blog_title', 'blog_text', 'pub_date', 'user', 'head_img', 'reply_counter',
                  'latest_reply_user', 'latest_reply',)

    def create(self, validated_data):
        """
        Create and return a new `Blog` instance, given the validated data.
        """
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Blog` instance, given the validated data.
        """
        instance.blog_title = validated_data.get('blog_title', instance.blog_title)
        instance.blog_text = validated_data.get('blog_text', instance.blog_text)
        instance.save()
        return instance


class ReplySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    head_img = serializers.ReadOnlyField(source='user.person.head_img.url')

    class Meta:
        model = Reply
        fields = ('url', 'id', 'reply_text', 'floor', 'pub_date', 'blog', 'reply_counter', 'user', 'head_img',)

    def create(self, validated_data):
        """
        Create and return a new `Reply` instance, given the validated data.
        """
        return Reply.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return a existing `Reply` instance, given the validated data.
        """
        instance.reply_text = validated_data.get('reply_text', instance.reply_text)
        instance.save()
        return instance


class ReplyInReplySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    reply_id = serializers.IntegerField(source='reply.id',read_only=True)
    head_img = serializers.ReadOnlyField(source='user.person.head_img.url')

    class Meta:
        model = ReplyInReply
        fields = ('url', 'id', 'reply_text', 'pub_date', 'reply', 'reply_id', 'user', 'head_img',)

    def create(self, validated_data):
        """
        Create and return a new `ReplyInReply` instance, given the validated data.
        """
        return ReplyInReply.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return a existing `ReplyInReply` instance, given the validated data.
        """
        instance.reply_text = validated_data.get('reply_text', instance.reply_text)
        instance.save()
        return instance
