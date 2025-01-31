from django.db import models

# Create your models here.
class AccountDetails(models.Model):
    number = models.CharField(max_length=20, default='')
    bank = models.CharField(max_length=20, default='')
    name = models.CharField(max_length=20, default='')  # bank name or Binance/Bybit as uid case may be
    uid = models.CharField(default='', max_length=20)
    account_type = models.CharField(default='bank')  # bank, crypto, uid

    