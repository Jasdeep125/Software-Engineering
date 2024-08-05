from django.contrib import admin
from .models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type', 'balance')
    search_fields = ('user__username', 'account_type')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'date')
    list_filter = ('transaction_type', 'date')
    search_fields = ('account__user__username', 'transaction_type')
