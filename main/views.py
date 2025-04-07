from django.shortcuts import render,redirect, redirect, get_object_or_404
from .forms import BankUserForm,WithdrawForm
from .models import BankUser,Userlogin,Transaction
from django.contrib import messages
import random
from decimal import Decimal
from django.utils import timezone


# Create your views here.
def home(request):
    return render(request, 'main/home.html',)

def signup(request):
    return render(request, 'main/signup.html',)

def login_view(request):
    return render(request, 'main/login.html',)


def generate_account_number():
    return str(random.randint(100000000000,999999999999))


def register_user(request):
    if request.method == "POST":
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        account_number = generate_account_number()

        user = BankUser.objects.create(
            name=name,
            dob=dob,
            gender=gender,
            city=city,
            country=country,
            pincode=pincode,
            account_number=account_number
        )
        request.session['registered_user_id'] = user.id
        return redirect('registration_success') 
    
    return render(request, 'main/signup.html')


def registration_success(request):
    user_id = request.session.get('registered_user_id')

    if user_id:
        user = BankUser.objects.get(id=user_id)
        return render(request, 'main/registration_success.html', {'user': user})




def create_userlogin_view(request):
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        dob = request.POST.get('dob')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = BankUser.objects.get(account_number=account_number, dob=dob)

            # Check if credentials already exist
            if Userlogin.objects.filter(bank_user=user).exists():
                return render(request, 'main/create_userlogins.html', {
                    'error': 'Credentials already created for this account.'
                })

            # Create the credentials
            Userlogin.objects.create(
                bank_user=user,
                username=username,
                password=password  # You can hash later
            )
            return redirect('login')

        except BankUser.DoesNotExist:
            return render(request, 'main/create_userlogin.html', {
                'error': 'Invalid account number or date of birth.'
            })

    return render(request, 'main/create_userlogin.html')



def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_cred = Userlogin.objects.get(username=username, password=password)
            request.session['user_id'] = user_cred.bank_user.id  # Save login session
            return redirect('bank_dashboard')
        except Userlogin.DoesNotExist:
            return render(request, 'main/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'main/login.html')


def bank_dashboard(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # if not logged in

    user = BankUser.objects.get(id=user_id)
    return render(request, 'main/bank_dashboard.html', {'user': user})



def logout_view(request):
    request.session.flush()
    messages.success(request,"You have been logged out successfully.")
    return redirect('home')





def withdraw_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = BankUser.objects.get(id=user_id)

    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount'))
        except:
            messages.error(request, "Invalid amount.")
            return render(request, 'main/withdraw.html', {'user': user})

        if amount <= 0:
            messages.error(request, "Amount must be positive.")
        elif user.balance < amount:
            messages.error(request, "Insufficient balance.")
        else:
            user.balance -= amount
            user.save()

            Transaction.objects.create(
                bank_user=user,
                transaction_type='W',
                amount=amount,
                description="ATM Withdrawal"
            )

            messages.success(request, f"₹{amount} withdrawn successfully.")

    return render(request, 'main/withdraw.html', {'user': user})





def fund_transfer(request):
    if request.method == "POST":
        sender_id = request.session.get('user_id')
        receiver_acc = request.POST.get('receiver_account')
        amount_str = request.POST.get('amount')

        try:
            amount = Decimal(amount_str)
        except:
            return render(request, 'main/fund_transfer.html', {'error': 'Invalid amount'})

        try:
            sender = BankUser.objects.get(id=sender_id)
            receiver = BankUser.objects.get(account_number=receiver_acc)

            if sender == receiver:
                return render(request, 'main/fund_transfer.html', {'error': "You can't transfer to your own account"})

            if sender.balance < amount:
                return render(request, 'main/fund_transfer.html', {'error': 'Insufficient balance'})

            # Perform transfer
            sender.balance -= amount
            receiver.balance += amount
            sender.save()
            receiver.save()

            # Sender transaction
            Transaction.objects.create(
                bank_user=sender,
                transaction_type='T',
                amount=amount,
                timestamp=timezone.now(),
                description=f"Transferred to {receiver.name} ({receiver.account_number})",
                receiver=receiver
            )

            # Receiver transaction
            Transaction.objects.create(
                bank_user=receiver,
                transaction_type='D',
                amount=amount,
                timestamp=timezone.now(),
                description=f"Received from {sender.name} ({sender.account_number})",
                receiver=sender
            )

            return render(request, 'main/fund_transfer.html', {
                'success': f'Transferred ₹{amount} to {receiver.name} ({receiver.account_number})',
                'sender': sender
            })

        except BankUser.DoesNotExist:
            return render(request, 'main/fund_transfer.html', {'error': 'Receiver not found'})

    return render(request, 'main/fund_transfer.html')



def transaction_history(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = BankUser.objects.get(id=user_id)
    transactions = Transaction.objects.filter(bank_user=user).order_by('-timestamp')
    
    return render(request, 'main/transaction_history.html', {
        'user': user,
        'transactions': transactions,
    })


def deposit_view(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = BankUser.objects.get(id=user_id)
    context = {'user': user}

    if request.method == "POST":
        try:
            amount = Decimal(request.POST.get('amount'))
            if amount > 0:
                user.balance += amount
                user.save()

                Transaction.objects.create(
                    bank_user=user,
                    transaction_type='D',
                    amount=amount,
                    timestamp=timezone.now(),
                    description="Money deposited by user"
                )

                context['success'] = True
                context['amount'] = amount
            else:
                context['error'] = 'Amount must be greater than zero.'
        except:
            context['error'] = 'Invalid amount.'

    return render(request, 'main/deposit.html', context)



def delete_account(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = BankUser.objects.get(id=user_id)

    if request.method == "POST":
        # Delete the user and their login credentials
        Userlogin.objects.filter(bank_user=user).delete()
        Transaction.objects.filter(bank_user=user).delete()
        user.delete()
        request.session.flush()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')

    return render(request, 'main/delete_account.html', {'user': user})