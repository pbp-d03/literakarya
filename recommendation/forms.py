from django import forms
from book_page.models import Book  
from .models import Rekomendasi
from django.core.exceptions import ValidationError

# Dalam class FormRekomendasi
def clean_nilai_buku(self):
    nilai_buku = self.cleaned_data.get('nilai_buku')
    if nilai_buku < 0 or nilai_buku > 5:
        raise ValidationError("Rating harus antara 0 dan 5")
    return nilai_buku

class FormRekomendasi(forms.ModelForm):
    unique_genres = set(Book.objects.values_list('genre_1', flat=True))
    genre_buku = forms.ChoiceField(choices=[(x, x) for x in unique_genres])


    class Meta:
        model = Rekomendasi
        fields = ['genre_buku', 'judul_buku', 'nilai_buku', 'isi_rekomendasi']
