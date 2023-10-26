from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()    
    address = models.CharField(max_length=400)
    favorite_genre1 = models.CharField(max_length=100)
    favorite_genre2 = models.CharField(max_length=100)
    favorite_genre3 = models.CharField(max_length=100)