from django import forms
from .models import Transaction

class SearchCustomerForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['customer']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']