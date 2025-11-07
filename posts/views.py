from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from .models import Post, Like, Comment  # Ensure these models exist

# ------------------------------------------------------------------
# 1. Post Feed View
# ------------------------------------------------------------------
def post_list(request):
    """
    Displays the main post feed.
    Replace this with a template and real post query later.
    """
    return HttpResponse("<h1>Post Feed (post_list view)</h1><p>The server is now running successfully.</p>")

# ------------------------------------------------------------------
# 2. Create Post View
# ------------------------------------------------------------------
@login_required
def create_post(request):
    """
    Handles the creation of a new post.
    """
    return HttpResponse("<h1>Create Post View</h1>")

# ------------------------------------------------------------------
# 3. Post Detail View
# ------------------------------------------------------------------
def post_detail(request, post_pk):
    """
    Displays a single post with its comments.
    """
    return HttpResponse(f"<h1>Post Detail View</h1><p>Viewing post ID: {post_pk}</p>")

# ------------------------------------------------------------------
# 4. Add Comment View
# ------------------------------------------------------------------
@login_required
def add_comment(request, post_pk):
    """
    Handles POST requests to add a comment to a specific post.
    """
    return HttpResponse(f"<h1>Add Comment View</h1><p>Adding comment to post ID: {post_pk}</p>")

# ------------------------------------------------------------------
# 5. Like Post View
# ------------------------------------------------------------------
@login_required
def like_post(request, post_pk):
    """
    Toggles the like status for a post by the current user.
    """
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        user = request.user

        like_instance = Like.objects.filter(post=post, user=user).first()

        if like_instance:
            like_instance.delete()  # UNLIKE
        else:
            Like.objects.create(post=post, user=user)  # LIKE

        return_path = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(return_path) if return_path else redirect('profiles:home')

    return redirect('profiles:home')
