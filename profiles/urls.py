from django.urls import path
from . import views # Import views from the same directory/app

# Set the application namespace
app_name = 'profiles'

urlpatterns = [
    # --- CORE AUTHENTICATION VIEWS ---
    
    # Homepage/Feed
    path('', views.home, name='home'), 
    
    # Custom Authentication Views (Matching functions in profiles/views.py)
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),

    
    
    # --- POSTS AND INTERACTION VIEWS ---
    
    # Create Post 
    path('posts/create/', views.create_post, name='create_post'),
    
    # Post List 
    path('posts/', views.post_list, name='post_list'),
    
    # Comment and Like interactions
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    
    # --- PROFILE VIEWS ---
    
    # Edit/Update Profile
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    # Profile Detail (Uses the username string in the URL)
    path('profile/<str:username>/', views.profile_detail, name='profile_detail'),

    path('search/', views.search_users, name='search_users'),
    path('explore/', views.explore_posts, name='explore_posts'),

]