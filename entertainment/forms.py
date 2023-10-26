from django import forms
from .models import BookReview
from book_page.models import Book 

class BookReviewForm(forms.ModelForm):
    book_choices = [(book.id, book.nama_buku) for book in Book.objects.all()]

    emoticon = forms.ChoiceField(choices=[('happy', '😊'), ('sad', '😢'), ('neutral', '😐')], widget=forms.RadioSelect)
    book_title = forms.ChoiceField(choices=book_choices)  
    rating = forms.DecimalField(min_value=1.0, max_value=5.0, decimal_places=1)
    review = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = BookReview
        fields = ['emoticon', 'book_title', 'rating', 'review']
