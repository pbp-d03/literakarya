from django import forms
from .models import Comment

class KomenForm(forms.ModelForm):
    class Meta:
        model = Comment
        
        fields = ['isi_komen']
        
        labels = {
            'isi_komen': (''),
        }
        
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['isi_komen'].widget.attrs.update({ 
            'required':'False', 
            'name':'isi_komen', 
            'id':'teks-komen', 
            'type':'text-area', 
            'placeholder':'Komentar',
            'rows':"2", 
            }) 