from django import forms
from .models import ShortenedURL


class URLShortenerForm(forms.ModelForm):
    class Meta:
        model = ShortenedURL
        fields = ['original_url']
        widgets = {
            'original_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter URL to shorten'})
        }

    def clean_original_url(self):
        url = self.cleaned_data['original_url']
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return url
