# profiles/admin.py

from django.contrib import admin
# Removed the redundant 'from django.contrib import admin' later in the file

from .models import UserProfile, Post, Comment, Like

# -----------------------------------------------------------------
# Removed the following duplicate registrations:
# admin.site.register(UserProfile)
# admin.site.register(Post)
# admin.site.register(Comment)
# admin.site.register(Like)
# -----------------------------------------------------------------

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # This registers UserProfile and provides custom admin options
    list_display = ('user', 'location', 'created_at')
    search_fields = ('user__username', 'location')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Fixed the PostAdmin list_display. Assuming the 'user' field is the author.
    list_display = ('user', 'content', 'created_at') 
    # Adjusted search_fields to match the ForeignKey to User (which is 'user' on the Post model)
    search_fields = ('user__username', 'content') 
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'created_at')
    # Adjusted search_fields to use 'author' (which is a ForeignKey to User)
    search_fields = ('author__username', 'content') 
    list_filter = ('created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    # Adjusted search_fields to use 'user' (which is a ForeignKey to User)
    search_fields = ('user__username',) 
    list_filter = ('created_at',)