from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# -------------------------------
# User Profile
# -------------------------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=300, blank=True)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    location = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)  # Comma-separated
    job_title = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    contact = models.CharField(max_length=100, blank=True)
    education = models.TextField(blank=True)
    following = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


# -------------------------------
# Post
# -------------------------------
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def is_liked_by_user(self, user):
        if not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()

    def __str__(self):
        return f'Post by {self.user.username} at {self.created_at.strftime("%Y-%m-%d")}'


# -------------------------------
# Comment
# -------------------------------
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'


# -------------------------------
# Like
# -------------------------------
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user.username} likes {self.post}'


# -------------------------------
# Endorsement
# -------------------------------
class Endorsement(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='endorsements')
    endorser = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='given_endorsements')
    skill = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('profile', 'endorser', 'skill')

    def __str__(self):
        return f'{self.endorser.user.username} endorsed {self.profile.user.username} for {self.skill}'
