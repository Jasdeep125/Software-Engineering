from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal


###############################################################################################


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        account_number = request.POST.get('account_number', '')

        if username and password and user_type and first_name and last_name and email:
            if user_type not in dict(CustomUser.USER_TYPE_CHOICES).keys():
                messages.error(request, 'Invalid user type')
                return render(request, 'register.html')

            if user_type == 'customer' and not account_number:
                messages.error(request, 'Account number is required for customers')
                return render(request, 'register.html')
            
            user = CustomUser.objects.create_user(
                username=username, 
                password=password, 
                first_name=first_name, 
                last_name=last_name,
                email=email,
                user_type=user_type,
                account_number=account_number
            )
            user.save()
            messages.success(request, 'User registered successfully')
            return redirect('login')
        else:
            messages.error(request, 'All fields are required')

    return render(request, 'register.html')

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.user_type == 'admin':
                return redirect('admin_dashboard')  # Redirect to the admin dashboard
            else:
                print("else m hu")
                return redirect('customer_dashboard')  # Redirect to the customer dashboard
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

@login_required
def admin_dashboard(request):
    ACCOUNT_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('business', 'Business'),
    ]

    customers = CustomUser.objects.filter(user_type='customer')
    print('customers',customers)
    accounts = Account.objects.all()
    return render(request, 'admin_dashboard.html', {
        'customers': customers,
        'accounts': accounts,
        'account_type_choices': ACCOUNT_TYPE_CHOICES
    })
    
    


# @login_required
# def customer_dashboard(request):
#     print(request.user)
#     account = Account.objects.filter(user=request.user).first()
#     if not account:
#         # messages.error(request, 'No account found for this user.')
#         return redirect('login')
    
#     return render(request, 'customer_dashboard.html', {
#         'account': account,
#     })

@login_required
def customer_dashboard(request):
    account = Account.objects.filter(user=request.user).first()
    if not account:
        return redirect('create_account')  # Redirect to create account if no account exists

    return render(request, 'customer_dashboard.html', {'account': account})



# Logout view
@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Account
import uuid

@login_required
def create_account(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type')
        if account_type not in dict(Account.ACCOUNT_TYPE_CHOICES).keys():
            messages.error(request, 'Invalid account type')
            return render(request, 'create_account.html')

        account_number = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique account number

        account = Account.objects.create(
            user=request.user,
            account_holder_name=request.user.username,  # Assign the username as the account holder name
            account_type=account_type,
            account_number=account_number
        )
        account.save()
        messages.success(request, 'Account created successfully')
        return redirect('view_account', account_id=account.id)
    
    ACCOUNT_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('business', 'Business'),
    ]

    customers = CustomUser.objects.filter(user_type='customer')
    return render(request, 'create_account.html', {'account_type_choices': ACCOUNT_TYPE_CHOICES, "customers": customers})

@login_required
def edit_account(request, account_id):
    account = Account.objects.get(id=account_id)
    if request.method == 'POST':
        account_type = request.POST.get('account_type')
        if account_type in dict(Account.ACCOUNT_TYPE_CHOICES).keys():
            account.account_type = account_type
            account.save()
            messages.success(request, 'Account details updated successfully')
            return redirect('view_account', account_id=account.id)
        else:
            messages.error(request, 'Invalid account type')

    return render(request, 'edit_account.html', {'account': account})


@login_required
def close_account(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    account.delete()
    messages.success(request, 'Account closed successfully')
    return redirect('admin_dashboard')


@login_required
def deposit(request, account_id):
    if request.method == 'POST':
        try:
            account = Account.objects.get(id=account_id, user=request.user)
        except Account.DoesNotExist:
            messages.error(request, 'Account not found')
            return redirect('customer_dashboard')

        amount = request.POST.get('amount')
        if amount:
            amount = Decimal(amount)  # Convert the amount to a Decimal
            account.balance += amount
            account.save()

            # Create a transaction record
            Transaction.objects.create(
                account=account,
                amount=amount,
                transaction_type='deposit'
            )

            messages.success(request, f'Deposited {amount} successfully')
            return redirect('view_account', account_id=account.id)
        else:
            messages.error(request, 'Amount is required')

    return render(request, 'deposit.html')


@login_required
def withdraw(request, account_id):
    if request.method == 'POST':
        account = Account.objects.get(id=account_id, user=request.user)
        amount = request.POST.get('amount')
        if amount:
            amount = Decimal(amount)
            if account.balance >= amount:
                account.balance -= amount
                account.save()

                # Create a transaction record
                Transaction.objects.create(
                    account=account,
                    amount=amount,
                    transaction_type='withdrawal'
                )

                messages.success(request, f'Withdrew {amount} successfully')
                return redirect('view_account', account_id=account.id)
            else:
                messages.error(request, 'Insufficient balance')
        else:
            messages.error(request, 'Amount is required')

    return render(request, 'withdraw.html')



@login_required
def transfer(request):
    if request.method == 'POST':
        from_account_id = request.POST.get('from_account')
        to_account_id = request.POST.get('to_account')
        amount = request.POST.get('amount')

        from_account = Account.objects.get(id=from_account_id, user=request.user)
        to_account = Account.objects.get(id=to_account_id, user=request.user)
        

        if amount and from_account and to_account:
            amount = float(amount)
            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()

                # Create transaction records
                Transaction.objects.create(
                    account=from_account,
                    amount=amount,
                    transaction_type='transfer'
                )
                Transaction.objects.create(
                    account=to_account,
                    amount=amount,
                    transaction_type='transfer'
                )

                messages.success(request, 'Transfer successful')
                return redirect('home')
            else:
                messages.error(request, 'Insufficient balance')
        else:
            messages.error(request, 'All fields are required')

    accounts = Account.objects.filter(user=request.user)
    return render(request, 'transfer.html', {'accounts': accounts})


@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(account__user=request.user)

    if request.method == 'GET':
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        transaction_type = request.GET.get('transaction_type')
        amount_min = request.GET.get('amount_min')
        amount_max = request.GET.get('amount_max')

        if date_from:
            transactions = transactions.filter(date__gte=date_from)
        if date_to:
            transactions = transactions.filter(date__lte=date_to)
        if transaction_type:
            transactions = transactions.filter(transaction_type=transaction_type)
        if amount_min:
            transactions = transactions.filter(amount__gte=amount_min)
        if amount_max:
            transactions = transactions.filter(amount__lte=amount_max)

    return render(request, 'transaction_history.html', {'transactions': transactions})


@login_required
def view_account(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    return render(request, 'view_account.html', {'account': account, 'transactions': transactions})



@login_required
def request_checkbook(request, account_id):
    account = Account.objects.get(id=account_id, user=request.user)
    CheckbookRequest.objects.create(account=account)
    messages.success(request, 'Checkbook requested successfully')
    return redirect('view_account', account_id=account.id)
