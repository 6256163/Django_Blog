from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Blog, Reply
from . import forms
from django import http


# Create your views here.

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
            relies=Reply.objects.filter(blog=each_blog).order_by('-pub_date')
            data.append((each_blog,relies[0] if relies else None, len(relies)))
        # Create new blog
        if request.method == "POST":
            if not request.user.is_authenticated():
                return http.HttpResponseRedirect('/users/login')
            form = forms.BlogForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get("blog_title")
                text = form.cleaned_data.get("blog_text")
                if request.user.has_perm('add_blog'):
                    Blog.objects.create(user=request.user, blog_title=title, blog_text=text)
                    return http.HttpResponseRedirect("/blog")
                else:
                    return render(request, 'blog/index.html',
                                  {'latest_list': data, 'form': form, 'user': request.user,
                                   'error': "No permission to add blog."})
        else:
            form = forms.BlogForm()
            for a in data:
                print (a[0].blog_title)
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
            Reply.objects.create(blog=blog, reply_text=text, user = request.user)
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
