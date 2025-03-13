from django.db import models
from django.utils import timezone
from users.models import AppUser



class AdminUser(models.Model):
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, default='')
    password = models.CharField(max_length=100, default='')
    level = models.CharField(max_length=50, default='super admin')
    username = models.CharField(default='', max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    uid = models.CharField(default='', max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} - {self.level.title()}'

class AdminLog(models.Model):
    user = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=100, blank=True, null=True)
    action = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"User {self.app_user.uid}, logged by {self.user.level}"


class Note(models.Model):
    user = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    app_user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    modified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(blank=True, null=True)
    super = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name}-{self.user.level} note"


class Blacklist(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100, default='default')
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(blank=True, null=True)


class AccountDetails(models.Model):
    number = models.CharField(max_length=20, default='', null=True)
    bank = models.CharField(max_length=20, default='', null=True)
    name = models.CharField(max_length=20, default='', null=True)  # bank name or Binance/Bybit as uid case may be
    uid = models.CharField(default='', max_length=20, null=True)
    account_type = models.CharField(default='bank', max_length=10)  # bank, crypto, uid
    platform = models.CharField(default='', max_length=10)   # bybit, platform


class BaseWallet(models.Model):
    currency = models.CharField(max_length=20, default='')
    currency_name = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=100, default='')
    network = models.CharField(max_length=100, default='')
    key = models.CharField(max_length=500, default='')
    created_at = models.DateTimeField(default=timezone.now)


class Webhook(models.Model):
    network = models.CharField(max_length=20, default='')
    url = models.CharField(max_length=100, default='')
    webhook_id = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(default=timezone.now)

class WebhookAddress(models.Model):
    webhook = models.ForeignKey(Webhook, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=100, default='')
    network = models.CharField(max_length=20, default='')
    created_at = models.DateTimeField(default=timezone.now)
