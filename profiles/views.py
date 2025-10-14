# profiles/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError 
from django.db.models import Q # <--- ADDED Q IMPORT HERE
from django.http import HttpResponse 

# --- CORRECTED & CONSOLIDATED RELATIVE IMPORTS ---
from .models import UserProfile, Post, Comment, Like, Endorsement
from .forms import SignupForm, PostForm, ProfileForm, CommentForm, SearchForm, EndorsementForm 


# =============================================================
# 1. AUTHENTICATION VIEWS
# =============================================================

# Custom Login View (Login is handled by the default AuthenticationForm)
def login_view(request):
    """Handles user login using Django's built-in form."""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'title': 'Log In',
    }
    return render(request, 'profiles/login.html', context)


def custom_logout_view(request):
    """Logs the user out and redirects to home."""
    logout(request)
    return redirect('home')


def signup_view(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save() 
            
            # Create the corresponding UserProfile object immediately
            UserProfile.objects.create(user=user)
            
            login(request, user) 
            return redirect('home')
    else:
        form = SignupForm()
        
    context = {
        'form': form,
        'title': 'Sign Up',
    }
    return render(request, 'profiles/signup.html', context)


# =============================================================
# 2. CORE APPLICATION VIEWS
# =============================================================

# Home/Feed View
def home(request):
    """Displays the main index/home page content."""
    post_form = PostForm()

    # Fetch all posts, ordered newest first
    posts = Post.objects.all().order_by('-created_at') 
    
    context = {
        'posts': posts,
        'post_form': post_form,
        'greeting': 'Welcome to LinkUp!',
    }
    return render(request, 'profiles/home.html', context)

# Profile Detail View (FIXED QUERYING)
def profile_detail(request, username):
    # Retrieve the Django User, then the related UserProfile
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.userprofile 
    
    # Post model links to the User object
    posts = Post.objects.filter(user=user_obj).order_by('-created_at') 
    
    # Calculate totals 
    total_likes = sum(post.likes.count() for post in posts)
    total_comments = sum(post.comments.count() for post in posts)
    
    # Endorsements
    endorsements = Endorsement.objects.filter(profile=profile)
    endorsement_form = EndorsementForm()
    
    context = {
        'profile': profile,
        'posts': posts,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'endorsements': endorsements,
        'endorsement_form': endorsement_form,
    }
    return render(request, 'profiles/profile_detail.html', context)


def post_list(request):
    """Displays a list of all posts (or redirects to the main feed)."""
    return redirect('home') 


@login_required
def create_post(request):
    """Handles creating a new post."""
    if request.method == 'POST':
        # MUST include request.FILES for image upload
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user 
            post.save()
            return redirect('home') 
    
    return redirect('home')


@login_required
def add_comment(request, post_id):
    """Handles adding a comment to a specific post."""
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            # Comment model links 'author' to the Django User
            comment.author = request.user 
            comment.save()
            # Use post.get_absolute_url() if defined, otherwise fall back to home
            return redirect(post.get_absolute_url() or 'home') 
    return redirect('home')


@login_required
def toggle_like(request, post_id):
    """Toggles a like on a specific post."""
    post = get_object_or_404(Post, pk=post_id)
    user = request.user 

    try:
        Like.objects.get(post=post, user=user).delete() # Unlike
    except Like.DoesNotExist:
        try:
            Like.objects.create(post=post, user=user) # Like
        except IntegrityError:
             pass 

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def edit_profile(request):
    """Allows the user to edit their profile details."""
    profile = request.user.userprofile 

    if request.method == 'POST':
        # MUST pass request.FILES for image/file uploads
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, 'profiles/edit_profile.html', {'form': form})


@login_required
def add_endorsement(request, username):
    """Handles adding an endorsement to another user's profile."""
    profile_user = get_object_or_404(User, username=username)
    profile_to_endorse = profile_user.userprofile

    if request.method == 'POST':
        form = EndorsementForm(request.POST)
        if form.is_valid():
            try:
                endorsement = form.save(commit=False)
                # The profile being endorsed (the page owner)
                endorsement.profile = profile_to_endorse 
                # The person giving the endorsement (current user's profile)
                endorsement.endorser = request.user.userprofile 
                endorsement.save()
                return redirect('profile_detail', username=username)
            except IntegrityError:
                # Handle case where user tries to endorse the same skill twice
                return HttpResponse("You have already endorsed this skill for this user.", status=400)
    
    return redirect('profile_detail', username=username)


def search_users(request):
    form = SearchForm(request.GET)
    results = []
    if form.is_valid():
        query = form.cleaned_data['query']
        # Search for users whose username or bio contains the query
        results = UserProfile.objects.filter(
            Q(user__username__icontains=query) | Q(bio__icontains=query)
        )
    return render(request, 'profiles/search_results.html', {
        'form': form,
        'results': results
    })

def explore_posts(request):
    posts = Post.objects.order_by('-created_at')[:20]
    return render(request, 'profiles/explore.html', {'posts': posts})