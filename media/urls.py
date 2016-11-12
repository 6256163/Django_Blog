from django.conf.urls import url
from media import views




# Create a router and register our viewsets with it.


urlpatterns = [
    url(r'^fileUpload/', views.fileUpload, name='fileUpload'),

]

