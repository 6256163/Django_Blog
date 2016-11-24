from django.contrib import admin

from .models import Blog, Reply


# Register your models here.

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1
    fieldsets = [
        ('Reply information', {'fields': ['reply_text']}),
        ('Date information', {'fields': ['pub_date']})
    ]


class BlogAdmin(admin.ModelAdmin):
    # fields = ['blog_title', 'blog_text', 'pub_date']
    fieldsets = [
        ('Blog information', {'fields': ['blog_title', 'blog_text']}),
        # (None,               {'fields': ['blog_text']}),
        ('Date information', {'fields': ['pub_date']})
    ]
    inlines = [ReplyInline]
    list_display = ('blog_title', 'pub_date', 'was_published_recently')
    list_filter = ['blog_title', 'pub_date']
    search_fields = ['blog_title']


admin.site.register(Blog, BlogAdmin)
