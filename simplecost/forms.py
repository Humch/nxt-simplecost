from django import forms
from django.forms import ModelForm, ModelChoiceField, DateField, DecimalField,CharField, Select

from django.utils.translation import ugettext as _

from .models import ThirdParty, PaymentMode, Expense

class ExpenseForm(ModelForm):
    """
    Model form to create and update Expense Model object
    """
    date_expense = DateField(
                        label = _('Expense Date')
                    )
    
    third_party = ModelChoiceField(
                    queryset = ThirdParty.objects.all(),
                    label = _("Third Party"),
                    widget = Select(attrs={'required':True})
                )
    
    amount = DecimalField(
                label = _("Amount")
            )
    
    notes = CharField(
                label = _("Notes"),
                widget=forms.Textarea
    )
    
    payment_mode = ModelChoiceField(
                        queryset = PaymentMode.objects.all(),
                        label = _("Payment Mode"),
                        widget = Select(attrs={'required':True})
                    )
    
    class Meta:
        
        model = Expense
        fields = ['date_expense','third_party','amount','notes','payment_mode']
        

        