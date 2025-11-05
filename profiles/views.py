# profiles/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q, Exists, OuterRef, Value, BooleanField
from django.core.paginator import Paginator
from django.utils import timezone 
from django.contrib import messages 

# 🌟 CRITICAL FIX: Import Post, Like, Comment from the 'posts' app
from posts.models import Post, Like, Comment 

# Import local models
from .models import UserProfile, Endorsement 
from .forms import SignupForm, PostForm, ProfileForm, CommentForm, SearchForm, EndorsementForm


# ===============================
# Authentication Views
# ===============================

def signup_view(request):
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        try:
            UserProfile.objects.create(user=user)
        except IntegrityError:
            pass
        login(request, user)
        messages.success(request, "Registration successful! Welcome to LinkUp.")
        return redirect('profiles:home')
    return render(request, 'profiles/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profiles:home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, f"Welcome back, {request.user.username}!")
        return redirect('profiles:home')
    return render(request, 'profiles/login.html', {'form': form})


def custom_logout_view(request):
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('profiles:home')


# ===============================
# Core Views (Feed/Home)
# ===============================

def home(request):
    post_form = PostForm()
    comment_form = CommentForm()
    posts_queryset = Post.objects.all().order_by('-created_at')
    
    suggested_users = User.objects.none() 

    if request.user.is_authenticated:
        # 1. Filter posts for the authenticated user's feed
        following_profiles = request.user.userprofile.following.all()
        posts_queryset = posts_queryset.filter(
            Q(user__userprofile__in=following_profiles) | Q(user=request.user)
        )
        
        # 2. ANNOTATION: Determine if the post is liked by the user
        liked_subquery = Like.objects.filter(user=request.user, post=OuterRef('pk'))
        posts_queryset = posts_queryset.annotate(is_liked=Exists(liked_subquery))
        
        # 3. PYMK LOGIC: Find suggested users
        followed_user_pks = following_profiles.values_list('user__pk', flat=True)
        exclude_pks = list(followed_user_pks) + [request.user.pk]
        
        suggested_users = User.objects.filter(
            ~Q(pk__in=exclude_pks)
        ).select_related('userprofile').order_by('?')[:5]

    else:
        # ANNOTATION: For unauthenticated users, is_liked is always False
        posts_queryset = posts_queryset[:25].annotate(is_liked=Value(False, output_field=BooleanField()))

    # 4. PREFETCHING: Optimize post query 
    posts_queryset = posts_queryset.select_related('user__userprofile').prefetch_related('likes', 'comments') 

    # 5. PAGINATION: Apply pagination to the full queryset
    paginator = Paginator(posts_queryset, 50)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'post_form': post_form,
        'comment_form': comment_form,
        'suggested_users': suggested_users, 
    }

    return render(request, 'profiles/home.html', context)


# ===============================
# 🛠️ POSTS VIEWS
# ===============================

@login_required
def create_post(request):
    """
    Handles the creation of a new post. (FIXED: The missing view)
    """
    form = PostForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        # Ensure the post is linked to the currently logged-in user
        post.user = request.user 
        post.save()
        messages.success(request, "Your post has been successfully created!")
        # Redirect to the user's post list/feed after creation
        return redirect('profiles:post_list', username=request.user.username) 
    
    # If GET or form is invalid, render the form page
    return render(request, 'profiles/create_post.html', {'form': form})


def post_list_view(request, username):
    """
    Displays a paginated list of all posts for a specific user.
    """
    # 1. Get the target user object and their profile
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.userprofile
    
    # 2. Fetch all posts by the user (using the 'user_posts' related_name)
    posts_queryset = user_obj.user_posts.all().order_by('-created_at')
    
    # 3. ANNOTATION: Determine if the post is liked by the current user
    if request.user.is_authenticated:
        liked_subquery = Like.objects.filter(user=request.user, post=OuterRef('pk'))
        posts_queryset = posts_queryset.annotate(is_liked=Exists(liked_subquery))
    else:
        posts_queryset = posts_queryset.annotate(is_liked=Value(False, output_field=BooleanField()))
        
    # 4. PREFETCHING: Optimize query
    posts_queryset = posts_queryset.select_related('user__userprofile').prefetch_related('likes', 'comments') 
        
    # 5. PAGINATION
    paginator = Paginator(posts_queryset, 10) # Show 10 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'profile': profile,
        'posts': posts,
        'comment_form': CommentForm(),
    }
    
    return render(request, 'profiles/post_list.html', context)


# ===============================
# Profile Views
# ===============================

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profiles:profile_detail', username=request.user.username)
    return render(request, 'profiles/edit_profile.html', {'form': form})


