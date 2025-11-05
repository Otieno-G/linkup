from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # Post CRUD/List Views (assuming these will be in posts/views.py)
    path('', views.post_list, name='post_list'), 
    path('create/', views.create_post, name='create_post'),
    path('<int:post_pk>/', views.post_detail, name='post_detail'), # Using post_pk for consistency

    # Interaction Views (Liking/Commenting)
    path('<int:post_pk>/comment/', views.add_comment, name='add_comment'),
    # Use the name 'like_post' as planned in the previous step's view implementation
    path('<int:post_pk>/like/', views.like_post, name='like_post'),
]