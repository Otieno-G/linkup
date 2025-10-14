# profiles/models.py (Complete and Correct)

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# ===============================================
# 1. User Profile Model
# ===============================================

class UserProfile(models.Model):
    """Extends the built-in Django User model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    profile_picture = models.ImageField( 
        upload_to='profiles/', 
        blank=True, 
        null=True
    )
    
    job_title = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    contact = models.CharField(max_length=100, blank=True) 
    skills = models.TextField(blank=True) 
    education = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.user.username

# -----------------------------------------------

# ===============================================
# 2. Post Model (RESTORED) ✅
# ===============================================

class Post(models.Model):
    """Represents a single post created by a user."""
    # Assuming the Post links directly to the Django User
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') 
    content = models.TextField()
    
    image = models.ImageField(
        upload_to='posts_images/', 
        blank=True,                 
        null=True                   
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.user.username} - {self.content[:30]}..." 
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

# -----------------------------------------------

# ===============================================
# 3. Comment Model (RESTORED) ✅
# ===============================================

class Comment(models.Model):
    """Represents a comment on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # Assuming the Comment links directly to the Django User
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments') 
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username}: {self.content[:20]}..."

# -----------------------------------------------

# ===============================================
# 4. Like Model (RESTORED) ✅
# ===============================================

class Like(models.Model):
    """Tracks a like on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user') 

    def __str__(self):
        return f"{self.user.username} likes post {self.post.pk}"
    
# -----------------------------------------------

# ===============================================
# 5. Endorsement Model
# ===============================================

class Endorsement(models.Model):
    # 'profile' is the profile being endorsed
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_endorsements')
    # 'endorser' is the user giving the endorsement
    endorser = models.ForeignKey(UserProfile, related_name='given_endorsements', on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'endorser', 'skill') 

    def __str__(self):
        return f"{self.endorser.user.username} endorsed {self.profile.user.username}'s skill: {self.skill}"