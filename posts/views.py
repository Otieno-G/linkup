from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator 
from django.db.models import Sum

# Import Models from their respective apps
from profiles.models import UserProfile, Endorsement
from posts.models import Post, Comment

# Import Forms 
from profiles.forms import SignupForm, PostForm, ProfileForm, CommentForm

# --- CORE APPLICATION VIEWS ---

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    post_form = PostForm()
    return render(request, 'profiles/home.html', {
        'posts': posts,
        'post_form': post_form
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
    
    # 1. Fetch user's posts
    user_posts_list = Post.objects.filter(user=target_user).order_by('-created_at')
    
    # 2. Add Pagination
    paginator = Paginator(user_posts_list, 5) 
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # 3. Check follow status safely
    following_profile = False
    if request.user.is_authenticated and request.user != target_user:
        following_profile = request.user.userprofile.following.filter(id=profile.id).exists()

    # 4. Calculate total likes received across all their posts
    # Using .count() in a loop or aggregate for the stats bar
    total_likes = sum(post.likes.count() for post in user_posts_list)

    context = {
        'profile': profile,
        'posts': posts,
        'following_profile': following_profile,
        'total_likes_received': total_likes,
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

# Match 'post_pk' with the URL pattern to fix routing errors
@login_required
def like_post(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'profiles:home'))

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'profiles/post_detail.html', {'post': post})