from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from . import forms
from django import http


# Create your views here.

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


def user_info(request):
    """
    Gte user info: username, email, first_name, last_name, permission.
    :param request:
    :return: to user info page
    """
    if not request.user.is_authenticated():
        return http.HttpResponseRedirect('users/login')
    else:
        permission = request.user.user_permissions.all()
        return render(request, 'users/user_info.html', {'user': request.user, "permission": permission})
