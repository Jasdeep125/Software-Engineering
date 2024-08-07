from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    account_number = models.CharField(max_length=20, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.username


class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('business', 'Business'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    account_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.user.username} - {self.account_number}'
    

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    
    
class CheckbookRequest(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='pending')

    def __str__(self):
        return f'Checkbook Request for {self.account.account_number}'
