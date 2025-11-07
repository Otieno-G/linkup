from django.contrib import admin
from django.urls import path, include

# ✅ Restored for media file serving during development
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

# ✅ Serve media files locally when DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
