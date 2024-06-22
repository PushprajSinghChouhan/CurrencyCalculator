from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_currency = models.CharField(max_length=10, default='USD')


class ConversionHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source_currency = models.CharField(max_length=3)
    target_currency = models.CharField(max_length=3)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=6)
    converted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} {self.source_currency} to {self.target_currency} = {self.converted_amount} @ {self.exchange_rate}"

class FinancialNews(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    published_date = models.DateTimeField()

class CurrencyRate(models.Model):
    pass




    def __str__(self):
        return f"{self.amount} {self.source_currency} to {self.target_currency} = {self.converted_amount} @ {self.exchange_rate}"
