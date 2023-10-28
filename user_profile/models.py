from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null = True)
    last_name = models.CharField(max_length=100, blank=True, null = True)
    bio = models.TextField(blank=True, null = True)    
    address = models.CharField(max_length=400, blank=True, null = True)
    favorite_genre1 = models.CharField(max_length=100, blank=True, null = True)
    favorite_genre2 = models.CharField(max_length=100, blank=True, null = True)
    favorite_genre3 = models.CharField(max_length=100, blank=True, null = True)

    def __str__(self):
        return self.user.username

#create profile when new user sign up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)

def is_complete(self):
    # Periksa apakah semua bidang yang diperlukan telah diisi
    return all([
        self.first_name,
        self.last_name,
        self.bio,
        self.address,
        self.favorite_genre1,
        self.favorite_genre2,
        self.favorite_genre3
    ])
