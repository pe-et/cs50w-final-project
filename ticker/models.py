from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Transaction(models.Model):
    user = models.ForeignKey("User", on_delete=models.PROTECT, related_name="transactions")
    ticker = models.CharField(max_length=6)
    units = models.DecimalField(max_digits=50, decimal_places=8)
    cost_basis = models.DecimalField(max_digits=50, decimal_places=8)
    quote_currency = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)

class Benchmark(models.Model):
    user = models.ForeignKey("User", on_delete=models.PROTECT, related_name="benchmark")
    ticker = models.CharField(max_length=6)
    units = models.DecimalField(max_digits=50, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)
