# posts/urls.py

from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # Main post feed/list (e.g., /posts/)
    path('', views.post_list, name='post_list'), 
    
    # Create a new post (e.g., /posts/create/)
    path('create/', views.create_post, name='create_post'),
    
    # View a single post (e.g., /posts/123/)
    path('<int:post_pk>/', views.post_detail, name='post_detail'),

    # Handle Liking/Unliking (This is the feature we implemented)
    path('<int:post_pk>/like/', views.like_post, name='like_post'), 
    
    # Handle Commenting
    path('<int:post_pk>/comment/', views.add_comment, name='add_comment'),
]