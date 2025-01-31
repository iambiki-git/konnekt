from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='posts_image/', default='posts_image/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption[:30] if self.caption else "No Caption"
