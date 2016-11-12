# coding=utf-8
from __future__ import unicode_literals
from django import forms
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from provinceList import provinceList
import datetime


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label=u"用户名",
        max_length=30,
        widget=forms.TextInput(attrs={"placeholder": u"请设置用户名", "id": "reg_username"})
    )

    email = forms.EmailField(label=u'邮箱',
                             widget=forms.TextInput(attrs={"placeholder": u"可用于登录和找回密码", "id": "reg_email"}))

    password = forms.CharField(
        label=u"密码",
        widget=forms.PasswordInput(attrs={"placeholder": u"请设置登录密码", "id": "reg_password"}),
    )
    password_confirm = forms.CharField(
        label=u"确认密码",
        widget=forms.PasswordInput(attrs={"placeholder": u"确认密码", "id": "reg_password_confirm"}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']


class LoginForm(forms.Form):
    username = forms.CharField(
        label="username",
        max_length=50,
    )
    password = forms.CharField(widget=forms.PasswordInput)


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class HeadImgForm(forms.Form):
    head_img = forms.ImageField(label=u'上传头像：',)



class UserInfoForm(forms.Form):
    sex = forms.ChoiceField(label=u'性别：',
                            choices=((u'男', u'男'), (u'女', u'女'),),
                            widget=forms.RadioSelect(),
                            required=False,)
    birthday = forms.DateField(label=u'生日：',
                               widget=widgets.AdminDateWidget(),)
    hometown_province = forms.CharField(label=u'出生地：',
                                        widget=forms.Select(choices=[]),
                                        required=False,)
    hometown_city = forms.CharField(widget=forms.Select(choices=[]),
                                    required=False,)
    hometown_area = forms.CharField(widget=forms.Select(choices=[]),
                                    required=False,)


    def clean(self):
        cleaned_data = super(UserInfoForm, self).clean()
        sex = cleaned_data.get("sex")
        birthday = cleaned_data.get("birthday")
        hometown_province = cleaned_data.get("hometown_province")
        hometown_city = cleaned_data.get("hometown_city")
        hometown_area = cleaned_data.get("hometown_area")

        # 性别验证
        if sex:
            if sex not in [u'男', u'女']:
                raise forms.ValidationError(
                    {'sex':"性别项错误"}
                )
        else:
            raise forms.ValidationError(
                {'sex':"性别不能为空"}
            )



        # 出生地验证
        if hometown_province:
            province_validation = False
            for province in provinceList:
                if province['name'] == hometown_province:
                    province_validation = True
                    if hometown_city:
                        city_validation = False
                        if province.get('cityList', []) != []:
                            for city in province['cityList']:
                                if city['name'] == hometown_city:
                                    city_validation = True
                                    if hometown_area:
                                        area_validation = False
                                        if city.get('areaList', []) != []:
                                            if hometown_area in city['areaList']:
                                                area_validation = True
        if province_validation == False:
            raise forms.ValidationError(
                {'province':"省份项错误"}
            )
        if city_validation == False:
            raise forms.ValidationError(
                {'city':"城市项错误"}
            )
        if area_validation == False:
            raise forms.ValidationError(
                {'area':"城区项错误"}
            )
