# coding=utf-8
from __future__ import unicode_literals

import re
import urllib

from blog.models import Blog, Reply
from blog.serializers import BlogSerializer, ReplySerializer
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.permissions import AllowAny

from . import forms
from django import http
from .models import Relationship, Notice, Person
from rest_framework import viewsets
from users.serializers import UserSerializer
from rest_framework.decorators import api_view, detail_route, list_route, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # permission_classes = [IsAccountAdminOrReadOnly]

    @detail_route(methods=['get'])
    def blog(self, request, pk):
        user = self.get_object()
        blog_queryset = Blog.objects.filter(user=user)
        page = self.paginate_queryset(blog_queryset)
        if page is not None:
            serializer = BlogSerializer(*[page], **{"context": self.get_serializer_context(), "many": True})
            return self.get_paginated_response(serializer.data)

        serializer = BlogSerializer(blog_queryset, context=self.get_serializer_context(), many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def reply(self, request, pk):
        user = self.get_object()
        reply_queryset = Reply.objects.filter(user=user)
        page = self.paginate_queryset(reply_queryset)
        if page is not None:
            serializer = ReplySerializer(*[page], **{"context": self.get_serializer_context(), "many": True})
            return self.get_paginated_response(serializer.data)

        serializer = ReplySerializer(reply_queryset, context=self.get_serializer_context(), many=True)
        return Response(serializer.data)



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
    })


@api_view(['POST'])
@permission_classes((AllowAny,))
def register_verification(request):
    if request.data.get("type")=="username":
        if request.data.get("username") != "" or request.data.get("username") != None:
            try:
                User.objects.get(username=request.data.get("username"))
            except User.DoesNotExist:
                return Response({"warning": ""})
            else:
                return Response({"warning": "用户名已被占用"})

        else:
            return Response({"warning": "用户名不能为空"})
    else:
        if request.data.get("email") != "" or request.data.get("email") != None:
            try:
                User.objects.get(email=request.data.get("email"))
            except User.DoesNotExist:
                return Response({"warning": ""})
            else:
                return Response({"warning": "邮箱已被占用"})

        else:
            return Response({"warning": "邮箱不能为空"})


@permission_classes((AllowAny,))
def register(request):
    """
    Regist a new user
    :param request:
    :return: to login page
    """
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if re.compile(r'^[\u4e00-\u9fa5]{1,7}$|^[\dA-Za-z_]{1,14}$').match(request.POST.get("username")):
            if re.compile(r'^\w{8,16}$').match(request.POST.get("password")):
                if re.compile(r'^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$').match(request.POST.get("email")):
                    if form.is_valid():
                        form.cleaned_data.pop("password_confirm")
                        user = User.objects.create_user(**form.cleaned_data)
                        Person.objects.create(user =  user)
                        login_user = auth.authenticate(username= form.data['username'], password = form.data['password'])
                        auth.login(request, login_user)
                        next = request.GET.get("next") if (request.GET.get("next") not in ["/user/login/",
                                                                                           "/user/register/",
                                                                                           "/user/register_login_success/", ]) else '/blog/'
                        return http.HttpResponseRedirect("/user/register_login_success/?%s" % urllib.urlencode({'next':next}))
                        #return render(request, 'users/register_login_success.html',{'info':'register'})
                    else:
                        return render(request, 'blog/index.html', {'form': form})

                else:
                    return render(request, 'blog/index.html', {'form': form, 'error': "邮箱格式不正确"})
            else:
                return render(request, 'blog/index.html', {'form': form, 'error': "密码不支持"})
        else:
            return render(request, 'blog/index.html', {'form': form, 'error': "用户名不正确"})
    else:
        form = forms.RegisterForm()
        return render(request, 'blog/index.html', {"form": form})


def login(request):
    """
    Login user
    :param request:
    :return: to blog index
    """
    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return http.HttpResponseRedirect("/blog/")
                else:
                    return render(request, 'blog/index.html', {'error': "account disabled"})
            else:
                return render(request, 'blog/index.html', {'error': "password error or account not existed"})
        else:
            return render(request, 'blog/index.html', {'form': form})
    else:
        form = forms.LoginForm()
        return render(request, 'blog/index.html', {'form': form})


def register_login_success(request):
    return render(request, 'users/register_login_success.html',{'next':request.GET.get("next")})


def logout(request):
    """
    logout user
    :param request:
    :return: to blog index
    """
    auth.logout(request)
    return http.HttpResponseRedirect(request.GET.get("next"))


def show_permission(request):
    """
    Get the user permission
    :param request:
    :return: to permission page
    """
    permission = request.user.user_permissions.all()
    return render(request, 'users/permission.html', {'permission': permission, 'user': request.user})


def my_info(request):
    """
    Gte user info: username, email, first_name, last_name, permission.
    :param request:
    :return: to user info page
    """
    if not request.user.is_authenticated():
        return http.HttpResponseRedirect('/user/login/')
    else:
        return render(request, 'users/my_info.html', {'user': request.user,
                                                      "permission": request.user.user_permissions.all(),
                                                      'followers': find_all_followers(request),
                                                      })


def update_user_info(request):
    if not request.user.is_authenticated():
        return http.HttpResponseRedirect('users/login')
    else:
        if request.method == "POST":
            form = forms.UserInfoForm(request.POST)
            if form.is_valid():
                person = Person.objects.filter(user=request.user)
                if not person:
                    Person.objects.create(user=request.user, **form.cleaned_data)
                else:
                    for attr, value in form.cleaned_data.items():
                        setattr(request.user.person, attr, value)
                    request.user.person.save()
                return render(request, 'users/update_user_info.html',
                              {'user': request.user, 'form': form, "error": "保存成功"})
            else:
                return render(request, 'users/update_user_info.html',
                              {'user': request.user, 'form': form, "error": form.errors})
        else:
            form = forms.UserInfoForm()
            return render(request, 'users/update_user_info.html', {'user': request.user, 'form': form})


def headimg_setting(request):
    if not request.user.is_authenticated():
        return http.HttpResponseRedirect('users/login')
    else:
        if request.method == "POST":
            form = forms.HeadImgForm(request.POST, request.FILES)
            if form.is_valid():
                person = Person.objects.filter(user=request.user)
                if not person:
                    p = Person.objects.create(user=request.user,)
                    p.head_img = form.cleaned_data['head_img']
                    p.save()
                else:
                    request.user.person.head_img = form.cleaned_data['head_img']
                    request.user.person.save()
                return render(request, 'users/headimg_setting.html',
                              {'user': request.user, 'form': form, "error": "保存成功"})
            else:
                return render(request, 'users/headimg_setting.html',
                              {'user': request.user, 'form': form, "error": form.errors})
        else:
            form = forms.HeadImgForm()
            return render(request, 'users/headimg_setting.html', {'user': request.user, 'form': form})




def find_all_followers(request):
    if not request.user.is_authenticated():
        return http.HttpResponseRedirect('users/login')
    else:
        followers = Relationship.objects.filter(current_user=request.user)
        return followers


def news_count(request):
    if not request.user.is_authenticated():
        return http.HttpResponseRedirect('users/login')
    else:
        notices = Notice.objects.filter(to_user=request.user, flag=1)
        return notices


def news(request):
    n = news_count(request)
    for f in n:
        f.flag = 0
        f.save()
    return render(request, 'users/news.html', {'news': n, })
