from django.db import models
from datetime import datetime

# Create your models here.
class BankUser(models.Model):
    GENDER_CHOICES =[
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),
    ]
    name=models.CharField(max_length=100)
    dob=models.DateField()
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES)
    city=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    pincode=models.CharField(max_length=10)
    account_number=models.CharField(max_length=12,unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} - {self.account_number}"
    

class Userlogin(models.Model):
    bank_user = models.OneToOneField(BankUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # Store hashed password later for security

    def __str__(self):
        return self.username
    



class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('D', 'Deposit'),
        ('W', 'Withdraw'),
        ('T', 'Transfer'),
    ]

    bank_user = models.ForeignKey(BankUser, on_delete=models.CASCADE, related_name='transactions')  # sender
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    receiver = models.ForeignKey(BankUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_transactions')  # for transfer

    def __str__(self):
        return f"{self.bank_user.name} - {self.get_transaction_type_display()} - ₹{self.amount}"
