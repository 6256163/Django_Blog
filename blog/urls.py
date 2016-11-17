from blog.views import ReplyViewSet
from django.conf.urls import url, include
from blog import views
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'blog', views.BlogViewSet)
router.register(r'replies', views.ReplyViewSet)
router.register(r'reply_in_reply', views.ReplyInReplyViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^$', views.api_root),
]
