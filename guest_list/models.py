from django.db import models
from django.utils import timezone

# Create your models here.

class Guest(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=9, default='not-sent')
    qr_code_path = models.ImageField(upload_to='qr_codes')
    created_at = models.DateTimeField(default=timezone.now)
    registration_code = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} {self.email} {self.created_at}"

    class Meta: 
        ordering = ['first_name', 'last_name']
