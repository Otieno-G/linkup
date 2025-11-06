# linkup/urls.py

from django.contrib import admin
from django.urls import path, include
# 👇 1. IMPORT NECESSARY SETTINGS MODULES 👇
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),
    
    # User Authentication URLs (Login, Logout, Password Reset, etc.)
    # Note: These typically map to Django's built-in views under /accounts/
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Profiles and General App URLs (Home, Explore, Search, etc.)
    path('', include('profiles.urls')), 
    
    # Posts URLs
    path('posts/', include('posts.urls')),
]

# 👇 2. MEDIA FILE FIX FOR PRODUCTION 👇
# This block tells Django to serve user-uploaded media files (MEDIA_URL) 
# from the directory where they are collected (MEDIA_ROOT) when DEBUG=False.
# This resolves the 404 error for the default avatar image.
if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)