from django import forms
from entertainment.models import Recommendation
from book_page.models import Book 

class BookRecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['book_title', 'rating', 'recommend']

