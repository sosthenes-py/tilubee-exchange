from django.db import models


class Ticker(models.Model):
    coin_short = models.CharField(max_length=10)
    coin_long = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    change = models.FloatField(default=0)
    network = models.CharField(max_length=10, default='bep20')
    min = models.FloatField(default=1)
    max = models.FloatField(default=1000)