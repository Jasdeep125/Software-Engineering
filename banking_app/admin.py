from django.contrib import admin
from .models import CustomUser, Account, Transaction, CheckbookRequest

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'account_number')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('user_type',)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type', 'balance', 'account_number')
    search_fields = ('user__username', 'account_number')
    list_filter = ('account_type',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'transaction_type', 'date')
    search_fields = ('account__account_number', 'transaction_type')
    list_filter = ('transaction_type', 'date')

@admin.register(CheckbookRequest)
class CheckbookRequestAdmin(admin.ModelAdmin):
    list_display = ('account', 'request_date', 'status')
    search_fields = ('account__account_number',)
    list_filter = ('status', 'request_date')
