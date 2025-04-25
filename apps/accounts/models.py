from django.contrib.auth.models import AbstractUser
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    business_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    company_email = models.EmailField(blank=True, null=True, unique=True)
    company_phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    company_address = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'crm_company'  

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    
    '''
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    '''
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="users", null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, unique=True)  

    class Meta:
        db_table = 'crm_user'

    def __str__(self):
        return f"{self.username} ({self.role})"

    