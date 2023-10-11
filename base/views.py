from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Customer, Account, Transaction
from django.contrib import messages
from .form import AccountForm, TransferForm
import random

# Create your views here.
def login_page(request):
    user = User.objects.all()
    if request.user.is_authenticated:
        logout(request)
    #page = "login"
    #if request.user.is_authenticated:
        #return redirect('home')
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            print("also")
        except:
            print("true")
            message = messages.error(request, 'user does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    context = {}

    return render(request, 'base/login-register.html')

@login_required(login_url='login')
def home(request):
    user = request.user

    customer = Customer.objects.get(user=user)
    if customer.account_set.all().count() == 0:
        return redirect('create-acc')
    accounts = Account.objects.get(customer=customer)
    transactions = Transaction.objects.filter(Q(receiver=accounts.name)| Q(sender=accounts.name))[0:2]
    num = accounts.account_number
    
    print(transactions)

    
    content={'user':user, 'customer':customer, 'accounts':accounts, 'transactions':transactions, 'num':num}
    return render(request, 'base/home.html', content)

@login_required(login_url='login')
def CreateAccount(request):
    customer = Customer.objects.get(user=request.user)
    form = AccountForm()
    if request.method == 'POST':
        acct_name = request.POST.get('name')
        pin = request.POST.get('pin')
        if pin.isnumeric:
            acct_no = random.randrange(1000000000, 9999999999)
            Account.objects.create(
                customer = customer,
                name =acct_name,
                account_number = acct_no,
                pin = pin,
            )
                
            
           
            return redirect('home')
            
    content = {'form':form}
    return render(request, 'base/create-room.html', content)

@login_required(login_url='login')
def Transactions(request, ak):
    page = True
    
    customer = Customer.objects.get(user=request.user)
    user_account = Account.objects.get(customer=customer)
    
    recieve = None
    
    if request.method =='POST':
        acct_no = request.POST.get('acct-no')
        print(acct_no)
        print('hello it worked')
        recv_acc = Account.objects.get(account_number=acct_no)
        if recv_acc != None:
            print('hello it worked')
            page=False
            
            
            return redirect('transfer', ak=user_account.id,pk=recv_acc.account_number)
        
    content = {'user_acc':user_account, 'page':page}
    return render(request, 'base/transfer.html', content)

@login_required(login_url='login')
def Transfer(request, ak,pk):
    page =False
    form = TransferForm()
    customer = Customer.objects.get(user=request.user)
    accounts = Account.objects.get(id=ak)
    account = Account.objects.get(customer=customer)
    if accounts.customer != customer:
        return HttpResponse('you are not allowed here')
    recv_acc = Account.objects.get(account_number=pk)
    if request.method == 'POST':
        amount = int(request.POST.get('amount'))
        about = request.POST.get('about')
        form = TransferForm(request.POST)
        if form.is_valid():
            if account.balance>= int(amount):
                balance = account.balance - amount
                recv_balance = recv_acc.balance + amount
                account.balance=balance
                recv_acc.balance = recv_balance
                about = about
                account.save()
                recv_acc.save()
            else:
                return HttpResponse('you have insufficient funds')    
            transaction =form.save(commit=False)
            transaction.sender = accounts.name
            print(accounts.name)
            transaction.receiver = recv_acc.name
            transaction.recv_no = recv_acc.account_number
            transaction.type = 'debit'
            transaction.save()
            

            return redirect('home')

    content ={'form':form,'page':page, 'recv_acc':recv_acc, 'accounts':accounts  }
    return render(request, 'base/transfer.html', content)

@login_required(login_url='login')
def Transactionss(request):
    customer= Customer.objects.get(user=request.user)
    account = Account.objects.get(customer=customer)
    transactions = Transaction.objects.filter(Q(sender=account.name)| Q(receiver=account.name))
    num = account.account_number
    context = {'transactions':transactions,'num':num, 'account':account}
    return render(request, 'base/transactions.html', context)