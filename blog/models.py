import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

# Create your models here.


class Blog(models.Model):
    user = models.ForeignKey(User)
    highlighted = models.TextField()
    blog_title = models.CharField(max_length=100)
    blog_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.blog_title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)


class Reply(models.Model):
    blog = models.ForeignKey(Blog)
    user = models.ForeignKey(User)
    reply_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date replied', auto_now_add=True)

    def __str__(self):
        return self.reply_text
