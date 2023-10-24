from django.db import models
from django.contrib.auth.models import User, AnonymousUser

class Ereading(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    last_updated = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default = AnonymousUser().id)