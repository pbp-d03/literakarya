from django.db import models
from django.contrib.auth.models import User
from book_page.models import Book

class Rekomendasi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre_buku = models.CharField(max_length=255)  
    judul_buku = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='judul_rekomendasi')
    nilai_buku = models.DecimalField(max_digits=5, decimal_places=1)
    isi_rekomendasi = models.TextField()
    likes = models.ManyToManyField(User, related_name='rekomendasi_likes')
    tanggal = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.judul_buku