from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('explore/', views.explore_posts, name='explore_posts'),
    path('create-post/', views.create_post, name='create_post'),
    path('like/<int:post_pk>/', views.like_post, name='like_post'),
    
    # ADD THIS LINE TO FIX THE SEARCH ERROR:
    path('search/', views.search_users, name='search_users'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]
