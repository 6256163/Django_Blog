from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^permission/$', views.show_permission, name='show_permission'),
    url(r'^my_info/$', views.my_info, name='my_info'),
    url(r'^(?P<user_id>[0-9]+)/user_info/$', views.user_info, name='user_info'),
    url(r'^(?P<user_id>[0-9]+)/follow/$', views.follow, name='follow'),
    url(r'^(?P<user_id>[0-9]+)/unfollow/$', views.unfollow, name='unfollow'),
    url(r'^news/$', views.news, name='news'),
]
