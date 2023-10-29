from django.contrib import admin
from .models import Rekomendasi 

class RekomendasiAdmin(admin.ModelAdmin):
    list_display = ('judul_buku', 'genre_buku')  # Hanya menampilkan judul_buku dan genre_buku
    search_fields = ['judul_buku']  # Mencari berdasarkan judul_buku saja
    list_filter = ['genre_buku']  # Menyediakan filter untuk genre_buku

admin.site.register(Rekomendasi, RekomendasiAdmin)
