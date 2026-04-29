from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator 

# Absolute imports
from profiles.models import UserProfile, Endorsement
from posts.models import Post, Comment, Like 
from profiles.forms import SignupForm, PostForm, ProfileForm, CommentForm

# --- CORE APPLICATION VIEWS ---

def home(request):
    """
    Renders the main feed. We check like status for each post 
    to handle the UI heart icons correctly.
    """
    posts_list = Post.objects.all().order_by('-created_at')
    
    # If logged in, we can pre-identify which posts the user has liked
    liked_posts = []
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    post_form = PostForm()
    return render(request, 'profiles/home.html', {
        'posts': posts_list,
        'post_form': post_form,
        'liked_posts': liked_posts
    })

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('profiles:home')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

# --- PROFILE & SOCIAL VIEWS ---

def profile_detail(request, username):
    target_user = get_object_or_404(User, username=username)
    profile = target_user.userprofile
    
    user_posts_list = Post.objects.filter(user=target_user).order_by('-created_at')
    
    # Count total likes across all posts owned by this user
    total_likes = Like.objects.filter(post__user=target_user).count()
    
    # Pagination
    paginator = Paginator(user_posts_list, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # Check follow status
    following_profile = False
    if request.user.is_authenticated and request.user != target_user:
        following_profile = request.user.userprofile.following.filter(id=profile.id).exists()

    context = {
        'profile': profile,
        'posts': posts,
        'total_likes_received': total_likes,
        'following_profile': following_profile,
    }
    return render(request, 'profiles/profile_detail.html', context)

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles:profile_detail', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    target_profile = user_to_follow.userprofile
    my_profile = request.user.userprofile

    if target_profile != my_profile:
        if my_profile.following.filter(id=target_profile.id).exists():
            my_profile.following.remove(target_profile)
        else:
            my_profile.following.add(target_profile)
    
    return redirect('profiles:profile_detail', username=username)

# --- POSTS & INTERACTIONS ---

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
    return redirect('profiles:home')

@login_required
def like_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    like_qs = Like.objects.filter(post=post, user=request.user)

    if like_qs.exists():
        like_qs.delete()
    else:
        Like.objects.create(post=post, user=request.user)
        
    return redirect(request.META.get('HTTP_REFERER', 'profiles:home'))

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    
    # FIXED: Check like status here to avoid TemplateSyntaxError
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = Like.objects.filter(post=post, user=request.user).exists()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user # Matches your ForeignKey field name
            comment.save()
            return redirect('profiles:post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'profiles/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': form,
        'user_has_liked': user_has_liked
    })

# --- SEARCH & EXPLORE ---

def search_users(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = User.objects.filter(username__icontains=query)
    return render(request, 'profiles/search_results.html', {'results': results, 'query': query})

def explore_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'profiles/explore.html', {'posts': posts})