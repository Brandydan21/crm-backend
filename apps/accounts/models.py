from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"