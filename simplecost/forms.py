from django import forms
from django.forms import ModelForm, ModelChoiceField, DateField, DecimalField,CharField, Select

from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from .models import ThirdParty, PaymentMode, Expense


class ThirdPartyForm(ModelForm):
    """
    Model form to create Third Party Model object
    """
    
    name = CharField(
                label = _("Name")
    )
    
    class Meta:
        
        model = ThirdParty
        fields = ['name']
    

class ExpenseForm(ModelForm):
    """
    Model form to create and update Expense Model object
    """
    date_expense = DateField(
                        label = _('Expense Date'),
                        required = True
                    )
    
    third_party = ModelChoiceField(
                    queryset = ThirdParty.objects.all(),
                    label = mark_safe(_("Third Party") + ' <a href="#" onClick="addThirdParty()"><i class="fi-plus green-color"></i></a>'),
                    required = True
                )
    
    amount = DecimalField(
                label = _("Amount"),
                required = True
            )
    
    notes = CharField(
                label = _("Notes"),
                widget=forms.Textarea,
                required = False
    )
    
    payment_mode = ModelChoiceField(
                        queryset = PaymentMode.objects.all(),
                        label = _("Payment Mode"),
                        required = True
                    )
    
    class Meta:
        
        model = Expense
        fields = ['date_expense','third_party','amount','notes','payment_mode']
        

        