from django.forms import ModelForm
from notes.models import Note

class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ["judul_catatan", "judul_buku", "konten_catatan", "penanda"]
        