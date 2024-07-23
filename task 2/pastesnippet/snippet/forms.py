from django import forms
from .models import Snippet

class SnippetForm(forms.ModelForm):
    secret_key = forms.CharField(max_length=256, required=False, widget=forms.PasswordInput)

    class Meta:
        model = Snippet
        fields = ['content', 'secret_key']
