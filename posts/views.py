# posts/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

# IMPORTANT: Ensure your Post and Like models are correctly imported
# from your posts/models.py file.
from .models import Post, Like, Comment # Assuming models are here

# ------------------------------------------------------------------
# 1. Post Feed View (Required by posts/urls.py)
# ------------------------------------------------------------------
def post_list(request):
    """
    Displays the main post feed.
    """
    # Placeholder: You will eventually query the database and render a template.
    # posts = Post.objects.all().order_by('-created_at')
    # return render(request, 'posts/post_list.html', {'posts': posts})
    return HttpResponse("<h1>Post Feed (post_list view)</h1><p>The server is now running successfully.</p>")

# ------------------------------------------------------------------
# 2. Create Post View
# ------------------------------------------------------------------
@login_required
def create_post(request):
    """
    Handles the creation of a new post.
    """
    # Placeholder
    return HttpResponse("<h1>Create Post View</h1>")

# ------------------------------------------------------------------
# 3. Post Detail View
# ------------------------------------------------------------------
def post_detail(request, post_pk):
    """
    Displays a single post with its comments.
    """
    # Placeholder
    # post = get_object_or_404(Post, pk=post_pk)
    # return render(request, 'posts/post_detail.html', {'post': post})
    return HttpResponse(f"<h1>Post Detail View</h1><p>Viewing post ID: {post_pk}</p>")

# ------------------------------------------------------------------
# 4. Add Comment View
# ------------------------------------------------------------------
@login_required
def add_comment(request, post_pk):
    """
    Handles POST requests to add a comment to a specific post.
    """
    # Placeholder
    return HttpResponse(f"<h1>Add Comment View</h1><p>Adding comment to post ID: {post_pk}</p>")


# ------------------------------------------------------------------
# 5. Like Post View (Core Interaction Logic)
# ------------------------------------------------------------------
@login_required
def like_post(request, post_pk):
    """
    Toggles the like status for a post by the current user.
    """
    if request.method == 'POST':
        # Safely retrieve the post or return a 404
        post = get_object_or_404(Post, pk=post_pk)
        user = request.user
        
        # Check if the Like object already exists
        like_instance = Like.objects.filter(post=post, user=user).first()

        if like_instance:
            like_instance.delete() # UNLIKE
        else:
            Like.objects.create(post=post, user=user) # LIKE

        # Redirect back to the page the user came from (HTTP_REFERER)
        return_path = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(return_path) if return_path else redirect('profiles:home')
            
    # If a user tries to access this view via GET, redirect them away
    return redirect('profiles:home')