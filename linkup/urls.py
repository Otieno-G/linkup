# linkup/urls.py (CORRECTED CODE)

from django.contrib import admin
from django.urls import path, include

# project/urls.py

from django.contrib.auth import views as auth_views # Standard practice

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profiles.urls')),
]


urlpatterns = [
    # ... other paths ...
    path('admin/', admin.site.urls),

    # Add ALL Django authentication URLs (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # Alternatively, you can specify just the login/logout views:
    # path('login/', auth_views.LoginView.as_view(template_name='profiles/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # Include your profiles app URLs
    path('', include('profiles.urls')),
]

urlpatterns = [
    # 1. Admin path is still separate
    path('admin/', admin.site.urls),
    
    # 2. Include the profiles app for the root path and all other paths
    # This directs requests to the profiles/urls.py
    path('', include('profiles.urls')), 


]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profiles.urls')),  # or whatever your app is called
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
