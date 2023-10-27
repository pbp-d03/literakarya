from django.db import models
from django.contrib.auth.models import User
from book_page.models import Book

class Recommendation(models.Model):
    MOOD_CHOICES = [
        ('happy', '😊'),
        ('sad', '😢'),
        ('neutral', '😐'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, default='neutral')
    book_title = models.ForeignKey(Book, on_delete=models.CASCADE)    
    rating = models.DecimalField(max_digits=5, decimal_places=1)
    recommend = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_recommendations', blank=True)
    date = models.DateTimeField(auto_now_add=True)


class Music(models.Model):
    spotify_url = models.URLField()
    date = models.DateTimeField(auto_now_add=True)

