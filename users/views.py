# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from . import forms
from django import http
from .models import Relationship, Notice
from rest_framework import viewsets
from users.serializers import UserSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    允许查看和编辑user 的 API endpoint
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


def register(request):
    """
    Regist a new user
    :param request:
    :return: to login page
    """
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return http.HttpResponseRedirect("/users/login")
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = forms.RegisterForm()
        return render(request, 'users/register.html', {'form': form})


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
                    return http.HttpResponseRedirect("/blog")
                else:
                    return render(request, 'users/login.html', {'error': "account disabled"})
            else:
                return render(request, 'users/login.html', {'error': "password error or account not existed"})
        else:
            return render(request, 'users/login.html', {'form': form})
    else:
        form = forms.LoginForm()
        return render(request, 'users/login.html', {'form': form})


def logout(request):
    """
    logout user
    :param request:
    :return: to blog index
    """
    auth.logout(request)
    return http.HttpResponseRedirect("/blog")


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
        return http.HttpResponseRedirect('users/login')
    else:
        n = news_count(request)
        return render(request, 'users/my_info.html', {'user': request.user,
                                                      'news':len(n),
                                                      "permission": request.user.user_permissions.all(),
                                                      'followers': find_all_followers(request),
                                                      })


def user_info(request, user_id):
    if not request.user.is_authenticated():
        return http.HttpResponseRedirect('users/login')
    else:
        user = get_object_or_404(User, pk=user_id)
        try:
            Relationship.objects.get(current_user = request.user, follower = user)
        except Relationship.DoesNotExist:
            return render(request, 'users/user_info.html', {'user': user,
                                                            "permission": user.user_permissions.all(),
                                                            'relation': False})
        else:
            return render(request, 'users/user_info.html', {'user': user,
                                                            "permission": user.user_permissions.all(),
                                                            'relation': True})


def follow(request, user_id):
    if not request.user.is_authenticated():
        return http.HttpResponseRedirect('users/login')
    else:
        try:
            r = Relationship(current_user= request.user, follower= User.objects.get(pk=user_id))
            r.save()
        except Exception,e:
            return user_info(request, user_id)
        else:
            return user_info(request, user_id)


def unfollow(request, user_id):
    if not request.user.is_authenticated():
        return http.HttpResponseRedirect('users/login')
    else:
        Relationship.objects.filter(current_user=request.user, follower=User.objects.get(pk=user_id)).delete()
        return user_info(request, user_id)

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
        notices = Notice.objects.filter(to_user = request.user, flag=1)
        return notices


def news(request):
    n = news_count(request)
    for f in n:
        f.flag=0
        f.save()
    return render(request, 'users/news.html', {'news': n,})