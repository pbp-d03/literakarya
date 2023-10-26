from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    MOOD_CHOICES = [
        ('happy', '😊'),
        ('sad', '😢'),
        ('neutral', '😐'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, default='neutral')
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    review = models.TextField()
    points = models.IntegerField(default=10)

    def __str__(self):
        return f"Review by {self.user.username} for '{self.book.title}'"

class Reward(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='rewards/')
    points_required = models.IntegerField()

    def __str__(self):
        return self.name

class UserReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.reward.name}"

class Music(models.Model):
    spotify_url = models.URLField()

    def __str__(self):
        return self.title