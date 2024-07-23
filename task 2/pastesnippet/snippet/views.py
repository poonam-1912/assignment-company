from django.shortcuts import render, redirect, get_object_or_404
from .forms import SnippetForm
from .models import Snippet
from cryptography.fernet import Fernet
import base64
import hashlib

def encrypt_message(key, message):
    fernet = Fernet(base64.urlsafe_b64encode(hashlib.sha256(key.encode()).digest()[:32]))
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

def decrypt_message(key, encrypted_message):
    fernet = Fernet(base64.urlsafe_b64encode(hashlib.sha256(key.encode()).digest()[:32]))
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message

def create_snippet(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if form.cleaned_data['secret_key']:
                snippet.encrypted_content = encrypt_message(form.cleaned_data['secret_key'], form.cleaned_data['content'])
                snippet.content = ''
                snippet.secret_key = form.cleaned_data['secret_key']
            snippet.save()
            return redirect('view_snippet', snippet_id=snippet.id)
    else:
        form = SnippetForm()
    return render(request, 'snippet/create_snippet.html', {'form': form})

def view_snippet(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    decrypted_message = None
    if request.method == 'POST' and snippet.secret_key:
        provided_key = request.POST.get('key', '')
        if provided_key == snippet.secret_key:
            try:
                decrypted_message = decrypt_message(provided_key, snippet.encrypted_content)
            except Exception as e:
                return render(request, 'snippet/view_snippet.html', {'error': f"Decryption failed: {str(e)}"})
        else:
            return render(request, 'snippet/view_snippet.html', {'error': "Invalid key"})
    return render(request, 'snippet/view_snippet.html', {'snippet': snippet, 'decrypted_message': decrypted_message})
