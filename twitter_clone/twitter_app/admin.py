from django.contrib import admin
from .models import Post, Comment, Category, News, Forum, Joblist

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(News)
admin.site.register(Forum)
admin.site.register(Joblist)