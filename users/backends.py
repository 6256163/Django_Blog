# coding=utf-8
import re
from django.contrib.auth.models import User


class MyBackend(object):
    """
    自定义后端，用作登录验证
    """
    def authenticate(self, username=None, password=None):
        if username:
            # email
            if re.match("^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$", username) != None:
                try:
                    user = User.objects.get(email=username)
                    if user.check_password(password):
                        return user
                except User.DoesNotExist:
                    return None
            #nickname
            else:
                try:
                    user = User.objects.get(username=username)
                    if user.check_password(password):
                        return user
                except User.DoesNotExist:
                    return None
        else:
            return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
