from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# -------------------------------
# Post Model
# -------------------------------
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    content = models.TextField()
    
    # Restored 'image' field as a FileField
    # This bypasses the Pillow requirement while allowing file uploads.
    image = models.FileField(upload_to='post_images/', blank=True, null=True)
    
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
# Like Model
# -------------------------------
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('post', 'user') 

    def __str__(self):
        return f'{self.user.username} likes {self.post}'


# -------------------------------
# Comment Model
# -------------------------------
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'