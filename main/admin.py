from django.contrib import admin
from .models import Blog, BlogCategory, BlogSeries
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    #Change order of field
    '''fields = ['blog_title',
	'blog_published',
	'blog_content']
	'''
    #Seperate fields into sets
    fieldsets = [
    ("Title/date", {'fields': ["blog_title", "blog_published"]}),
    ("URL", {'fields': ["blog_slug"]}),
    ("Series", {'fields': ["blog_series"]}),
    ("Content", {"fields": ["blog_content"]})
    ]

    formfield_overrides = {
    models.TextField: {'widget': TinyMCE()},
    }
    

admin.site.register(BlogSeries)
admin.site.register(BlogCategory)
admin.site.register(Blog, BlogAdmin)
