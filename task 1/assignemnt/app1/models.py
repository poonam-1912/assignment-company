from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
import string
import random

class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=10, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    @classmethod
    def create_short_code(cls):
        characters = string.ascii_letters + string.digits
        short_code = ''.join(random.choice(characters) for _ in range(7))
        while cls.objects.filter(short_code=short_code).exists():
            short_code = ''.join(random.choice(characters) for _ in range(7))
        return short_code

    def is_expired(self):
        return self.expires_at and self.expires_at < timezone.now()

