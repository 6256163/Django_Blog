from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<blog_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<blog_id>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<blog_id>[0-9]+)/reply/$', views.reply_blog, name='reply'),
    url(r'^(?P<blog_id>[0-9]+)/delete/$', views.delete, name='delete'),

]
