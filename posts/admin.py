from django.contrib import admin

from .models import Tag, Content, Category, Post, PostImage

# Register your models here.
admin.site.register(Tag)
admin.site.register(Content)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostImage)