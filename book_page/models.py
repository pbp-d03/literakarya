from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    nama_buku = models.TextField(null=True,blank=True)
    gambar_buku = models.TextField(null=True,blank=True)
    author = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    rating = models.FloatField(null=True,blank=True)
    jumlah_rating = models.TextField(null=True,blank=True)
    genre_1 = models.TextField(null=True,blank=True)
    genre_2 = models.TextField(null=True,blank=True)
    genre_3 = models.TextField(null=True,blank=True)
    genre_4 = models.TextField(null=True,blank=True)
    genre_5 = models.TextField(null=True,blank=True)
    jumlah_halaman = models.IntegerField(null=True,blank=True)
    waktu_publikasi = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.nama_buku

class Komen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buku = models.ForeignKey(Book, on_delete=models.CASCADE)
    isi_komen = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    likes = models.IntegerField()
    dislikes = models.IntegerField()

