from django import forms
from notes.models import Notes
from book_page.models import Book

class NoteForm(forms.ModelForm):
    judul_buku = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label="(Pilih Buku)")

    class Meta:
        model = Notes
        fields = ['judul_catatan', 'judul_buku', 'isi_catatan', 'penanda']