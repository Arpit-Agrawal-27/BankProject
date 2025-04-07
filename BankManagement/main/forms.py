from django import forms
from .models import BankUser


class BankUserForm(forms.ModelForm):
    class Meta:
        model= BankUser
        fields = ['name','dob','gender','city','country','pincode']


class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01, label="Withdraw Amount")