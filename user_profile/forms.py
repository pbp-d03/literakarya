from django.forms import ModelForm
from user_profile.models import Profile
from django import forms

class ProfileForm(ModelForm):
    FAVORITE_GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Novels', 'Novels'),
        ('Classics', 'Classics'),
        ('Romance', 'Romance'),
        ('Horror', 'Horror'),
        ('Young Adult', 'Young Adult'),
        ('Indonesian Literature', 'Indonesian Literature'),
        ('Comedy', 'Comedy'),
        ('Thriller', 'Thriller'),
        ('Poetry', 'Poetry'),
        ('Childrens', 'Childrens'),
        ('Inspirational', 'Inspirational'),
        ('Education', 'Education'),
        ('Historical', 'Historical')
    ]

    favorite_genre1 = forms.ChoiceField(choices=FAVORITE_GENRE_CHOICES, label="Favorite Genre 1")
    favorite_genre2 = forms.ChoiceField(choices=FAVORITE_GENRE_CHOICES, label="Favorite Genre 2")
    favorite_genre3 = forms.ChoiceField(choices=FAVORITE_GENRE_CHOICES, label="Favorite Genre 3")
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'address', 'favorite_genre1', 'favorite_genre2', 'favorite_genre3']