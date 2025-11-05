from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin Interface
    path('admin/', admin.site.urls),
    
    # Core app URLs (This assumes the profiles app handles the root path '')
    path('', include('profiles.urls')),
    
    # Standard Django Authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),

    # 🌟 NEW LINE ADDED: Include the URLs for the posts application
    # This makes URLs like /posts/1/like/ available
    path('posts/', include('posts.urls')), 
]

# Serving media and static files during development
if settings.DEBUG:
    # Handle user-uploaded media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Handle collected static files (optional but safe)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)