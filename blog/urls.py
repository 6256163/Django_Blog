from django.conf.urls import url
from blog import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<blog_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<blog_id>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<blog_id>[0-9]+)/reply/$', views.reply_blog, name='reply'),
    url(r'^(?P<blog_id>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^blogs/$', views.BlogList.as_view(), name= 'BlogList'),
    url(r'^blogs/(?P<blog_id>[0-9]+)/$', views.BlogDetail.as_view(), name = 'BlogDetail'),
]
urlpatterns = format_suffix_patterns(urlpatterns)