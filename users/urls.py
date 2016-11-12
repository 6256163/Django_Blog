from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from users import views
from users.views import UserViewSet



# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet, base_name="user")

user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    url(r'^register_verification/', views.register_verification, name='register_verification'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register_login_success/', views.register_login_success, name='register_login_success'),
    url(r'^my_info/$', views.my_info, name='my_info'),
    url(r'^update_user_info/$', views.update_user_info, name='update_user_info'),
    url(r'^headimg_setting/$', views.headimg_setting, name='headimg_setting'),

    #url(r'^permission/$', views.show_permission, name='show_permission'),
    #url(r'^(?P<user_id>[0-9]+)/follow/$', views.follow, name='follow'),
    #url(r'^(?P<user_id>[0-9]+)/unfollow/$', views.unfollow, name='unfollow'),
    #url(r'^news/$', views.news, name='news'),
    url(r'^', include(router.urls)),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
]

