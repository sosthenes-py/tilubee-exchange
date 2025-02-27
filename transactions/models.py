from django.db import models
from django.utils import timezone

from users.models import AppUser, UserBankAccount


# Create your models here.
class Asset(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='assets')
    ada = models.FloatField(default=0)
    bch = models.FloatField(default=0)
    bnb = models.FloatField(default=0)
    btc = models.FloatField(default=0)
    busd = models.FloatField(default=0)
    dash = models.FloatField(default=0)
    doge = models.FloatField(default=0)
    eth = models.FloatField(default=0)
    ftm = models.FloatField(default=0)
    link = models.FloatField(default=0)
    ltc = models.FloatField(default=0)
    matic = models.FloatField(default=0)
    ngn = models.FloatField(default=0)
    neo = models.FloatField(default=0)
    ont = models.FloatField(default=0)
    shib = models.FloatField(default=0)
    sol = models.FloatField(default=0)
    trx = models.FloatField(default=0)
    ton = models.FloatField(default=0)
    usdc = models.FloatField(default=0)
    usdt = models.FloatField(default=0)
    wbtc = models.FloatField(default=0)
    xlm = models.FloatField(default=0)
    xmr = models.FloatField(default=0)
    xrp = models.FloatField(default=0)
    yfi = models.FloatField(default=0)
    zec = models.FloatField(default=0)


class Transaction(models.Model):
    tx_id = models.CharField(max_length=20, default='1234')
    transaction_type = models.CharField(max_length=10, blank=False)  # deposit, withdrawal
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='transactions')
    qty = models.FloatField(default=0, blank=False, null=False)
    amount_usd = models.FloatField(default=0, blank=False, null=False)
    currency = models.CharField(max_length=10, blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)
    address = models.CharField(max_length=70, blank=True, null=True)
    reference = models.CharField(max_length=70, blank=True, null=True)
    hash = models.CharField(max_length=70, blank=True, null=True)
    status = models.CharField(max_length=10, default='pending')  # pending, completed, failed
    fee = models.FloatField(default=0)
    medium = models.CharField(max_length=10, default='')
    bank = models.ForeignKey(UserBankAccount, on_delete=models.CASCADE, related_name='transactions', null=True, default=None)


class Conversion(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='conversions')
    qty_from = models.FloatField(default=0)
    qty_to = models.FloatField(default=0)
    currency_from = models.CharField(max_length=10, blank=False, null=False)
    currency_to = models.CharField(max_length=10, blank=False, null=False)
    status = models.CharField(max_length=10, blank=False, null=False)  # completed
    created_at = models.DateTimeField(default=timezone.now)
