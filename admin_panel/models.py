from django.db import models


# Create your models here.
class AccountDetails(models.Model):
    number = models.CharField(max_length=20, default='', null=True)
    bank = models.CharField(max_length=20, default='', null=True)
    name = models.CharField(max_length=20, default='', null=True)  # bank name or Binance/Bybit as uid case may be
    uid = models.CharField(default='', max_length=20, null=True)
    account_type = models.CharField(default='bank', max_length=10)  # bank, crypto, uid
    platform = models.CharField(default='', max_length=10)  # bybit, platform

