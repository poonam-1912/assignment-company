from django.db import models

class Snippet(models.Model):
     content = models.TextField()
     encrypted_content = models.TextField(null=True, blank=True)
     secret_key = models.CharField(max_length=256, null=True, blank=True)
     created_at = models.DateTimeField(auto_now_add=True)
