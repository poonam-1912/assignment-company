from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .models import ShortenedURL
from .form import URLShortenerForm
from app1.models import *

@require_http_methods(["GET", "POST"])
def home(request):
    if request.method == 'POST':
        form = URLShortenerForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            url.short_code = ShortenedURL.create_short_code()
            url.save()
            return render(request, 'shortener/result.html', {'shortened_url': url})
    else:
        form = URLShortenerForm()
    return render(request, 'shortener/home.html', {'form': form})

@require_http_methods(["GET"])
def redirect_to_original(request, short_code):
    url = get_object_or_404(ShortenedURL, short_code=short_code)
    if url.is_expired():
        return render(request, 'shortener/expired.html')
    return HttpResponseRedirect(url.original_url)