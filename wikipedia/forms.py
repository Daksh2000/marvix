from django import forms
from .models import Tag

class TagForm(forms.Form):
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter comma-separated tags'}))

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        return [tag.strip() for tag in tags.split(',') if tag.strip()]
