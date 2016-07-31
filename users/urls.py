from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^permission/$', views.show_permission, name='show_permission'),
    url(r'^user_info/$', views.user_info, name='user_info'),

]
