from django.db import models
from django.contrib.auth.models import User

# Create your models here.

tran_types =(
    ('credit', 'credit'),
    ('debit', 'debit'),
    ('deposit', 'deposit'),
    ('withdraw', 'withdraw'),
)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    profile = models.ImageField(null=True)
    dob = models.DateField()
    file = models.FileField(null=True, upload_to='files/')
    def __str__(self):
        return self.user.username

class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    name =models.CharField(max_length=100)
    account_number = models.CharField(max_length=10, unique=True)
    pin = models.CharField(max_length=4)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    def __str__ (self):
        return self.name

class Transaction(models.Model):
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    recv_no = models.CharField(max_length=10, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    about = models.TextField(blank=True, null=True)
    type  = models.CharField(max_length=10, choices=tran_types, default='credit')
    class Meta:
        ordering = ['-time']
    def __str__(self):
        return f' {self.sender}, {str(self.amount)}'
    

