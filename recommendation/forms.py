from django import forms
from book_page.models import Book  
from .models import Rekomendasi

class FormRekomendasi(forms.ModelForm):
    unique_genres = set(Book.objects.values_list('genre_1', flat=True))
    genre_buku = forms.ChoiceField(choices=[(x, x) for x in unique_genres])


    class Meta:
        model = Rekomendasi
        fields = ['genre_buku', 'judul_buku', 'nilai_buku', 'isi_rekomendasi']
