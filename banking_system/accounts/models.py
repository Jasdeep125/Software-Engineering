from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('personal', 'Personal'),
        ('business', 'Business'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
