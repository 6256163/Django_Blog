# coding=utf-8
from __future__ import unicode_literals
from blog.permissions import IsOwnerOrReadOnly
from django.contrib import messages,auth
from django.shortcuts import render, get_object_or_404
from django import http
from blog.serializers import BlogSerializer, ReplySerializer, ReplyInReplySerializer
from users.models import Notice, Relationship
from . import forms
from users import forms as user_form
from .models import Blog, Reply, ReplyInReply
from rest_framework import permissions, viewsets,renderers
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
# Create your views here.


class BlogViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    renderer_classes = (renderers.TemplateHTMLRenderer,renderers.JSONRenderer,)
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_blog = self.get_serializer(instance)
        replies_queryset = Reply.objects.filter(blog=instance)
        page = self.paginate_queryset(replies_queryset)
        if page is not None:
            serializer_reply = ReplySerializer(*[page], **{"context": self.get_serializer_context(), "many": True})
            return Response({"blog":serializer_blog.data, "replies":self.get_paginated_response(serializer_reply.data).data},template_name='blog/detail.html')

        serializer_reply = ReplySerializer(replies_queryset, context=self.get_serializer_context(), many=True)
        return Response({"blog":serializer_blog.data, "replies":serializer_reply.data},template_name='blog/detail.html')

    def create(self, request, *args, **kwargs):
        request.data['blog_title']=request.data['blog_title'].replace("\n", "")
        #request.data['blog_text']=request.data['blog_text'].replace("\n", "<br>")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=302, headers=headers)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by("-pub_date")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return Response({'blog': self.get_paginated_response(serializer.data).data, 'form': user_form.RegisterForm}, template_name='blog/index.html')
        serializer = self.get_serializer(queryset, many=True)
        return Response({'blog': serializer, 'user': request.user, 'form': user_form.RegisterForm},template_name='blog/index.html')


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    renderer_classes = (renderers.TemplateHTMLRenderer, renderers.JSONRenderer)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_reply = self.get_serializer(instance)
        replies_in_reply_queryset = ReplyInReply.objects.filter(reply=instance)
        page = self.paginate_queryset(replies_in_reply_queryset)
        if page is not None:
            serializer_replies_in_reply = ReplyInReplySerializer(*[page], **{"context": self.get_serializer_context(), "many": True})
            return Response(
                {"reply": serializer_reply.data, "replies_in_reply": self.get_paginated_response(serializer_replies_in_reply.data).data},
                template_name='blog/reply_in_reply.html')

            serializer_replies_in_reply = ReplyInReplySerializer(replies_in_reply_queryset, context=self.get_serializer_context(), many=True)
        return Response({"reply": serializer_reply.data, "replies_in_reply": serializer_replies_in_reply.data},
                        template_name='blog/reply_in_reply.html')


class ReplyInReplyViewSet(viewsets.ModelViewSet):
    queryset = ReplyInReply.objects.all()
    serializer_class = ReplyInReplySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = ReplyInReply.objects.all()
        reply = self.request.GET.get('reply', None)
        if reply is not None:
            queryset = queryset.filter(reply=reply)
        return queryset


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'blogs': reverse('blog-list', request=request, format=format)
    })


def home(request):
    return render(request, 'blog/home.html')



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
            return render(request, 'blog/index.html',{'user': request.user})
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




