from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=300, blank=True)
    
    # CHANGED: Using FileField instead of ImageField to bypass Pillow requirement.
    # This allows you to "Browse" your laptop for files.
    image = models.FileField(
        upload_to='profile_pics/', 
        default='profiles/images/default_profile.png', 
        blank=True
    )
    
    location = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    contact = models.CharField(max_length=100, blank=True)
    education = models.TextField(blank=True)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    
    # CHANGED: FileField allows for local file browsing without Pillow validation.
    image = models.FileField(upload_to='post_images/', blank=True, null=True)
    
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s post - {self.created_at.strftime('%Y-%m-%d')}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"

class Endorsement(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='endorsements')
    endorser = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='given_endorsements')
    skill = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('profile', 'endorser', 'skill')