from django.db import models
from django.contrib.auth.models import User
from book_page.models import Book
from django.core.validators import MinValueValidator, MaxValueValidator

class Rekomendasi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre_buku = models.CharField(max_length=255)  
    judul_buku = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='judul_rekomendasi')
    nilai_buku = models.DecimalField(
        max_digits=5, 
        decimal_places=1, 
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )    
    isi_rekomendasi = models.TextField()
    likes = models.ManyToManyField(User, related_name='rekomendasi_likes')
    tanggal = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()
    
    def save(self, *args, **kwargs):
        if self.nilai_buku < 1.0 or self.nilai_buku > 5.0:
            raise ValidationError('Rating buku harus antara 1 dan 5')
        super().save(*args, **kwargs)
