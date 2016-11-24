from blog.models import Blog
from django import forms


class ReplyForm(forms.Form):
    reply_text = forms.CharField(min_length=5, widget=forms.TextInput)


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['blog_title', 'blog_text', ]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
