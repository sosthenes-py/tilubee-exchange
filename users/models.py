import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class AppUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    uid = models.CharField(max_length=9, unique=True)


class Session(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='session')
    uid = models.CharField(max_length=30, editable=False)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now=True)
