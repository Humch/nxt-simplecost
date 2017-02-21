from django.forms import ModelForm, FileInput, FileField, Select, ModelChoiceField, DateField

from django import forms

from django.utils.safestring import mark_safe

from .models import ThirdParty, PaymentMode, Expense

class ExpenseForm(ModelForm):
    """
    Model form to create and update Expense Model object
    """
    class Meta:
        
        model = Expense
        fields = ['date_expense','third_party','amount','notes','payment_mode']
        

        