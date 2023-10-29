from django.forms import ModelForm, TextInput, Textarea, URLInput
from ereading.models import Ereading

class EreadingForm(ModelForm):
    class Meta:
        model = Ereading
        fields = ["title", "author", "description", "link"]
        widgets = {
            'title': TextInput(attrs={'placeholder': 'Laskar Pelangi'}),
            'author': TextInput(attrs={'placeholder': 'Andrea Hirata'}),
            'description': Textarea(attrs={'placeholder': 'Buku ini berkisah tentang masa sekolahnya.'}),
            'link': URLInput(attrs={'placeholder': 'https://example.com'}),
        }