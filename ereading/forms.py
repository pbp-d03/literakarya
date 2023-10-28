from django.forms import ModelForm
from ereading.models import Ereading

class EreadingForm(ModelForm):
    class Meta:
        model = Ereading
        fields = ["title", "author", "description", "link"]