from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    # 1. Django Admin
    path('admin/', admin.site.urls),
    
    # 2. Profiles (Home/Root) 
    # This handles the main feed, profile viewing, and editing
    path('', include('profiles.urls')),
    
    # 3. Authentication
    # Provides built-in login/logout logic
    path('accounts/', include('django.contrib.auth.urls')),

    # 4. Posts
    # This handles specific post interactions if you have a separate posts/urls.py
    path('posts/', include('posts.urls')), 
]

# 5. Static and Media Files (CRITICAL for Laptop Browsing)
# This allows Django to serve the images you upload from your laptop 
# while you are in development mode (DEBUG = True)
if settings.DEBUG:
    # Serves images from the /media/ folder
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serves CSS/JS from the /static/ folder
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)