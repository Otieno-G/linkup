# In profiles/views.py

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
        
        # 🎯 Ensure this line is exactly correct:
        return redirect('profiles:post_list', username=request.user.username) 
    
    return render(request, 'profiles/create_post.html', {'form': form})