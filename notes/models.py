from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    judul_catatan = models.CharField(max_length=30)
    judul_buku = models.CharField(max_length=255)
    catatan = models.TextField()
    penanda = models.TextField()
