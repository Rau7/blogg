from django.contrib import admin
from .models import Post, Like, UserProfile, Follow, Hashtag

# Register your models here
admin.site.register(Post, list_display=['title', 'author', 'created_at'])
admin.site.register(Like , list_display=['user', 'post', 'created_at'])
admin.site.register(UserProfile)
admin.site.register(
    Follow,
    list_display=['follower', 'followed'],
)

admin.site.register(Hashtag)