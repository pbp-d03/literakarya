from django.forms import ModelForm
from user_profile.models import Profile
from django import forms

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'address', 'favorite_genre1', 'favorite_genre2', 'favorite_genre3']