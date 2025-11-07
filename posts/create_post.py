from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from profiles.forms import PostForm  # Adjust if your form is elsewhere
from posts.models import Post        # Ensure this model exists

@login_required
def create_post(request):
    """
    Handles the creation of a new post.
    """
    form = PostForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, "Your post has been successfully created!")

        # Redirect to the user's post list
        return redirect('profiles:post_list', username=request.user.username)

    return render(request, 'profiles/create_post.html', {'form': form})
