from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils.timezone import now
from .models import Account, Transaction
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('account_details')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def deposit(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()
        Transaction.objects.create(account=account, transaction_type='deposit', amount=amount)
        return redirect('account_details')
    return render(request, 'accounts/deposit.html')

@login_required
def withdraw(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        account = Account.objects.get(user=request.user)
        if amount > account.balance:
            return render(request, 'accounts/withdraw.html', {'error': 'Insufficient funds'})
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, transaction_type='withdrawal', amount=amount)
        return redirect('account_details')
    return render(request, 'accounts/withdraw.html')

@login_required
def transfer(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        to_account_number = request.POST.get('to_account')
        from_account = Account.objects.get(user=request.user)
        to_account = Account.objects.filter(account_number=to_account_number).first()
        if not to_account:
            return render(request, 'accounts/transfer.html', {'error': 'Recipient account not found'})
        if amount > from_account.balance:
            return render(request, 'accounts/transfer.html', {'error': 'Insufficient funds'})
        from_account.balance -= amount
        to_account.balance += amount
        from_account.save()
        to_account.save()
        Transaction.objects.create(account=from_account, transaction_type='transfer', amount=-amount)
        Transaction.objects.create(account=to_account, transaction_type='transfer', amount=amount)
        return redirect('account_details')
    return render(request, 'accounts/transfer.html')

@login_required
def account_details(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'accounts/details.html', {'account': account, 'transactions': transactions})
