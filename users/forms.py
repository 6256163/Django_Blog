# coding=utf-8
from __future__ import unicode_literals
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label=u"用户名",
        max_length=30,
    )

    email = forms.EmailField(label='邮箱', )

    password_1 = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
    )
    password_2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput,
    )
    class Meta:
        model = User
        fields = ['username', 'password_1','password_2', 'email', 'first_name', 'last_name']


class LoginForm(forms.Form):
    username = forms.CharField(
        label="username",
        max_length=30,
    )
    password = forms.CharField(widget=forms.PasswordInput)

class FollowForm(forms.Form):
    pass