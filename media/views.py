from django.shortcuts import render
from media.models import Image
from django import http
# Create your views here.

def fileUpload(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            img = Image.objects.create(user = request.user, path = request.FILES['files[]'])
            return http.HttpResponse(img.path.url)
        else:
            return render(request, 'blog/insert_image.html')
