# coding=utf-8
from __future__ import unicode_literals
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django import http
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from blog.models import Blog
from blog.serializers import BlogSerializer
from users.models import Notice, Relationship
from . import forms
from .models import Blog, Reply




# Create your views here.


class BlogList(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


def blog_list(request,format=None):
    """
    List all blogs, or create a new blog.
    """
    if request.method == 'GET':
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True,context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BlogSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def blog_detail(request, blog_id):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Blog.DoesNotExist:
        return http.HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



def index(request):
    """
    Show the blog index. Add function to create new blog
    :param request:
    :return: to index page
    """
    if request.user.is_authenticated():
        # Show the blog list
        latest_blog_list = Blog.objects.order_by('-pub_date')
        data = list()
        for each_blog in latest_blog_list:
            relies = Reply.objects.filter(blog=each_blog).order_by('-pub_date')
            data.append((each_blog, relies[0] if relies else None, len(relies)))
        # Create new blog
        if request.method == "POST":
            if not request.user.is_authenticated():
                return http.HttpResponseRedirect('/users/login')
            form = forms.BlogForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get("blog_title")
                text = form.cleaned_data.get("blog_text")
                if request.user.has_perm('add_blog'):
                    b = Blog.objects.create(user=request.user, blog_title=title, blog_text=text)
                    return blog_notice(request, b)

                else:
                    return render(request, 'blog/index.html',
                                  {'latest_list': data, 'form': form, 'user': request.user,
                                   'error': "No permission to add blog."})
        else:
            form = forms.BlogForm()
            return render(request, 'blog/index.html',
                          {'latest_list': data, 'form': form, 'user': request.user})
    else:
        form = forms.LoginForm()
        return render(request, 'users/login.html', {'form': form})


def detail(request, blog_id):
    """
    Show the blog detail: blog content and reply content
    :param request:
    :param blog_id:
    :return: to blog detail
    """
    blog = get_object_or_404(Blog, pk=blog_id)
    form = forms.ReplyForm()
    return render(request, 'blog/detail.html', {'blog': blog, 'form': form, 'user': request.user})


def reply_blog(request, blog_id):
    """
    Add reply for specific blog
    :param request:
    :param blog_id:
    :return: return to the detail page
    """
    if request.method == "POST":
        if not request.user.is_authenticated():
            return http.HttpResponseRedirect('/users/login')
        blog = get_object_or_404(Blog, pk=blog_id)
        form = forms.ReplyForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get("reply_text")
            Reply.objects.create(blog=blog, reply_text=text, user=request.user)
            return http.HttpResponseRedirect("/blog/%s/" % blog.id)
        else:
            return render(request, 'blog/detail.html', {'blog': blog, 'form': form, 'user': request.user})
    else:
        return http.HttpResponseNotAllowed()


def edit(request, blog_id):
    """
    Modify the specific blog
    :param request:
    :param blog_id:
    :return: to blog index page
    """
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        form = forms.BlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("blog_title")
            text = form.cleaned_data.get("blog_text")
            blog.blog_title = title
            blog.blog_text = text
            blog.save()
            # Blog.objects.update(blog_title=title, blog_text=text)
        return http.HttpResponseRedirect("/blog")
    else:
        form = forms.BlogForm()
        return render(request, 'blog/edit.html', {'blog': blog, 'form': form, 'user': request.user})


def delete(request, blog_id):
    """
    delete specific blog
    :param request:
    :param blog_id:
    :return: to blog index page
    """
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.user.has_perm('delete_blog'):
        blog.delete()
    else:
        messages.add_message(request, messages.WARNING, 'Not permissons')
    return http.HttpResponseRedirect("/blog")


def blog_notice(request, b):
    if not request.user.is_authenticated():
        return http.HttpResponseRedirect('/users/login')
    else:
        r = Relationship.objects.filter(follower=request.user)
        for f in r:
            Notice.objects.create(
                from_user=request.user,
                to_user=f.current_user,
                message="我发布了新博客《%s》,快来看吧！" % (b.blog_title)
            )
        return http.HttpResponseRedirect("/blog")


class Dict():
    def __init__(self):
        self.data=[None for i in range(0,12)]

    def hash(self,key):
        return key%3

    def set(self,key,value):
        self.data[self.hash(key)]=value

    def get(self,key):
        return self.data[self.hash(key)]




