from django.db import models
from django.contrib.auth.models import User
from book_page.models import Book
    
class Notes(models.Model):
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    judul_catatan = models.CharField(max_length=30)
    judul_buku = models.CharField(max_length=255)
    isi_catatan = models.TextField()
    penanda = models.CharField(max_length=30)
    buku = models.ForeignKey(Book, null=True, on_delete=models.CASCADE)
