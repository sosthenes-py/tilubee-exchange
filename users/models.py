import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
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
    avatar_id = models.IntegerField(default=3)
    status = models.BooleanField(default=False)
    status_reason = models.CharField(max_length=100, default='')
    last_access = models.DateTimeField(default=timezone.now)

    groups = models.ManyToManyField(Group, related_name="appuser_set")
    user_permissions = models.ManyToManyField(Permission, related_name="appuser_permissions_set")

    def is_blacklisted(self):
        if hasattr(self, 'blacklist'):
            return True
        return False



class Session(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='session')
    uid = models.CharField(max_length=30, editable=False)
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now=True)


class UserWallet(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='user_wallets')
    currency = models.CharField(max_length=20, default='')
    currency_name = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    network = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(default=timezone.now)

class UserBankAccount(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='user_bank_accounts')
    number = models.CharField(max_length=20, default='')
    bank = models.CharField(max_length=20, default='')
    bank_code = models.CharField(max_length=10, default='')
    name = models.CharField(max_length=20, default='')
    created_at = models.DateTimeField(default=timezone.now)


class Notification(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100, default='')
    body = models.TextField(default='', max_length=10000)
    created_at = models.DateTimeField(default=timezone.now)


class VirtualAccount(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='virtual_accounts')
    number = models.CharField(max_length=20, default='')
    bank = models.CharField(max_length=20, default='')
    name = models.CharField(max_length=20, default='')
    created_at = models.DateTimeField(default=timezone.now)
