# profiles/admin.py

from django.contrib import admin
from .models import UserProfile, Endorsement
from posts.models import Post, Comment, Like

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Added 'image' so you can see the profile pic path
    list_display = ('user', 'location', 'image', 'created_at')
    search_fields = ('user__username', 'location')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Added 'image' here so you can verify uploads in the admin list
    list_display = ('user', 'content_snippet', 'image', 'created_at') 
    search_fields = ('user__username', 'content') 
    list_filter = ('created_at',)

    # Helper to keep the admin list clean if content is long
    def content_snippet(self, obj):
        return obj.content[:50]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Your model uses 'author', so this is correct
    list_display = ('author', 'post', 'created_at')
    search_fields = ('author__username', 'content') 
    list_filter = ('created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username',) 
    list_filter = ('created_at',)

@admin.register(Endorsement)
class EndorsementAdmin(admin.ModelAdmin):
    list_display = ('profile', 'endorser', 'skill', 'created_at')