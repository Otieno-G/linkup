# linkup/urls.py

from django.contrib import admin
from django.urls import path, include
# 👇 REQUIRED IMPORTS 👇
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),
    
    # User Authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Profiles and General App URLs
    path('', include('profiles.urls')), 
    
    # Posts URLs
    path('posts/', include('posts.urls')),
]

# 👇 SIMPLIFIED MEDIA FIX 👇
# This is a safe way to handle default media files in small production environments.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)