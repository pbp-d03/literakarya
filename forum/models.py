from django.db import models
# from main.models import User

# Create your models here.

class Topic(models.Model):
    # user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    subject = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    message = models.TextField()
    date = models.DateTimeField()
    
class Reply(models.Model):
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE, related_name="reply")
    # user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    body = models.TextField()
    date = models.DateTimeField()