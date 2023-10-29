from django.db import models
from django.contrib.auth.models import User
from book_page.models import Book

class Rekomendasi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre_buku = models.CharField(max_length=255)  # Diubah menjadi CharField
    judul_buku = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='judul_rekomendasi')
    nilai_buku = models.DecimalField(max_digits=5, decimal_places=1)
    isi_rekomendasi = models.TextField()
    suka_buku = models.ManyToManyField(User, related_name='suka_rekomendasi', blank=True)
    tanggal = models.DateTimeField(auto_now_add=True)
