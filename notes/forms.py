from django import forms
from notes.models import Note
from book_page.models import Book

class NoteForm(forms.ModelForm):
    judul_buku = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label="(Choose a book)")

    class Meta:
        model = Note
        fields = ['judul_catatan', 'judul_buku', 'isi_catatan', 'penanda']