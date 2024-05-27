from django.contrib import admin

# Register your models here.
from .models import Article, Comment, Profile, LikeArticle

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(LikeArticle)