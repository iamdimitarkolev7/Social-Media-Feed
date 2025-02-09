# core/admin.py

from django.contrib import admin
from .models import Profile, Post, Comment, LikePost, FollowersCount

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LikePost)
admin.site.register(FollowersCount)