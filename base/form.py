from django.forms import ModelForm
from .models import Account, Transaction


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        exclude = ['customer','account_number', 'balance']

class TransferForm(ModelForm):
    class Meta:
        model =Transaction
        fields = '__all__'
        exclude =['sender', 'type', 'receiver','recv_no']