def profile_detail(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.userprofile
    
    # 🌟 CRITICAL FIX: Use the new related_name 'user_posts'
    # Fetch only a few posts for the detail view
    posts_queryset = user_obj.user_posts.all().order_by('-created_at')
    
    # Calculate total likes received by the profile's posts
    total_likes_received = Like.objects.filter(post__user=user_obj).count()
    
    # Determine follow status
    following_profile = False
    
    # ANNOTATION: Prepare posts for display with like status
    if request.user.is_authenticated:
        liked_subquery = Like.objects.filter(user=request.user, post=OuterRef('pk'))
        posts_queryset = posts_queryset.annotate(is_liked=Exists(liked_subquery))
        
        # Determine if the current user is following this profile
        if request.user.userprofile != profile:
            following_profile = request.user.userprofile.following.filter(pk=profile.pk).exists()
    else:
        posts_queryset = posts_queryset.annotate(is_liked=Value(False, output_field=BooleanField()))
            
    # Standard practice is to use Paginator even for a profile page (showing first page only)
    paginator = Paginator(posts_queryset, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
        
    endorsements = Endorsement.objects.filter(profile=profile).select_related('endorser__user')
    endorsement_form = EndorsementForm()
    comment_form = CommentForm()
    
    return render(request, 'profiles/profile_detail.html', {
        'profile': profile,
        'posts': posts,
        'endorsements': endorsements,
        'endorsement_form': endorsement_form,
        'comment_form': comment_form,
        'total_likes_received': total_likes_received,
        'following_profile': following_profile,
    })


@login_required
def follow_user(request, username):
    if request.method != 'POST':
        # Safely get HTTP_REFERER for redirect, falling back to profile_detail
        return redirect(request.META.get('HTTP_REFERER', redirect('profiles:profile_detail', username=username).url))
        
    target_user = get_object_or_404(User, username=username)
    target_profile = target_user.userprofile
    current_profile = request.user.userprofile
    
    if current_profile == target_profile:
        messages.warning(request, "You cannot follow yourself.")
        return redirect('profiles:profile_detail', username=username)
        
    is_following = current_profile.following.filter(pk=target_profile.pk).exists()

    if is_following:
        current_profile.following.remove(target_profile)
        messages.info(request, f"You are no longer following {username}.")
    else:
        current_profile.following.add(target_profile)
        messages.success(request, f"You are now following {username}.")

    # Safely get HTTP_REFERER for redirect, falling back to profile_detail
    return redirect(request.META.get('HTTP_REFERER', redirect('profiles:profile_detail', username=username).url))


@login_required
def add_endorsement(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile_to_endorse = profile_user.userprofile
    
    if request.user.userprofile == profile_to_endorse:
        messages.error(request, "You cannot endorse yourself.")
        return redirect('profiles:profile_detail', username=username)
        
    form = EndorsementForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            endorsement = form.save(commit=False)
            endorsement.profile = profile_to_endorse
            endorsement.endorser = request.user.userprofile
            endorsement.save()
            messages.success(request, f"Endorsement added for {username}.")
        except IntegrityError:
            messages.warning(request, f"You have already endorsed {username}.")
            
    return redirect('profiles:profile_detail', username=username)


# ===============================
# Discovery & Search
# ===============================

def search_users(request):
    form = SearchForm(request.GET)
    results = UserProfile.objects.none()
    
    if form.is_valid():
        query = form.cleaned_data['query']
        results = UserProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(job_title__icontains=query) | 
            Q(location__icontains=query) | 
            Q(bio__icontains=query) |
            Q(skills__icontains=query)
        ).select_related('user')
        
    return render(request, 'profiles/search_results.html', { 
        'form': form,
        'results': results
    })


def explore_posts(request):
    posts_queryset = Post.objects.all().order_by('-created_at')
    comment_form = CommentForm()
    
    # ANNOTATION: Efficiently determine if the post is liked by the current user
    if request.user.is_authenticated:
        liked_subquery = Like.objects.filter(user=request.user, post=OuterRef('pk'))
        posts_queryset = posts_queryset.annotate(is_liked=Exists(liked_subquery))
    else:
        posts_queryset = posts_queryset.annotate(is_liked=Value(False, output_field=BooleanField()))

    # PREFETCHING: Optimize query
    posts_queryset = posts_queryset.select_related('user__userprofile').prefetch_related('likes', 'comments')

    # Add Pagination to Explore View for performance
    paginator = Paginator(posts_queryset, 20) # Show 20 per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'profiles/explore.html', {
        'posts': posts,
        'comment_form': comment_form,
    })