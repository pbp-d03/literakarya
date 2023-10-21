from django.db import models

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

