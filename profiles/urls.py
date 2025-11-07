from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    # --- CORE APPLICATION VIEWS ---
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),

    # --- PROFILE VIEWS ---
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/endorse/', views.add_endorsement, name='add_endorsement'),

    # --- POSTS VIEWS ---
    path('profile/<str:username>/posts/', views.post_list_view, name='post_list'),
    path('posts/create/', views.create_post, name='create_post'),

    # --- DISCOVERY & SEARCH ---
    path('search/', views.search_users, name='search_users'),
    path('explore/', views.explore_posts, name='explore_posts'),
]
