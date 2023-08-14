from django.contrib import admin

from social_app.models import UserProfile, Post, Comment, Follow, CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)