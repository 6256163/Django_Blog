# coding=utf-8
from __future__ import unicode_literals
from blog.models import Blog
from rest_framework import serializers
from users.serializers import UserSerializer

class BlogSerializer(serializers.ModelSerializer):
    #pk = serializers.IntegerField(read_only=True)
    #blog_title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    #blog_text = serializers.CharField(required=True, allow_blank=False, max_length=200)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = ('id', 'blog_title', 'blog_text', 'pub_date','user',)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.blog_title = validated_data.get('blog_title', instance.title)
        instance.blog_text = validated_data.get('blog_text', instance.code)
        instance.save()
        return instance





