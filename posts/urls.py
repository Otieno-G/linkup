# linkup/urls.py

from django.contrib import admin
from django.urls import path, include
# REMOVED: from django.conf import settings
# REMOVED: from django.conf.urls.static import static 

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

# REMOVED: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)