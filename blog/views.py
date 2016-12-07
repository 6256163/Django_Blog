# coding=utf-8
from __future__ import unicode_literals

from copy import copy

from blog.permissions import IsOwnerOrReadOnly
from blog.serializers import BlogSerializer, ReplySerializer, ReplyInReplySerializer
from django import http
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, viewsets, renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from . import forms
from users.forms import RegisterForm
from .models import Blog, Reply, ReplyInReply


# Create your views here.


class BlogViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, `update` and `destroy` actions.

    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    renderer_classes = (renderers.TemplateHTMLRenderer, renderers.JSONRenderer,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, latest_reply_user=self.request.user)

    # 重写retrieve以适应分页需求
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_blog = self.get_serializer(instance)
        replies_queryset = Reply.objects.filter(blog=instance)
        page = self.paginate_queryset(replies_queryset)
        if page is not None:
            serializer_reply = ReplySerializer(page, context=self.get_serializer_context(), many=True)
            return Response(
                {"blog": serializer_blog.data, "replies": self.get_paginated_response(serializer_reply.data).data},
                template_name='blog/detail.html')

        serializer_reply = ReplySerializer(replies_queryset, context=self.get_serializer_context(), many=True)
        return Response({"blog": serializer_blog.data, "replies": serializer_reply.data},
                        template_name='blog/detail.html')

    # 重写create以过滤'blog_title'字段
    def create(self, request, *args, **kwargs):
        data = copy(request.data)
        data['blog_title'] = data['blog_title'].replace("\n", "")
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        #return 中的template_name没有实际意义。单元测试中需要给出返回的template。
        return Response(serializer.data, status=302, headers=headers,template_name='blog/index.html',)

    # 重写list以适应分页需求
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by("-pub_date")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({'blog': self.get_paginated_response(serializer.data).data,
                             'user': request.user,
                             'form': RegisterForm},
                            template_name='blog/index.html')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'blog': serializer,
                         'user': request.user,
                         'form': RegisterForm}, template_name='blog/index.html')


class ReplyViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, `update` and `destroy` actions.

    """
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    renderer_classes = (renderers.TemplateHTMLRenderer, renderers.JSONRenderer)
    template_name = "blog/reply_in_reply.html"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # 重写retrieve以适应分页需求
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        queryset = ReplyInReply.objects.filter(reply=instance)
        page = self.paginate_queryset(queryset)

        if page is not None:
            reply_serializer = ReplyInReplySerializer(page, context=self.get_serializer_context(), many=True)
            data = {
                "reply": serializer.data,
                "replies_in_reply": self.get_paginated_response(reply_serializer.data).data
            }
            return Response(data, template_name=self.template_name)

        reply_serializer = ReplyInReplySerializer(queryset, context=self.get_serializer_context(), many=True)
        data = {"reply": serializer.data, "replies_in_reply": reply_serializer.data}
        return Response(data, template_name=self.template_name)


class ReplyInReplyViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`, `update` and `destroy` actions.

    """
    queryset = ReplyInReply.objects.all()
    serializer_class = ReplyInReplySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = ReplyInReply.objects.all()
        reply = self.request.GET.get('reply', None)
        if reply is not None:
            queryset = queryset.filter(reply=reply)
        return queryset


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'blogs': reverse('blog-list', request=request, format=format)
    })
