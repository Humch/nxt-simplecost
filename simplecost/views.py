from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import ThirdParty, PaymentMode, Expense

class ExpenseListView(ListView):
    
    model = Expense
    context_object_name = 'expenses'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ExpenseListView, self).dispatch(*args, **kwargs)
