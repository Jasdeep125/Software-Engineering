from django import forms
from django.contrib.auth.models import User


class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

class WithdrawalForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']