from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    topic = models.CharField(max_length=255, null=False)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    
class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name="reply")
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)